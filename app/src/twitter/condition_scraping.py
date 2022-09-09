# Public Imports
import traceback
import pandas as pd
import twint
import nest_asyncio

# Private Imports
from log import logger

nest_asyncio.apply()


def condition_based_scraping(username, start_date=None, end_date=None):
    try:
        c = twint.Config()
        c.Hide_output = True
        c.Username = username

        if start_date:
            c.Since = start_date
        if end_date:
            c.Until = end_date

        logger.info(start_date)
        logger.info(end_date)

        # c.Limit = 2

        # c.Search = ['chelei']
        # c.Min_likes = 3000
        # c.Popular_tweets = True

        # c.Images= False
        # c.Videos = False
        # c.Media = False

        # c.Store_csv = True
        # c.Store_json = True
        # c.Output = "tweets.json"

        # c.All = True
        # c.Debug = False

        c.Pandas = True

        twint.run.Search(c)

        tweets_df = twint.storage.panda.Tweets_df
        columns = ['date', 'tweet']

        if tweets_df.empty:
            tweets_df = pd.DataFrame(columns=columns)

        return 200, tweets_df['tweet'].tolist(), tweets_df[columns]
    except ValueError as e:
        if "Cannot find twitter account with name" in str(e):
            return 400, "Twitter username not found", -1
    except Exception as e:
        logger.info(e)
        logger.info(traceback.format_exc())
        return 500, "Error while fetching tweets", -1
