# Public Imports
from datetime import datetime

# Private Imports
from config import DB_ENGINE
from src.db.db_queries import LIVE_SCRAP_CHECK, INSERT_LIVE, DELETE_LIVE, \
    SELECT_ALL_LIVE, UPDATE_LAST_SCRAP, LAST_VIEW_QUERY, FETCH_QUERY, \
    UPDATE_LAST_VIEW, INSERT_DATA, CHECK_DATA


def format_db_result(result):
    d, a = {}, []
    for row in result:
        # row.items() returns an array like [(key0, value0), (key1, value1)]
        for column, value in row.items():
            # build up the dictionary
            d = {**d, **{column: value}}
        a.append(d)
    return a


def insert_data(data, model, username):
    for index, row in data.iterrows():
        date = row['date']
        text = row['text']
        tweet_author = row['tweet_author']
        prediction = row['prediction']
        check_exist_query = CHECK_DATA.format(username=username, model=model,
                                              date=date, text=text,
                                              tweet_author=tweet_author)
        check_exist = DB_ENGINE.execute(check_exist_query)
        result = [row[0] for row in check_exist]
        if result:
            continue
        insert_query = INSERT_DATA.format(username=username, model=model,
                                          date=date, text=text,
                                          tweet_author=tweet_author,
                                          prediction=prediction)
        DB_ENGINE.execute(insert_query)


def insert_live_scraping(username, model, replies):
    check_exist_query = LIVE_SCRAP_CHECK.format(username=username, model=model)
    check_exist = DB_ENGINE.execute(check_exist_query)
    result = [row[0] for row in check_exist]
    if result:
        return "Live scrapping already being done for username and model", 400

    start_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    insert_query = INSERT_LIVE.format(username=username, model=model,
                                      start_date=start_date,
                                      replies=replies,
                                      last_scrapped_time=None,
                                      last_viewed_time=None)

    DB_ENGINE.execute(insert_query)
    msg = f"Liver scrapping started for username: {username} and model: {model}"
    msg.format(username=username, model=model)
    return msg, 200


def delete_live_scraping(username, model):
    delete_query = DELETE_LIVE.format(username=username, model=model)
    DB_ENGINE.execute(delete_query)
    msg = f"Liver scrapping stopped for username: {username} and model: {model}"
    msg.format(username=username, model=model)
    return msg, 200


def select_all_live_scraping():
    result = DB_ENGINE.execute(SELECT_ALL_LIVE)
    data = format_db_result(result)
    return data


def update_last_scrap(username, model, last_date):
    update_query = UPDATE_LAST_SCRAP.format(username=username, model=model,
                                            last_scrapped_time=last_date)
    DB_ENGINE.execute(update_query)


def get_tweet_results(username, model, show_all, limit):
    last_view_time = None
    if not show_all:
        last_view_query = LAST_VIEW_QUERY.format(username=username, model=model)
        last_view_time = DB_ENGINE.execute(last_view_query)
        last_view_time = format_db_result(last_view_time)[0]["last_view_time"]
        if last_view_time == "None":
            last_view_time = None

    fetch_query = FETCH_QUERY.format(username=username, model=model)
    if last_view_time:
        fetch_query += f" and date >= '{last_view_time}'"
    fetch_query += " limit " + str(limit)

    result = DB_ENGINE.execute(fetch_query)
    data = format_db_result(result)

    # update last view
    new_last_view = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    update_query = UPDATE_LAST_VIEW.format(username=username, model=model,
                                           last_viewed_time=new_last_view)
    DB_ENGINE.execute(update_query)

    return data
