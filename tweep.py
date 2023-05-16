import tweepy
import pandas as pd
from config.db import collentionlistim
import datetime

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


search_query = ['amenaza','violencia','agresión','víctima','abuso']
no_of_tweets = 1000
geo = '18.7009,-70.16546,100km'


try:
    hoy = datetime.date.today()
    dia_anterior = hoy - datetime.timedelta(days=1)
    fecha_anterior_str = dia_anterior.strftime("%Y-%m-%d")
    query = "({}) until:{} -filter:retweets".format(" OR ".join(search_query), fecha_anterior_str)
    # Realizar la búsqueda en la API de Twitter
    tweets = api.search_tweets(q=query, count=no_of_tweets, hidden=True, geocode=geo)
    tweets_list = []
    for tweet in tweets:
        created_at = tweet.created_at
        user = tweet.user.screen_name
        text = tweet.text
        imagen = tweet.entities['media'][0]['media_url'] if 'media' in tweet.entities and len(tweet.entities['media']) > 0 else None

        if imagen is None:
            imagen = 'https://es.wikipedia.org/wiki/Twitter#/media/Archivo:Logo_of_Twitter.svg'
        
    

        url = tweet.entities['urls'][0]['url'] if 'urls' in tweet.entities and len(tweet.entities['urls']) > 0 else None
        tweet_dict = {'fecha': created_at, 'owner_username': user, 'Nombre': text, 'video': url, 'fuente': 'twitter', 'status': 'Pendiente', 'imagen': imagen}
        tweets_list.append(tweet_dict)
    columns_name = ['fecha', 'owner_username', 'Nombre', 'video', 'fuente', 'status', 'imagen']
    df = pd.DataFrame(tweets_list, columns=columns_name)
    
    for frame in df.to_dict('records'):
        try:
            collentionlistim.insert_one(frame)
            # pruba.insert_one(frame)
        except BaseException as e:
            print('Status Failed On,', str(frame))

except BaseException as e:
    print('Status Failed On,', str(e))