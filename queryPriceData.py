# -*- coding: utf-8 -*-
"""
PETA-Bot Module for collecting Price Data

Assumes that at one directory level above current one, there is a 
json file containing the INFURA data endpoints for your account.

Created on Tue Mar 23 21:29:25 2021

Author: Patrick Gartland

"""


from web3 import Web3 
import json


eth_usd_addr = '0x9326BFA02ADD2366b30bacB125260Af641031331'

main_eth_usd_addr = '0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419'

def getEndpoint(chain='mainnet'):
    """
    Extracts the infura endpoint website given the input chain name from among
    the possible values:
        mainnet
        kovan
        rinkeby
        goerli
        ropsten

    Parameters
    ----------
    chain : str, optional
        DESCRIPTION. The default is 'mainnet'.

    Raises
    ------
    ValueError
        DESCRIPTION.

    Returns
    -------
    endpoint : str
        url to endpoint for specified chain.

    """
    with open('../secretInfuraCredentials.json','r') as file:
        INFURA_CREDENTIALS = json.load(file)
    try:
        endpoint = INFURA_CREDENTIALS[f'{chain.upper()}_ENDPOINT']
    except:
        raise ValueError(f'COULD NOT FIND ENDPOINT FOR SPECIFIED CHAIN: {chain.upper()}')
    return endpoint


def getPriceData(chain="kovan", addr=''):
    endpoint = getEndpoint(chain)
    web3 = Web3(Web3.HTTPProvider(endpoint))
    abi = '[{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"description","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint80","name":"_roundId","type":"uint80"}],"name":"getRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"latestRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"version","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

   
    contract = web3.eth.contract(address=addr, abi=abi)
    data = contract.functions.latestRoundData().call()
    
    print(data[1]/1E8)
    return data[1]/1E8


