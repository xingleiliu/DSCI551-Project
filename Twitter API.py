# Import Libraries
from textblob import TextBlob
import sys
import tweepy
import preprocessor as p
import statistics
import requests
import json
# import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
# import nltk
# import pycountry
import re
import string
from typing import List
# from wordcloud import WordCloud, STOPWORDS
# from PIL import Image
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
# from langdetect import detect
# from nltk.stem import SnowballStemmer
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
# from sklearn.feature_extraction.text import CountVectorizer

consumer_key = "eTaweaYCyXZJCqbW9VGcTRR1u"
consumer_secret = "If8dXEW9L1nYgvJbbxZWjmdvn3UALYLgXceFiQFpRPQ6M1JKOK"

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)

data = {}

def get_tweets(keyword: str) -> List[str]:
    all_tweets = []
    for tweet in tweepy.Cursor(api.search_tweets, q=keyword, tweet_mode='extended', lang="en", result_type="popular").items(10):
        all_tweets.append(tweet.full_text)
    for i in range(len(all_tweets)):
        data[i] = {}
        key = 'tweet'
        data[i][key] = all_tweets[i]
    # print(data)
    return all_tweets

# print(get_tweets("USC"))

def clean_tweets(all_tweets: List[str]) -> List[str]:
    tweets_clean = []
    # for tweet in all_tweets:
    #     tweets_clean.append(p.clean(tweet))
    for i in range(len(all_tweets)):
        cleaned = p.clean(all_tweets[i])
        tweets_clean.append(cleaned.split())
    # print(tweets_clean)
    return tweets_clean
# print(clean_tweets(get_tweets("USC")))

def get_sentiment(all_tweets: List[List[str]]) -> List[List[float]]:
    sentiment_scores = []
    # for tweet in all_tweets:
    for i in range(len(all_tweets)):
        total = 0
        for y in range(len(all_tweets[i])):
            blob = TextBlob(all_tweets[i][y])
            score = blob.sentiment.polarity
            sentiment_scores.append(score)
            total += score
        # print(total)
        key = 'sentiment_scores'
        data[i][key] = total
    # print(data)
    return sentiment_scores

# print(get_sentiment(clean_tweets(get_tweets("USC"))))

def avg_sentiment(keyword: str) -> int:
    tweets = get_tweets(keyword)
    tweets_clean = clean_tweets(tweets)
    sentiment_scores = get_sentiment(tweets_clean)
    avg = sum(sentiment_scores) / len(tweets)
    return avg
# print(avg_sentiment("USC"))

if __name__ == "__main__":
    # print("two inputs")
    # first = input()
    # sec = input()
    # print()
    first = "USC"
    # sec = "UCLA"

    first_score = avg_sentiment(first)
    # sec_score = avg_sentiment(sec)

    data_tweet = {}
    data_tweet["Tweets"] = data
    data_tweet_json = json.dumps(data_tweet)
    print(data_tweet)
    requests.put(url="https://proj-aa3d9-default-rtdb.firebaseio.com/.json", json=data_tweet)
    # requests.put(url="https://dsci-551-9dfe8-default-rtdb.firebaseio.com/.json", json=data_tweet)
    # if (first_score > sec_score):
    #     print(f"{first} wins!{first_score}")
    # else:
    #     print(f"{sec} wins!{sec_score}")



