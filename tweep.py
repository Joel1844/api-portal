import tweepy
# import pandas as pd

consumer_key = 'ImGK6XiE4b2VgNlGfMO3J5O3I'
consumer_secret = 'fnkmexUjUfiGfTa7yFLWqZY1swV1NJbfia3M9uVjBHJQKgtHkv'
# bearer_token = 'AAAAAAAAAAAAAAAAAAAAAHBOkQEAAAAAbFEs45qSVgMYsEVogQxPk9NxUHA%3DKgpRZCJxYZfTSz8K0D4SxkrHaLuh4QMoxS6LeumMdSmPjzGzZn'
access_token = '1420432654646890506-JMgm4g9sj0h4jtm1aceI1WHF6XkjJT'
access_token_secret = 'T1J1AV6sul8AHsxXAahqrHr6OYgOLAjDMdsSpFspBMnwL'
#Pass in our twitter API authentication key
auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret,
    access_token, access_token_secret
)

#Instantiate the tweepy API
api = tweepy.API(auth, wait_on_rate_limit=True)


search_query = ['violencia']
no_of_tweets = 200
geo = '18.7009,-70.16546,100km'


try:
    #bsucar tweets por palabras clave que estan en la lista search_query
    # tweets = tweepy.Cursor(api.search, q=search_query, lang='es', geocode=geo,hidden = True).items(no_of_tweets)

    #buscar tweets por palabras clave que estan en la lista search_query
    # tweets = tweepy.Cursor(api.search, q=search_query, lang='es', geocode=geo,hidden = True).items(no_of_tweets)1
    tweets = api.search_tweets(q=search_query, count=no_of_tweets, hidden=True, geocode=geo)
 
    attributes_container = [[tweet.created_at, tweet.user.screen_name, tweet.text, tweet.entities['urls'][0]['url']]  for tweet in tweets]
    print(attributes_container)
    # columns_name = ['created_at', 'user','screen_name', 'text', 'url']
    # df = pd.DataFrame(attributes_container, columns=columns_name)
    # print(df)
except BaseException as e:
    print('Status Failed On,',str(e))