def getDodoPriceData(currencyPair, chain='mainnet'):
    """
    Pulls DODO price data for midprice, expected target, and oracle price for 
    the given input currency pair.

    Parameters
    ----------
    currencyPair : str
        DESCRIPTION.
    chain : str, optional
        DESCRIPTION. The default is 'mainnet'.

    Raises
    ------
    ValueError
        DESCRIPTION.

    Returns
    -------
    dict
        dictionary containing keys for midprice, expectedTarget, and oraclePrice
        as calculated from contract for DODO exchange.

    """
    abi = '[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"buyer","type":"address"},{"indexed":false,"internalType":"uint256","name":"receiveBase","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"payQuote","type":"uint256"}],"name":"BuyBaseToken","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"maintainer","type":"address"},{"indexed":false,"internalType":"bool","name":"isBaseToken","type":"bool"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"ChargeMaintainerFee","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"payer","type":"address"},{"indexed":false,"internalType":"bool","name":"isBaseToken","type":"bool"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"ChargePenalty","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"baseTokenAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"quoteTokenAmount","type":"uint256"}],"name":"ClaimAssets","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"payer","type":"address"},{"indexed":true,"internalType":"address","name":"receiver","type":"address"},{"indexed":false,"internalType":"bool","name":"isBaseToken","type":"bool"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"lpTokenAmount","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"bool","name":"isBaseToken","type":"bool"}],"name":"Donate","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferPrepared","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"seller","type":"address"},{"indexed":false,"internalType":"uint256","name":"payBase","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"receiveQuote","type":"uint256"}],"name":"SellBaseToken","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"oldGasPriceLimit","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"newGasPriceLimit","type":"uint256"}],"name":"UpdateGasPriceLimit","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"oldK","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"newK","type":"uint256"}],"name":"UpdateK","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"oldLiquidityProviderFeeRate","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"newLiquidityProviderFeeRate","type":"uint256"}],"name":"UpdateLiquidityProviderFeeRate","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"oldMaintainerFeeRate","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"newMaintainerFeeRate","type":"uint256"}],"name":"UpdateMaintainerFeeRate","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"payer","type":"address"},{"indexed":true,"internalType":"address","name":"receiver","type":"address"},{"indexed":false,"internalType":"bool","name":"isBaseToken","type":"bool"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"lpTokenAmount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"_BASE_BALANCE_","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_BASE_CAPITAL_RECEIVE_QUOTE_","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_BASE_CAPITAL_TOKEN_","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_BASE_TOKEN_","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"_CLAIMED_","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_CLOSED_","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_DEPOSIT_BASE_ALLOWED_","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_DEPOSIT_QUOTE_ALLOWED_","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_GAS_PRICE_LIMIT_","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_K_","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_LP_FEE_RATE_","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_MAINTAINER_","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_MT_FEE_RATE_","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_NEW_OWNER_","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_ORACLE_","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_OWNER_","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_QUOTE_BALANCE_","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_QUOTE_CAPITAL_RECEIVE_BASE_","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_QUOTE_CAPITAL_TOKEN_","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_QUOTE_TOKEN_","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_R_STATUS_","outputs":[{"internalType":"enum Types.RStatus","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_SUPERVISOR_","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_TARGET_BASE_TOKEN_AMOUNT_","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_TARGET_QUOTE_TOKEN_AMOUNT_","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_TRADE_ALLOWED_","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"maxPayQuote","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"buyBaseToken","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"claimAssets","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"claimOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"depositBase","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"depositBaseTo","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"depositQuote","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"depositQuoteTo","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"disableBaseDeposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"disableQuoteDeposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"disableTrading","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"donateBaseToken","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"donateQuoteToken","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"enableBaseDeposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"enableQuoteDeposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"enableTrading","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"finalSettlement","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"lp","type":"address"}],"name":"getBaseCapitalBalanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getExpectedTarget","outputs":[{"internalType":"uint256","name":"baseTarget","type":"uint256"},{"internalType":"uint256","name":"quoteTarget","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"lp","type":"address"}],"name":"getLpBaseBalance","outputs":[{"internalType":"uint256","name":"lpBalance","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"lp","type":"address"}],"name":"getLpQuoteBalance","outputs":[{"internalType":"uint256","name":"lpBalance","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getMidPrice","outputs":[{"internalType":"uint256","name":"midPrice","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getOraclePrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"lp","type":"address"}],"name":"getQuoteCapitalBalanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getTotalBaseCapital","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getTotalQuoteCapital","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"getWithdrawBasePenalty","outputs":[{"internalType":"uint256","name":"penalty","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"getWithdrawQuotePenalty","outputs":[{"internalType":"uint256","name":"penalty","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"supervisor","type":"address"},{"internalType":"address","name":"maintainer","type":"address"},{"internalType":"address","name":"baseToken","type":"address"},{"internalType":"address","name":"quoteToken","type":"address"},{"internalType":"address","name":"oracle","type":"address"},{"internalType":"uint256","name":"lpFeeRate","type":"uint256"},{"internalType":"uint256","name":"mtFeeRate","type":"uint256"},{"internalType":"uint256","name":"k","type":"uint256"},{"internalType":"uint256","name":"gasPriceLimit","type":"uint256"}],"name":"init","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"queryBuyBaseToken","outputs":[{"internalType":"uint256","name":"payQuote","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"querySellBaseToken","outputs":[{"internalType":"uint256","name":"receiveQuote","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"retrieve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"minReceiveQuote","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"sellBaseToken","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"newGasPriceLimit","type":"uint256"}],"name":"setGasPriceLimit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"newK","type":"uint256"}],"name":"setK","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"newLiquidityPorviderFeeRate","type":"uint256"}],"name":"setLiquidityProviderFeeRate","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newMaintainer","type":"address"}],"name":"setMaintainer","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"newMaintainerFeeRate","type":"uint256"}],"name":"setMaintainerFeeRate","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOracle","type":"address"}],"name":"setOracle","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newSupervisor","type":"address"}],"name":"setSupervisor","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"version","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"withdrawAllBase","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"withdrawAllBaseTo","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"withdrawAllQuote","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"withdrawAllQuoteTo","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"withdrawBase","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"withdrawBaseTo","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"withdrawQuote","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"withdrawQuoteTo","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"}]'
    endpoint = getEndpoint(chain)
    web3 = Web3(Web3.HTTPProvider(endpoint))
    dodoAddresses = {'DODO Pair: WETH-USDC':'0x75c23271661d9d143dcb617222bc4bec783eff34',
                     'DODO Pair: LINK-USDC':'0x562c0b218cc9ba06d9eb42f3aef54c54cc5a4650',
                     'DODO Pair: LEND-USDC':'0xc226118fcd120634400ce228d61e1538fb21755f',
                     'DODO Pair: AAVE-USDC':'0x94512fd4fb4feb63a6c0f4bedecc4a00ee260528',
                     'DODO Pair: SNX-USDC':'0xca7b0632bd0e646b0f823927d3d2e61b00fe4d80',
                     'DODO Pair: COMP-USDC':'0x0d04146b2fe5d267629a7eb341fb4388dcdbd22f',
                     'DODO Pair: WBTC-USDC':'0x2109f78b46a789125598f5ad2b7f243751c2934d',
                     'DODO Pair: YFI-USDC':'0x1b7902a66f133d899130bf44d7d879da89913b2e',
                     'DODO Pair: FIN-USDT':'0x9d9793e1e18cdee6cf63818315d55244f73ec006',
                     'DODO Pair: USDT-USDC':'0xC9f93163c99695c6526b799EbcA2207Fdf7D61aD',
                     'DODO Pair: WOO-USDT':'0x181d93ea28023bf40c8bb94796c55138719803b4',
                     'DODO Pair: wCRES-USDT':'0x85f9569b69083c3e6aeffd301bb2c65606b5d575'}
    key = [k for k in dodoAddresses if currencyPair.upper() in k]
    if not key:
        raise ValueError(f"COULD NOT FIND ADDRESS FOR CURRENCY PAIR {currencyPair.upper}")
    addr = web3.toChecksumAddress(dodoAddresses[key[0]])
    contract = web3.eth.contract(address=addr, abi=abi)
    midprice = contract.functions.getMidPrice().call()
    expectedTarget = contract.functions.getExpectedTarget().call()[1]
    oraclePrice = contract.functions.getOraclePrice().call()
    return {'midprice':midprice,
            'expectedTarget':expectedTarget,
            'oraclePrice':oraclePrice}


def getChainlinkPriceData(currencyPair, chain='mainnet'):
    abi = '[{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"description","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint80","name":"_roundId","type":"uint80"}],"name":"getRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"latestRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"version","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'
    