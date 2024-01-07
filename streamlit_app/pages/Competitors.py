import yfinance as yf
import streamlit as st
import plotly.express as px
import datetime
import pandas as pd
from time import strftime, localtime

st.set_page_config(layout='wide')

fpath = r'D:\Excel_Stock_Analysis\stock_analysis3\stock_analysis3.xlsm'
sym_df = pd.read_excel(fpath, sheet_name='symbols')
symbols = sym_df['Symbol'].unique()

tick1 = st.sidebar.multiselect('Select Competitor(s): ', symbols, default=st.session_state['main_ticker'])
tick_list = [x for x in tick1 if x != None]
start_date = st.sidebar.date_input('Select the start date:', datetime.datetime(2020,1,1))
end_date = st.sidebar.date_input('Select the end date', datetime.datetime.today())

data = yf.Ticker(tick_list[0]).history(start=start_date, end=end_date)
data['ticker'] = tick_list[0]
for i in tick_list[1:len(tick_list)]:
    temp_df = yf.Ticker(i).history(start=start_date, end=end_date)
    temp_df['ticker'] = i
    data = pd.concat([data, temp_df])

data = data.reset_index()
data['Date'] = pd.to_datetime(data['Date'])
data = data[(data['Date']>=start_date.strftime('%Y-%m-%d')) & (data['Date']<=end_date.strftime('%Y-%m-%d'))]


fig = px.line(data,
              x='Date',
              y='Close',
              color='ticker',
              title='Historical Stock Prices')
st.title('Competitor Analytics')
st.plotly_chart(fig, use_container_width=True)
st.title('News')
for i in yf.Ticker(tick_list[0]).news:
    i['providerPublishTime'] = strftime('%Y-%m-%d', localtime(i['providerPublishTime']))
    st.write(i['providerPublishTime'] + ' - ' + '[{y}]({x})'.format(x=i['link'], y=i['title']))