import pymongo
import time
from sqlalchemy import create_engine
import os
import logging
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 

time.sleep(20)

# Establish a connection to the MongoDB server
client = pymongo.MongoClient("mongodb")
#create connection to postgres
pg = create_engine('postgres://docker_postgres:postgres@postgresdb:5432/tweets_db', echo=True)
# Select the database you want to use within the MongoDB server
db = client.tweets
# Select the collection of documents you want to use withing the MongoDB database
collection = db.tweet_info

#create table
create_table_query='''
     CREATE TABLE IF NOT EXISTS tweets_table(
             id VARCHAR(50),
             tweet_created_at DATE,
             text TEXT,
             tweeter_user VARCHAR(1024) ,
             source VARCHAR(1024),
             language VARCHAR(10),
             user_description TEXT,
             num_followers INT,
             user_statuses INT,
             user_created_at DATE,
             hashtags TEXT,
             tweet_location VARCHAR(1024),
             user_location VARCHAR(1024),
             user_image_URL text,
             sentiment NUMERIC
     );

'''
pg.execute(create_table_query)


#extract
def extract_tweets():
        tweets = list(collection.find())
        return tweets

# transform tweets with Sentiment analysis
def transform_tweets(tweets):
        s  = SentimentIntensityAnalyzer()
        for tweet in tweets:
                text =tweet['text']
                # calculate sentiment
                score = s.polarity_scores(text)
                sentiment=score['compound']
                tweet.update({'sentiment': sentiment})
        return tweets


def load_tweets(tweets):
        logging.critical("inside load")
        for e in tweets:
                logging.critical("inside for")
                id =e['id']
                tweet_created_at=e['tweet_created_at']
                text =e['text']
                tweeter_user= e['user']
                source= e['source']
                language=e['language']
                user_description =e['user_description']
                num_followers =e['num_followers']
                user_statuses=e['user_statuses']
                user_created_at =e['user_created_at']
                hashtags =e['hashtags']
                tweet_location=e['tweet_location']
                user_location=e['user_location']
                user_image_url=e['user_image_URL']
                sentiment=e['sentiment']

                query = "INSERT INTO tweets_table VALUES (%s, %s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s, %s,%s, %s);"
                pg.execute(query, (id,tweet_created_at,text,tweeter_user,source,language,user_description,
                                        num_followers,user_statuses,user_created_at,hashtags,tweet_location,
                                        user_location,user_image_url,sentiment))

                logging.critical(f'Tweet {id}  loaded into Postgres.')

                

logging.critical("Starting ETL job")
while True:
        tweets = extract_tweets()
        if tweets:
                tweets = transform_tweets(tweets)
                load_tweets(tweets)
        time.sleep(50)