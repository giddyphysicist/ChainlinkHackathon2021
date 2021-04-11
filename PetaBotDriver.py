# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 22:30:19 2021

Author: Giddy Physicist


PetaBotDriver.py

PETA-Bot Driver Module

Part of the PETA-Bot hackathon repo. This module is the main driving function 
for the project. By running the executePetaBotTasks, price query data will be 
stored and evaluated at the specified time interval. Default is every 30 minutes.

"""
import sched
import time

import twitterBot as TB
import dataStoreInterface as DSI



#Schedule Price Query at given frequency
s = sched.scheduler(time.time, time.sleep)


def executePetaBotTasks(scheduler=s, timePeriod=60*30, pricePercentageTweetThreshold=0.1):
    """
    Main PETA-Bot function for storing historical price query data. 
    
    Evaluates data points from DODO exchange and Chainlink price feeds (mainnet)
    to compare price quotes for 8 common currency pairs. 
    
    When the price advantage percentage for DODO is above the input threshold, 
    the function triggers the twitter bot to tweet out a price alert containing 
    the percentage price edge, the currency pair name, and the prices from 
    chainlink and DODO. 
    
    Once set up, this function will continue to schedule query events until 
    the function is stopped or an error is encountered.

    Parameters
    ----------
    scheduler : sched.scheduler
        task scheduler object for storing tasks in queue. The default is s 
        defined at top of this module.
    timePeriod : float, optional
        time period in seconds at which the PETA-Bot executes its main tasks. The default is 60*30, or 30 minutes.
    pricePercentageTweetThreshold : float, optional
        the percentage theshold above which the twitter bot will tweet the price
        advantage for DODO. The default is 0.1 (0.1%)

    Returns
    -------
    None.

    """
    location='file'
    dataRowDict = DSI.queryDataPoint()
    for pricePair,priceData in dataRowDict.items():
        database = DSI.loadDatabase(pricePair, location=location)
        newDatabase = DSI.appendDataRowToDatabase(priceData, database)
        DSI.pushDatabase(newDatabase,location=location,currencyPair=pricePair)
        #check if DODO has price advantage
        #if so, compose tweet.
        #######################################################################
        #### NOTE: I had to comment this section out, because Twitter froze this 
        #### account for violating its policies. I had already live-tweeted 
        #### quite a few instances of the DODO price edge, but until I head back
        #### from twitter support, I am unable to auto-tweet. :(
        #######################################################################
        # if priceData['dodoPriceEdgePercentage'] > pricePercentageTweetThreshold:
        #     try:
        #         TB.postPriceEdge(pricePair, 
        #                           priceData['dodoPriceEdgePercentage'], 
        #                           priceData['chainlinkPrice'], 
        #                           priceData['dodoPrice'])
        #         time.sleep(60) #wait 60 seconds between tweets to try not to violate twitter policy
        #     except:
        #         print(f'ERROR IN TRYING TO TWEET FOR {pricePair}')
        #######################################################################

    scheduler.enter(timePeriod,1,executePetaBotTasks,kwargs={"scheduler":scheduler,
                                                             "timePeriod":timePeriod,
                                                             "pricePercentageTweetThreshold":pricePercentageTweetThreshold})
    scheduler.run()

    

