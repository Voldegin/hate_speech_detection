# Public Imports
from datetime import datetime

# Private Imports
from config import DB_ENGINE
from src.db.db_queries import LIVE_SCRAP_CHECK, INSERT_LIVE, DELETE_LIVE


def insert_data(data, username):
    data['username'] = username
    data.to_sql('twitter_data', DB_ENGINE, if_exists='append', index=False)


def insert_live_scraping(username, model):
    check_exist_query = LIVE_SCRAP_CHECK.format(username=username, model=model)
    check_exist = DB_ENGINE.execute(check_exist_query)
    result = [row[0] for row in check_exist]
    if result:
        return "Live scrapping already being done for username and model", 400

    start_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    insert_query = INSERT_LIVE.format(username=username, model=model,
                                      start_date=start_date,
                                      last_scrapped_time=None,
                                      last_viewed_time=None)

    DB_ENGINE.execute(insert_query)
    return "Liver scrapping started for username: " + username + " and model: " + model, 200


def delete_live_scraping(username, model):
    delete_query = DELETE_LIVE.format(username=username, model=model)
    DB_ENGINE.execute(delete_query)
    return "Liver scrapping stopped for username: " + username + " and model: " + model, 200
