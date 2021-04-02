# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 22:57:25 2021

Author: Giddy Physicist


"""


import pandas as pd

import time

import queryPriceData as QPD




def queryDataPoint():
    result = QPD.queryAllPricesDodoAndChainlink(chain='mainnet')
    # queryTime = datetime.datetime.now().timestamp()
    queryTime = time.time()
    dataRowDict = {}
    for pair in result:
        pairData = result[pair]
        dataRow = {'queryTimestamp':queryTime,
                    'dodoPriceEdgePercentage':(pairData['chainlinkPrice'] - pairData['dodoPrice'])/(0.5*(pairData['chainlinkPrice']+pairData['dodoPrice']))*100,
                    'timeLag':queryTime - pairData['chainlinkTimestamp'],
                    'chainlinkTimestamp':pairData['chainlinkTimestamp'],
                    'dodoPrice':pairData['dodoPrice'],
                    'chainlinkPrice':pairData['chainlinkPrice'],
                    'currencyPair':pair
                    }
                           
        dataRowDict[pair] = dataRow
    return dataRowDict


def loadDatabase(currencyPair, location='file'):
    if location.lower()=='file':
        df = pd.read_csv(f'./data/{currencyPair}.csv')
    elif location.lower() =='ipfs':
        raise NotImplementedError()
        df = pd.read_csv('<IPFS ADDRESS HERE>')
    else:
        raise Exception('UNRECOGNIZED INPUT. LOCATION INPUT MUST SET TO "FILE" or "IPFS"')
    return df
    #implement IPFS database using IPNS name service or DNS mapping
    

def appendDataRowToDatabase(dataRow, database):
    df = database.append(dataRow,ignore_index=True)
    return df

    
def pushDatabase(database,location='file',currencyPair=None):
    if location.lower()=='file':
        if currencyPair is None:
            currencyPair = database.currencyPair.unique().tolist()[0]
        database.to_csv(f'./data/{currencyPair}.csv',index=False)
        return
    elif location.lower()=='ipfs':
        #PUSH UPDATED DATABASE TO IPFS
        #implement IPFS
        raise NotImplementedError()
        pass
    else:
        raise Exception('UNRECOGNIZED INPUT. LOCATION INPUT MUST SET TO "FILE" or "IPFS"')
    