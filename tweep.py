import tweepy
import pandas as pd
from config.db import collentionlistim,collectionportal
import datetime
from datetime import datetime, timedelta,date
from dateutil import tz

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
    hoy = date.today()
    dia_anterior = hoy - timedelta(days=1)
    fecha_anterior_str = dia_anterior.strftime("%Y-%m-%d")
    query = "({}) until:{} -filter:retweets".format(" OR ".join(search_query), fecha_anterior_str)
    # Realizar la búsqueda en la API de Twitter
    tweets = api.search_tweets(q=query, count=no_of_tweets, hidden=True, geocode=geo)
    tweets_list = []
    for tweet in tweets:
        created_a = tweet.created_at
        created_a = tweet.created_at
        created_at = created_a.strftime("%d/%m/%Y")
        user = tweet.user.screen_name
        text = tweet.text
        imagen = tweet.entities['media'][0]['media_url'] if 'media' in tweet.entities and len(tweet.entities['media']) > 0 else None

        if imagen is None:
            imagen = 'https://3.bp.blogspot.com/-XiSlfYYT_FM/WN_SwvPLrrI/AAAAAAAAAE0/eNNfi9x0Qpwot3fT3u-h12DxsU4M927QQCLcB/s320/Twitter_logo_2012.svg.png'
        
        null = None
        
        url = tweet.entities['urls'][0]['url'] if 'urls' in tweet.entities and len(tweet.entities['urls']) > 0 else None
        tweet_dict = {'fecha': created_at, 'name': user, 'Titulo': text, 'video': null, 'fuente': 'twitter', 'status': 'Pendiente', 'imagen': imagen,'longitude':23232,'latitude':232343,'clasificacion': 'Violencia de Género','descripcion': 'Violencia de Género','Lastname':'','url':url}
        tweets_list.append(tweet_dict)
    columns_name = ['fecha', 'name', 'Titulo', 'video', 'fuente', 'status', 'imagen','longitude','latitude','clasificacion','descripcion','Lastname']
    df = pd.DataFrame(tweets_list, columns=columns_name)
    df['fecha'] = pd.to_datetime(df['fecha'], format="%d/%m/%Y").dt.strftime("%d/%m/%Y")
    # print(df)
    
    for frame in df.to_dict('records'):
        try:
            collectionportal.insert_one(frame)
            # pruba.insert_one(frame)
        except BaseException as e:
            print('Status Failed On,', str(frame))

except BaseException as e:
    print('Status Failed On,', str(e))