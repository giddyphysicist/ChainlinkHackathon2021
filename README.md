# ChainlinkHackathon2021
#chainlink

PETA-Bot

Price Edge & Twitter Analysis Bot (PETA-Bot)

<p align="center">
  <img src="./img/PETA-Bot-logo.png"/>
</p>


This project was started for the chainlink 2021 hackathon as my first foray into ethereum, smart contracts, and chainlink.

![Project Comoponents Chart](./img/PETA-Bot_chart.png)

The code contains queries for generating price quotes from different exchanges, including DODO and chainlink data oracles. 

When there is a price advantage, the twitter bot will tweet out the currency pair and the price edge. 

Previous price data and opportunities will be tracked in an interactive dashboard, powered by streamlit.

![Streamlit Dashboard Example](./img/dashboard_example.PNG)

The project was written making use of 3rd party python libraries, including web3.py, tweepy.py, and streamlit.py.

I used web3.py to interact with the chainlink price feed smart contracts on the mainnet, and to query the midprice data using the DODO exchange smart contract on the mainnet. I used tweepy to interact with the twittert api, and I used the streamlit framework, along with some scipy statistics functions, as the bones for the historical data analytics dashboard app. The historical database is accessed using the python pandas dataframe objects, and for short term queries, is stored in local csv files. At longer term intervals, the historical data is backed up to the IPFS, under a constant IPNS name reference.

The main driving module is the PetaBotDriver.py. This module schedules price queries at a specified time interval (defaults to every 30 minutes). Once the price is queried for 8 different currency pairs on both the chainlink mainnet price feed, as well as on the DODO price feed, the data is appended to the historical price data database. 

Follow our [Twitter Bot](https://twitter.com/DodoPetaBot)!

Like the PETA-Bot Projects? Consider Donating ETH!

0x2263B05F52e30b84416EF4C6a060E966645Cc66e
