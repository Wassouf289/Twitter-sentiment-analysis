# Twitter-sentiment-analysis

<img src="images/structure.svg">

This project aims to build a Dockerized Data Pipeline that analyzes the sentiment of tweets. It consists of five components :
1- collects the tweets with a specific tag (for example I used "berlin").
2- stores the tweets in a Mongo database.
3- an ETL job that read the tweets from Mongo DB and computes the sentiment for the tweet with vaderSentiment.
VADER (Valence Aware Dictionary and sEntiment Reasoner) is a lexicon and rule-based sentiment analysis tool that is specifically attuned to sentiments expressed in social media.
4- stores the tweets with their accordings sentiment into a Postgres database.
5- a slack bot that will post a tweet with its sentiment every period of time.
Each component will run in a separate docker container, managed by docker-compose file (docker-compose.yml).
