LIVE_SCRAP_CHECK = """select * from live_scraping_details 
where username='{username}' and model='{model}'"""

INSERT_LIVE = """insert into live_scraping_details VALUES(null, '{username}', 
'{model}', '{start_date}', '{last_scrapped_time}', '{last_viewed_time}')"""

DELETE_LIVE = """delete from live_scraping_details 
where username='{username}' and model='{model}'"""