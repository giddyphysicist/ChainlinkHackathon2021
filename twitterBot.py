# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 20:18:10 2021

Author: Patrick Gartland


"""
import tweepy
import json


def getTwitterApi():
    with open('../secretTwitterEnvKeys.json','r') as file:
        TWITTER_CREDENTIALS = json.load(file)
    auth = tweepy.OAuthHandler(TWITTER_CREDENTIALS['APP_KEY'], TWITTER_CREDENTIALS['APP_SECRET'])
    auth.set_access_token(TWITTER_CREDENTIALS['OAUTH_TOKEN'], TWITTER_CREDENTIALS['OAUTH_TOKEN_SECRET'])
    api = tweepy.API(auth)
    return api

def tweet():
    pass


'''
Twitter Price Bot and Analysis Dashboard

'''

