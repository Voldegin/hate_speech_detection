DROP TABLE IF EXISTS twitter_data;

CREATE TABLE IF NOT EXISTS twitter_data (
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT NOT NULL,
model TEXT,
date TEXT,
text TEXT,
tweet_author TEXT,
prediction INT
);

DROP TABLE IF EXISTS live_scraping_details;

CREATE TABLE IF NOT EXISTS live_scraping_details (
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT NOT NULL,
model TEXT,
start_date TEXT,
replies BOOLEAN,
last_scrapped_time TEXT,
last_viewed_time TEXT
);