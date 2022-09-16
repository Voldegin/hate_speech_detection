# Public Imports
import traceback
import pandas as pd
import twint
import nest_asyncio

# Private Imports
from log import logger

nest_asyncio.apply()


def condition_based_scraping(username, start_date=None, end_date=None,
                             search=False):
    try:
        c = twint.Config()
        c.Hide_output = True
        if search:
            c.Search = [username]
        else:
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

        return 200, tweets_df
    except ValueError as e:
        if "Cannot find twitter account with name" in str(e):
            return 400, "Twitter username not found"
    except Exception as e:
        logger.info(e)
        logger.info(traceback.format_exc())
        return 500, "Error while fetching tweets"


def fetch_tweet_data(username, start_date=None, end_date=None, replies=False):
    columns = ['date', 'tweet', 'tweet_author']
    code, tweets_df = condition_based_scraping(username, start_date=start_date,
                                               end_date=end_date,
                                               search=False)
    if tweets_df.empty or code != 200:
        tweets_df = pd.DataFrame(columns=columns)
        return 200, tweets_df['tweet'].tolist(), tweets_df[columns]
    if replies:
        # Fetch Replies from twitter based on conversation id
        reply_code, reply_tweets_df = condition_based_scraping(username,
                                                               start_date=start_date,
                                                               end_date=end_date,
                                                               search=True)
        if not reply_tweets_df.empty and reply_code == 200:
            conversation_id = tweets_df[tweets_df['reply_to'].str.len() == 0][
                'conversation_id'].tolist()
            filtered_reply_df = reply_tweets_df[reply_tweets_df['conversation_id'].isin(
                conversation_id)].sort_values('date', ascending=False)
            tweets_df = filtered_reply_df.merge(tweets_df,on=['date', 'tweet', 'username'],how='outer')

    new_tweets_df = tweets_df.copy()
    new_tweets_df.rename(columns={"username": "tweet_author"}, inplace=True)
    logger.info(len(new_tweets_df))

    return 200, new_tweets_df['tweet'].tolist(), new_tweets_df[columns]
