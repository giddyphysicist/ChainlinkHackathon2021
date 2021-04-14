# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 22:57:25 2021

Author: Giddy Physicist

Data Store Interface Module

Part of the PETA-Bot hackathon repo. This module is used to interact with the 
historical price data files. The interaction involves loading a database, 
querying for a new data row, appending the row to the database structure, and 
pushing the new database structure back into the file storage locaiton. 

There are two main locations for the database files:
    (1) local csv files
    (2) decentralized file server using IPFS


"""
import os
import subprocess
import pandas as pd
import time
import queryPriceData as QPD

def getIPNSurl():
    """
    return the URL to the fixed IPNS (named IPFS hash) where the directory is 
    stored containing the price history csv data for the analytics app.

    Returns
    -------
    ipnsDir : str
        string url to fixed IPNS location of slowly backed up price history data.

    """
    ipnsDir = r'https://gateway.ipfs.io/ipns/k51qzi5uqu5djuxohf4c5kj838m14tgygn1hrey2cmda0y2efzwu03w63em3qt/'
    return ipnsDir
    

def getStreamlitHostingUrl():
    """
    returns the hosting URL to the streamlit analytics app for price edge viewing.


    Returns
    -------
    streamlitHostingUrl : str
        hosting URL for streamlit analytics app.

    """
    streamlitHostingUrl = r'https://share.streamlit.io/giddyphysicist/chainlinkhackathon2021/main/analysisDashboard.py'
    return streamlitHostingUrl

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
    """
    extract historical price data for the specified currency pair name.
    Loads the data into a pandas dataframe object

    Parameters
    ----------
    currencyPair : str
        currency pair name string.
    location : TYPE, optional
        DESCRIPTION. The default is 'file'.

    Raises
    ------
    NotImplementedError
        DESCRIPTION.
    Exception
        DESCRIPTION.

    Returns
    -------
    df : pandas.core.frame.DataFrame
        Pandas dataframe object containing .

    """
    if location.lower()=='file':
        if not os.path.isdir('./data'):
            os.makedirs('./data')
        file = f'./data/{currencyPair}.csv'
        if not os.path.isfile(file):
            #pull from ipfs
            ipnsDir = getIPNSurl()
            ipnsFile = ipnsDir + f'{currencyPair}.csv'
            df = pd.read_csv(ipnsFile)
            df.to_csv(file,index=False)
        else:
            df = pd.read_csv(file)
    elif location.lower() =='ipfs':
        # raise NotImplementedError()
        try:
            ipnsDir = getIPNSurl()
            ipnsFile = ipnsDir + f'{currencyPair}.csv'
        except:
            print(f'WARNING -- COULD NOT EXTRACT {currencyPair} file from IFPS. Reverting to local file.')
            ipnsFile = f'./data/{currencyPair}.csv'
        df = pd.read_csv(ipnsFile)
    else:
        raise Exception('UNRECOGNIZED INPUT. LOCATION INPUT MUST SET TO "FILE" or "IPFS"')
    return df
    #implement IPFS database using IPNS name service or DNS mapping


def loadAllDatabases(location='file'):
    """
    Load Pandas dataframes for all currency pairs

    Parameters
    ----------
    location : TYPE, optional
        DESCRIPTION. The default is 'file'.

    Returns
    -------
    dfs : list<pandas.core.frame.DataFrame>
        List of pandas dataframes containing historical price data for each
        currency pair.

    """
    currencyPairs = QPD.getCurrencyPairs()
    dfs = []
    for currencyPair in currencyPairs:
        dfs.append(loadDatabase(currencyPair, location=location))
    return dfs

    
def appendDataRowToDatabase(dataRow, database):
    """
    Append a data row to the input pandas dataframe object, and return a new 
    dataframe object

    Parameters
    ----------
    dataRow : TYPE
        DESCRIPTION.
    database : TYPE
        DESCRIPTION.

    Returns
    -------
    df : TYPE
        DESCRIPTION.

    """
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
    



    