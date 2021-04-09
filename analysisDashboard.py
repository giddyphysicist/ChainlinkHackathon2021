# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 22:07:27 2021

Author: Giddy Physicist

analysisDashboard.py
"""

import streamlit as st
import pandas as pd

import dataStoreInterface as DSI

#breakout by currency pair
#show line plot of price advantages at specific interval

#show histogram for price advantage

#filter on price percentage threshold (histogram and line chart vs time)


#load all databases

import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy.stats as stats
import altair as alt
import datetime

# path = r'C:/Users/pgartland/Desktop/bcdata'
path = r'./data'

dfs = [pd.read_csv(os.path.join(path,x)) for x in os.listdir(path)]

updateTime = datetime.datetime.now()


def priceLineChart(df):
    #time series chart
    #histogram (shaded +/-)
    currencyPair = df.currencyPair[0]
    sns.jointplot(x=df.queryTimestamp-np.min(df.queryTimestamp),
                  y=df.dodoPriceEdgePercentage,
                  hue=df.currencyPair)
    fig = plt.gcf()
    fig.delaxes(fig.axes[1])
    fig.axes[0].get_legend().remove()
    ax = fig.axes[0]
    xlims = ax.get_xlim()
    ylims = ax.get_ylim()
    ax.fill_between(xlims, 0, np.max([0,*ylims]),color='green',alpha=0.1,zorder=-10)
    ax.fill_between(xlims, 0, np.min([0,*ylims]),color='red',alpha=0.1,zorder=-10)
    ax.plot(xlims,[0,0],color='black',linewidth=3)
    ax.grid(True)
    ax.set_title(currencyPair)
   
    # ax2 = fig.axes[-1]
    # xlims2 = ax2.get_xlim()
    # ylims2 = ax2.get_ylim()
    # ax2.plot(max(ylims)*np.ones(2,),[0,0],color='black')
    pe = df.dodoPriceEdgePercentage
    pe25, pe75 = np.percentile(pe,[25,75])
    peMin = np.min(pe)
    peMax = np.max(pe)
    peMean = np.mean(pe)
    # pricesChart(df)
    return fig, peMin, peMax, pe25, pe75, peMean
    # raise NotImplementedError


def pricesChart(df):
    df['time'] = [datetime.datetime.fromtimestamp(x) for x in df.queryTimestamp.values]
    data = df
    ylims = (min([data['dodoPrice'].min(),data['chainlinkPrice'].min()]),
             max([data['dodoPrice'].max(),data['chainlinkPrice'].max()]))
    dodoChart = alt.Chart(data).mark_point(color='#fffe7a').encode(
    alt.X('time:T',
          axis=alt.Axis(title='Data Query Time',titleFontWeight=500,titleFontSize=15)),
    alt.Y('dodoPrice:Q',
          scale=alt.Scale(domain=ylims),
          axis=alt.Axis(title="$ Price (DODO=yellow, Chainlink=blue)",titleFontWeight=500,titleFontSize=14))
    ).interactive()
    
    chainlinkChart = alt.Chart(data).mark_point(color='#93CAED').encode(
    alt.X('time:T',
          axis=alt.Axis(title='')),
    alt.Y('chainlinkPrice:Q',
          scale=alt.Scale(domain=ylims),
          axis=alt.Axis(title=''))
    ).interactive()
    return dodoChart + chainlinkChart

def altairEdgePercentageHistoram(df):
    source = pd.DataFrame()
    currentEdge = df.dodoPriceEdgePercentage.values[-1]
    verticals = pd.DataFrame([{"zero": 0, "currentEdge":currentEdge}])
    yy = df.dodoPriceEdgePercentage
    x = np.linspace(np.min(yy),np.max(yy),200)
    y = stats.gaussian_kde(yy)(x)
    maxmag = np.max(np.abs(yy))
    xlims = (-maxmag,maxmag)
    source['percentEdge'] = x
    source['kdeWeight'] = y
   
    histPos = alt.Chart(source).transform_filter(
        alt.datum.percentEdge>=0).mark_area(
    line={'color':'darkgreen'},
    color=alt.Gradient(
        gradient='linear',
        stops=[alt.GradientStop(color='lightGreen', offset=0),
               alt.GradientStop(color='darkGreen', offset=1)],
        x1=1,
        x2=1,
        y1=1,
        y2=0
    )
    ).encode(
    alt.X('percentEdge:Q',
          scale=alt.Scale(domain=xlims)),
    alt.Y('kdeWeight:Q')
    ).interactive()
       
       
    histNeg = alt.Chart(source).transform_filter(
        alt.datum.percentEdge<0).mark_area(
    line={'color':'#8b0000'},
    color=alt.Gradient(
        gradient='linear',
        stops=[alt.GradientStop(color='#E6676B', offset=0),
               alt.GradientStop(color='#8b0000', offset=1)],
        x1=1,
        x2=1,
        y1=1,
        y2=0
    )
    ).encode(
    alt.X('percentEdge:Q',
          axis=alt.Axis(title="DODO % Price Edge",titleFontWeight=500,titleFontSize=20),
          scale=alt.Scale(domain=xlims)),
    alt.Y('kdeWeight:Q',axis=alt.Axis(title="historical weight",labels=False,titleFontWeight=500,titleFontSize=20))
    ).interactive()
   
       
    zeroRule = alt.Chart(verticals).mark_rule(color="white").encode(
            alt.X("zero:Q",axis=alt.Axis(title='')))
    currentEdgeRule = alt.Chart(verticals).mark_rule(color="yellow").encode(
            alt.X("currentEdge:Q",axis=alt.Axis(title=''))).interactive()
    chart = (zeroRule + currentEdgeRule + histNeg + histPos).interactive()
    return chart

################################################################
#PAGE LAYOUT:

st.set_page_config(page_title='PETA-Bot Dashboard',
                          page_icon=None,
                          layout='centered',
                          initial_sidebar_state='auto')

st.beta_container()
st.title('PETA-BOT Analysis Dashboard')
st.text('Price Edge & Twitter Analysis Bot')
st.markdown('Check us out on [Github](https://github.com/giddyphysicist/ChainlinkHackathon2021)!')
st.markdown('Follow our Alert Bot on [Twitter](https://twitter.com/DodoPetaBot)!')

st.markdown('---')

aboutExpander = st.beta_expander("About Us")
with aboutExpander:
    st.markdown('The Price Edge & Twitter Analysis Bot (PETA-Bot) was developed during the 2021 Chainlink Hackathon.')
    st.markdown('The PETA-Bot Project consists of two main components: a twitter bot and an analysis dashboard. Both components use the smart contract price feeds supplied by DODO and Chainlink for mainnet price comparisons between the exhanges. When the DODO exchange has a better midprice than the price quoted in chainlink, the twitter bot announces the percentage advantage in a tweet.')
    st.image('./img/PETA-Bot_chart.png')

st.markdown('---')
st.text(f"Data Updated {updateTime}")
ecol1,ecol2 = st.beta_columns(2)
with ecol1:
    st.info('Positive edge : DODO has a lower price')
    displayPositiveEdge = st.checkbox('Show Only Positive Edge')

with ecol2:
    st.info('Negative edge : Chainlink has a lower price')
st.markdown('---')
cp2ce = {df.currencyPair[0]:df.dodoPriceEdgePercentage.values[-1] for df in dfs}
cp2display = {k:(not displayPositiveEdge or cp2ce[k]>0) for k in cp2ce}
cp2df = {df.currencyPair[0]:df for df in dfs}
for currencyPair,df in cp2df.items():
    # currentEdge = df.dodoPriceEdgePercentage.values[-1]
    currentEdge = cp2ce[currencyPair]
    if cp2display[currencyPair]:
        col1, col2 = st.beta_columns(2)
        currencyPair = df.currencyPair[0]
        col1.header(currencyPair)
        fig, peMin, peMax, pe25, pe75,peMean = priceLineChart(df)
        lastQueryTime = datetime.datetime.fromtimestamp(np.max(df["queryTimestamp"]))
       
        if currentEdge > 0:
            col2.success(f"Current Edge for {currencyPair}: {currentEdge:.3f} %")
            col2.text(f'Last Query Time: {lastQueryTime}')
        else:
            col2.error(f"Current Edge for {currencyPair}: {currentEdge:.3f} %")
            col2.text(f'Last Query Time: {lastQueryTime}')
        # st.pyplot(fig)
        expander = st.beta_expander(f"Historical Stats for {currencyPair}")
        # clicked = expander.button('Historical Stats')
        with expander:
            expcol1, expcol2 = st.beta_columns(2)
            with expcol1:
                st.info(f'Average Historical Edge: {peMean:.3f} %')
                st.info(f'Minimum Historical Edge: {peMin:.3f} %')
                st.info(f'Maximum Historical Edge: {peMax:.3f} %')
            with expcol2:
                st.altair_chart(altairEdgePercentageHistoram(df))
            pc = pricesChart(df)
            st.altair_chart(pc,use_container_width=True)
        st.markdown(' ')
        st.markdown(' ')
        st.markdown('---')
footerCol1,footerCol2 = st.beta_columns(2)
with footerCol1:
    st.markdown('Check us out on [Github](https://github.com/giddyphysicist/ChainlinkHackathon2021)!')
with footerCol2:
    st.markdown('Follow our Alert Bot on [Twitter](https://twitter.com/DodoPetaBot)!')
    # st.text(f'25th perc.: {pe25:.3f} %')
    # st.text(f'75th perc.: {pe75:.3f} %')
   

