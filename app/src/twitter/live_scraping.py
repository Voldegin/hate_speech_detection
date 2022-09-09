# Public Imports
from threading import Event, Thread
from dateutil.parser import parse
from datetime import timedelta

# Private Imports
from src.db.db_operations import select_all_live_scraping, update_last_scrap, \
    insert_data
from src.twitter.condition_scraping import condition_based_scraping
from config import MODEL_LIST, MODEL_PREDICTIONS
from src.utils.format_twitter_preds import format_predictions


def call_repeatedly(interval, func):
    stopped = Event()

    def loop():
        while not stopped.wait(
                interval):  # the first call is in `interval` secs
            func()

    Thread(target=loop).start()
    return stopped.set


def live_scraping():
    print("Live Scrapping started")
    data = select_all_live_scraping()
    for each_row in data:
        print(each_row)
        username = each_row["username"]
        model = each_row["model"]
        start_date = each_row["start_date"]

        if each_row["last_scrapped_time"] == "None":
            last_scrapped_time = None
        else:
            last_scrapped_time = each_row["last_scrapped_time"]

        if last_scrapped_time:
            start_date = last_scrapped_time

        code, tweets, full_data = condition_based_scraping(username,
                                                           start_date=start_date)
        print("\n\n", len(full_data), "\n\n")
        if code != 200:
            print("Failed scraping during live scrap")

        if not full_data.empty and code == 200:
            model_details = [x for x in MODEL_LIST if x["name"] == model]
            model_details = model_details[0]
            model_func = model_details["function"]
            model_config = model_details["config"]

            predictions = model_func(input_text=tweets,
                                     model_config=model_config)

            result = format_predictions(full_data, predictions)

            insert_data(result, model, username)

            last_date = parse(full_data['date'].max()) + timedelta(seconds=1)
            update_last_scrap(username, model, last_date)


def initialise_live_scraping():
    cancel_future_calls = call_repeatedly(25, live_scraping)
