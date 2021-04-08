import time
from sqlalchemy import create_engine
import logging
import requests
import pandas as pd
import config

#create connection to postgres
pg = create_engine('postgres://docker_postgres:postgres@postgresdb:5432/tweets_db', echo=True)
webhook_url = config.webhook_url


time.sleep(5)

while True:
    logging.critical("\n\n new tweet tweeted :\n")
    tweet_query = '''
    SELECT text,tweeter_user,user_image_URL,sentiment FROM tweets_table ORDER BY sentiment LIMIT(1)
    '''
    df=pd.read_sql(tweet_query,con=pg)
    tweet=df['text'][0]
    user=df['tweeter_user'][0]
    sentiment=df['sentiment'][0]
    user_image_url=df['user_image_url'][0]
    #logging.critical( tweet + "\n")
    output = f'New tweet has been already tweeted! \n from @{user}: {tweet} \n The sentiment score of the tweet is: {sentiment}'

    #data = {'text': output}
    data = {'blocks': [{
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{user}* \n {tweet} \n\n The sentiment score of the tweet is: {sentiment}"
            },
            "accessory": {
                "type": "image",
                "image_url":f"{user_image_url}",
                "alt_text": "alt text for image"
            }
        }]
    }

    logging.critical(user_image_url)

    requests.post(url=webhook_url, json=data)

    time.sleep(300)

    