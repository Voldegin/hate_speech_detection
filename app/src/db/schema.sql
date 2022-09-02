DROP TABLE IF EXISTS twitter_data;

CREATE TABLE twitter_data (
id INTEGER PRIMARY KEY AUTOINCREMENT,
username VARCHAR NOT NULL,
model VARCHAR,
date VARCHAR,
text VARCHAR,
prediction INT
);

DROP TABLE IF EXISTS live_scraping_details;

CREATE TABLE live_scraping_details (
id INTEGER PRIMARY KEY AUTOINCREMENT,
username VARCHAR NOT NULL,
model VARCHAR,
start_date TEXT,
last_scrapped_time VARCHAR,
last_viewed_time VARCHAR
);