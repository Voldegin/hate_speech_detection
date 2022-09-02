LIVE_SCRAP_CHECK = """select * from live_scraping_details 
where username='{username}' and model='{model}'"""

INSERT_LIVE = """insert into live_scraping_details VALUES(null, '{username}', 
'{model}', '{start_date}', '{last_scrapped_time}', '{last_viewed_time}')"""

DELETE_LIVE = """delete from live_scraping_details 
where username='{username}' and model='{model}'"""

SELECT_ALL_LIVE = """select * from live_scraping_details"""

UPDATE_LAST_SCRAP = """update live_scraping_details 
set last_scrapped_time='{last_scrapped_time}' where username='{username}' 
and model='{model}'"""

LAST_VIEW_QUERY = """select max(last_viewed_time) as last_view_time 
from live_scraping_details 
where username='{username}' and model='{model}'"""

FETCH_QUERY = """select username, model, date, text, prediction 
from twitter_data where username='{username}' 
and model='{model}'"""

UPDATE_LAST_VIEW = """update live_scraping_details 
set last_viewed_time='{last_viewed_time}' where username='{username}' 
and model='{model}'"""
