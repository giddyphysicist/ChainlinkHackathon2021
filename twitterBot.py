# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 20:18:10 2021

Author: Giddy Physicist


"""
import tweepy
import json


def getTwitterApi():
    with open('../secretTwitterCredentials.json','r') as file:
        TWITTER_CREDENTIALS = json.load(file)
    auth = tweepy.OAuthHandler(TWITTER_CREDENTIALS['APP_KEY'], TWITTER_CREDENTIALS['APP_SECRET'])
    auth.set_access_token(TWITTER_CREDENTIALS['OAUTH_TOKEN'], TWITTER_CREDENTIALS['OAUTH_TOKEN_SECRET'])
    api = tweepy.API(auth)
    return api


def postTweet(tweetText="Test Tweet"):
    api = getTwitterApi()
    api.update_status(status=tweetText)
    

def postPriceEdge(currencyPair, percentage, chainlinkPrice, dodoPrice):
    tweetText = '\n'.join([f"🚨 PRICE EDGE DETECTED FOR {currencyPair}! 🚨",
                           f"{percentage:.3f}% better price for DODO",
                           f"chainlink price: {chainlinkPrice:.8f}",
                           f"dodo price: {dodoPrice:.8f}"])
    postTweet(tweetText=tweetText)
        
    # print(tweetText)
    # print(len(tweetText))
'''
Twitter Price Bot and Analysis Dashboard

'''

