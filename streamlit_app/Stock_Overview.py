import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
import streamlit as st
import plotly.express as px
import datetime
from time import strftime


########################################################################################################################
# Configuration, layout, and downloading data
########################################################################################################################
# Change page layout to wide
st.set_page_config(layout='wide')


# Pull a list of all stock tickers as of 1/6/2024
fpath = r'\stock_analysis3\stock_analysis3.xlsm'
sym_df = pd.read_excel(fpath, sheet_name='symbols')

########################################################################################################################
# Sidebar
########################################################################################################################
st.sidebar.title('Layout and Filters')
ticker = st.sidebar.multiselect('Select a ticker symbol',
                      sym_df['Symbol'].unique(),default='XOM')
ticker = ticker[0]
st.session_state['main_ticker'] = ticker
start_date = st.sidebar.date_input('Start Date',value=datetime.datetime(2020,1,1))
end_date = st.sidebar.date_input('End Date')
info = yf.Ticker(ticker).info
company_name = info['longName']
#st.markdown('Company Name:    {x}'.format(x = company_name))

########################################################################################################################
st.title('Stock Analysis   |   {ticker}   |   {name}'.format(ticker=ticker, name = company_name))
st.caption('The purpose of this site is to show data on stocks. You can select'
           ' which stocks you would like to see by changing the ticker on the sidebar. This site'
           ' was developed by Jared Heiner. ')
st.divider()

a = yf.Ticker(ticker).history(start=start_date, end=end_date)
b = a.reset_index()
b = b.rename(columns={'Close':'Close $ per Share'})
b['Date'] = b['Date'].dt.strftime('%Y-%m-%d')

col1, col2 = st.columns(2, gap='small')
with col1:
    fig = px.line(
        b,
        x=b['Date'],
        y=b['Close $ per Share'],
        title='Historical Stock Price',
        height=350
    )

    st.plotly_chart(fig, use_container_width=True)
    fig2 = px.line(
        b,
        x=b['Date'],
        y=b['Volume'],
        title='Historical Trading Volume',
        height=350,
    )

    st.plotly_chart(fig2, use_container_width=True)
with col2:
    st.subheader('Company Info')
    st.write('Legal Name:    {x}'.format(x=company_name))
    st.write('Industry:      {x}'.format(x=info['industry']))
    st.write('Website:       {x}'.format(x=info['website']))
    st.write('Audit Risk:    {x}'.format(x=info['auditRisk']))
    st.write('Board Risk:    {x}'.format(x=info['boardRisk']))
    st.write('Previous Close: ${x}'.format(x=info['previousClose']))
    st.write('Company Description:')
    st.write('{x}'.format(
        x = info['longBusinessSummary']
    ))
st.write('This site is powered by Straemlit and Python')



