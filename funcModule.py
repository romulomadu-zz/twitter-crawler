#Module fof functions used on TrabalhoNoSql.ipynb

#imports
import string
from pymongo import MongoClient
from stopwords import allStopWords
import re
import tweepy
import datetime as dt
import json
from pandas import to_datetime
from pprint import pprint


def write_tweets(tweets, filename):
    ''' Function that appends tweets to a file. '''

    with open(filename, 'a') as f:
        for tweet in tweets:
            json.dump(tweet, f)
            f.write('\n')
        f.close()

def get_tweet_id(api, date='', days_ago=9, query='a'):
    ''' Function that gets the ID of a tweet. This ID can then be
        used as a 'starting point' from which to search. The query is
        required and has been set to a commonly used word by default.
        The variable 'days_ago' has been initialized to the maximum
        amount we are able to search back in time (9).'''

    if date:
        # return an ID from the start of the given day
        td = date + dt.timedelta(days=1)
        tweet_date = '{0}-{1:0>2}-{2:0>2}'.format(td.year, td.month, td.day)
        tweet = api.search(q=query, count=1, until=tweet_date)
    else:
        # return an ID from __ days ago
        td = dt.datetime.now() - dt.timedelta(days=days_ago)
        tweet_date = '{0}-{1:0>2}-{2:0>2}'.format(td.year, td.month, td.day)
        # get list of up to 10 tweets
        tweet = api.search(q=query, count=10, until=tweet_date)
        print('Search limit (start/stop):',to_datetime(tweet['statuses'][0]['created_at']))
        # return the id of the first tweet in the list
        return tweet['statuses'][0]['id']

#==============================================================================
# Function countWords
#==============================================================================
#Parameters type: string
#Output type: Dictionary

def countWords(text):
    dictofwords = dict()
    s = re.sub(r'\W+', ' ', text).lower().strip()
    words = list(filter(None,s.split(' ')))
    #print('counting tweet words..')
    for word in words:
        if word in allStopWords:
            continue
        if word in dictofwords:
            dictofwords[word]['count']+=1
        else:
            dictofwords[word] = dict()
            dictofwords[word]['count']=1
    #print('done.')
    return dictofwords

#==============================================================================
# Function makeSentimentDict
#==============================================================================
#Parameters type: None
#Output type: Dictionary

def makeSentimentDict():
    dictofwords = dict()
    fneg = open('negative.txt')
    for word in fneg:
        word = word.strip()
        if word not in dictofwords:
             dictofwords[word]='negative'
    
    fpos= open('positive.txt')
    for word in fpos:
        word = word.strip()
        if word not in dictofwords:
             dictofwords[word]='positive'    
    return dictofwords

#==============================================================================
# Function putSentiment
#==============================================================================
#Parameters type: Dictionary
#Output type: Dictionary

def putSentiment(text):
    sentdict = makeSentimentDict()
    dictofwords = countWords(text)
    #print('puting sentiment on tweet words..')
    for key,value in dictofwords.items():
        if key in sentdict:
            dictofwords[key]['sentiment'] = sentdict[key]
        else:
            dictofwords[key]['sentiment'] = None
    #print('done.')
    return dictofwords

#==============================================================================
# Function putSentiment
#==============================================================================
#Parameters type: Dictionary
#Output type: Boolean, Integer
def sentimentScore(text):
    dictofwords = putSentiment(text)
    score = 0
    #print('get sentiment reaction from tweet...')
    for key, value in dictofwords.items():
        if value['sentiment']=='positive':
            score += int(value['count'])
        elif value['sentiment']=='negative':
            score -= int(value['count'])
    if score > 0:
        sentiment = 1
    elif score == 0:
        sentiment = 0
    else:
        sentiment = -1
    #print('done.')
    return sentiment, abs(score)
#

#==============================================================================
# Function getFromMongo
#==============================================================================
#Parameters type: None
#Output type: Iterator of collection elements
def getFromMongo(config):
    client = MongoClient() 
    db = client[config['db_name']]
    collection = db.tweets
    collection_iterator = collection.find({},config['projection'])
    client.close()
    return collection_iterator