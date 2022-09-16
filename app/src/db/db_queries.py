LIVE_SCRAP_CHECK = """select * from live_scraping_details 
where username='{username}' and model='{model}'"""

INSERT_LIVE = """insert into live_scraping_details VALUES(null, '{username}', 
'{model}', '{start_date}', '{replies}','{last_scrapped_time}', 
'{last_viewed_time}')"""

DELETE_LIVE = """delete from live_scraping_details 
where username='{username}' and model='{model}'"""

SELECT_ALL_LIVE = """select * from live_scraping_details"""

UPDATE_LAST_SCRAP = """update live_scraping_details 
set last_scrapped_time='{last_scrapped_time}' where username='{username}' 
and model='{model}'"""

LAST_VIEW_QUERY = """select max(last_viewed_time) as last_view_time 
from live_scraping_details 
where username='{username}' and model='{model}'"""

FETCH_QUERY = """select username, model, date, text, prediction, tweet_author 
from twitter_data where username='{username}' 
and model='{model}'"""

UPDATE_LAST_VIEW = """update live_scraping_details 
set last_viewed_time='{last_viewed_time}' where username='{username}' 
and model='{model}'"""

INSERT_DATA = """insert into twitter_data VALUES(null, '{username}', 
'{model}', '{date}', '{text}','{tweet_author}', '{prediction}')"""

CHECK_DATA = """select * from twitter_data where username='{username}' 
and model='{model}' and date='{date}' and text='{text}' 
and tweet_author='{tweet_author}' """
