# Public Imports
import twint
import nest_asyncio

nest_asyncio.apply()


def condition_based_scraping(username, start_date=None, end_date=None):
    c = twint.Config()
    c.Hide_output = True
    c.Username = username

    if start_date:
        c.Since = start_date
    if end_date:
        c.Until = end_date


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

    return tweets_df['tweet'], tweets_df[columns]
