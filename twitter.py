# Import Libraries
from textblob import TextBlob
import sys
import tweepy
import preprocessor as p
import statistics
import requests
import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import nltk
import re
import string
from typing import List
from wordcloud import WordCloud, STOPWORDS
from PIL import Image

consumer_key = "eTaweaYCyXZJCqbW9VGcTRR1u"
consumer_secret = "If8dXEW9L1nYgvJbbxZWjmdvn3UALYLgXceFiQFpRPQ6M1JKOK"

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)

data = {}

def get_tweets(keyword: str) -> List[str]:
    all_tweets = []
    for tweet in tweepy.Cursor(api.search_tweets, q=keyword, tweet_mode='extended', lang="en", result_type="popular").items(100):
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

def inputs():
    list = []
    print("Please input two keywords:")
    first = input()
    list.append(first)
    sec = input()
    list.append(sec)
    print()
    return list

def wc(text, num):
    mask = np.array(Image.open("cloud.png"))
    stopwords = set(STOPWORDS)
    wc = WordCloud(background_color="white",
                  mask = mask,
                  max_words=3000,
                  stopwords=stopwords,
                  repeat=True)
    wc.generate(str(text))
    if num == 1:
        wc.to_file("wc1.png")
        path = "wc21.png"
        # display(Image.open(path))
        print("Word Cloud1 Saved Successfully")
    elif num == 2:
        wc.to_file("wc2.png")
        path = "wc2.png"
        # display(Image.open(path))
        print("Word Cloud2 Saved Successfully")
    else:
        wc.to_file("wc3.png")
        path = "wc3.png"
        # display(Image.open(path))
        print("Word Cloud3 Saved Successfully")

# print(wc(clean_tweets(get_tweets("USC")), 2))


def userData(input_json):
    # input_dict = json.dumps(input_json)
    input_list = list(input_json.values())
    for i in range(len(input_list)):
        data[i] = {}
        key = 'tweet'
        data[i][key] = input_list[i]
    input_clean = clean_tweets(input_list)
    input_scores = get_sentiment(input_clean)
    avg = sum(input_scores) / len(input_list)
    # wc(input_clean, 3)

    # output_json = json.dumps(data)
    return data, f"The average sentiment score is {avg}"


def main(first, sec):
    # first = "USC"
    # sec = "UCLA"
    # print(inputs())
    # keywords = inputs()
    # first = keywords[0]
    # sec = keywords[1]

    #####first keyword dict###########
    first_score = avg_sentiment(first)
    first_dict = {}
    first_dict[first] = data
    requests.put(url="https://proj-aa3d9-default-rtdb.firebaseio.com/.json", json=first_dict)
    # print(f"Number of tweets of the first keywords: {len(data)}")

    ####second keyword dict###########
    sec_dict = {}
    sec_score = avg_sentiment(sec)
    sec_dict[sec] = data
    requests.patch(url="https://proj-aa3d9-default-rtdb.firebaseio.com/.json", json=sec_dict)
    # print(f"Number of tweets of the second keywords: {len(data)}")
    # print(sec_dict)

    ########plot wordcloud#######
    # wc(clean_tweets(get_tweets(first)), 1)
    # wc(clean_tweets(get_tweets(sec)), 2)

    ########print winner############
    if (first_score > sec_score):
        return (f"{first} wins! Sentiment score is {first_score}, the other is {sec_score}")
    else:
        return (f"{sec} wins! Sentiment score is {sec_score}, the other is {first_score}")


if __name__ == "__main__":
    print(main("USC", "UCLA"))



