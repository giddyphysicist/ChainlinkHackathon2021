# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 22:30:19 2021

Author: Giddy Physicist


PetaBotDriver.py

"""
import sched
import time

import twitterBot as TB
import dataStoreInterface as DSI



#Schedule Price Query at given frequency
s = sched.scheduler(time.time, time.sleep)


def executePetaBotTasks(scheduler=s, timePeriod=30*15, pricePercentageTweetThreshold=0.1):
    location='file'
    dataRowDict = DSI.queryDataPoint()
    for pricePair,priceData in dataRowDict.items():
        database = DSI.loadDatabase(pricePair, location=location)
        newDatabase = DSI.appendDataRowToDatabase(priceData, database)
        DSI.pushDatabase(newDatabase,location=location,currencyPair=pricePair)
        #push data to ipfs database
        #check if DODO has price advantage
        #if so, compose tweet.
        
        
        # if priceData['dodoPriceEdgePercentage'] > pricePercentageTweetThreshold:
        #     try:
        #         TB.postPriceEdge(pricePair, 
        #                          priceData['dodoPriceEdgePercentage'], 
        #                          priceData['chainlinkPrice'], 
        #                          priceData['dodoPrice'])
        #     except:
        #         print('ERROR IN TRYING TO TWEET')
                
                
    scheduler.enter(timePeriod,1,executePetaBotTasks,kwargs={"scheduler":scheduler,
                                                             "timePeriod":timePeriod,
                                                             "pricePercentageTweetThreshold":pricePercentageTweetThreshold})
    scheduler.run()

    

