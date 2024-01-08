import pandas as pd
import plotly.express as px
import numpy as np
import yfinance as yf
import seaborn
import matplotlib.pyplot as plt
import streamlit as st
import datetime as dt
from dateutil.relativedelta import relativedelta
import datetime
from time import strftime

st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(layout='wide')


fpath = r'stock_analysis3.xlsm'
sym_df = pd.read_excel(fpath, sheet_name='symbols')
symbols = sym_df['Symbol'].unique()

tick1 = st.sidebar.multiselect('Select Competitor(s): ', symbols, default=st.session_state['main_ticker']+['CVX', 'PSX', 'WMT'])
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
 #   i['providerPublishTime'] = strftime('%Y-%m-%d', localtime(i['providerPublishTime']))
    st.write(str(i['providerPublishTime']) + ' - ' + '[{y}]({x})'.format(x=str(i['link']), y=str(i['title'])))


def auto_plot(ticker):
    end_date = datetime.datetime.today()
    start_date = end_date - relativedelta(years=1)

    def test_weekday(start_date, end_date):
        if start_date.strftime('%A') in ['Saturday', 'Sunday']:
            start_date = start_date + relativedelta(days=1)
            if start_date.strftime('%A') in ['Saturday', 'Sunday']:
                start_date = start_date + relativedelta(days=1)
                return start_date
            else:
                return start_date
        else:
            return start_date

    start_date = test_weekday(start_date=start_date, end_date=end_date)
    xom_data = yf.Ticker(ticker).history(
        end=end_date.strftime('%Y-%m-%d'),
        start=start_date.strftime('%Y-%m-%d')
    )

    xom_data = xom_data.reset_index()
    xom_data['Date'] = pd.to_datetime(xom_data['Date']).dt.date
    cols = xom_data.columns
    cols_replace = [x.lower() for x in cols]
    cols_replace = [x.replace(' ', '_') for x in cols_replace]
    cols_map = {cols[i]: cols_replace[i] for i in range(len(cols))}
    xom_data.rename(columns=cols_map, inplace=True)
    start_price = xom_data[xom_data['date'] == datetime.date(
        year=int(start_date.year),
        month=int(start_date.month),
        day=int(start_date.day)
    )]['close'][0]

    if end_date.day == 6:
        end_date = end_date - relativedelta(days=1)
    elif end_date.day == 7:
        end_date = end_date - relativedelta(days=2)
    else:
        end_date = end_date
    end_price = xom_data[xom_data['date'] == datetime.date(
        year=int(end_date.year),
        month=int(end_date.month),
        day=int(end_date.day)
    )]['close'].iloc[0]
    return_perc = round(((end_price - start_price) / start_price) * 100, 2)

    print(f'Start share price: ${round(start_price, 2)} per share on {start_date.date()}.')
    print(f'End share price: ${round(end_price, 2)} per share on {end_date.date()}.')
    print(f"The one year return on {ticker.upper()} stock was {return_perc}%.")
    pd.plotting.autocorrelation_plot(xom_data['close']).set_title(
        f"{tick_list[0]} | Autocorrelation Plot | {start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%y')}")
#    plt.rcParams['text.color'] = 'white'
    return plt

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.write(f"{tick_list[0]} | Autocorrelation Plot | {start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%y')}")
    st.pyplot(auto_plot('xom'))
    plt.title(
        f"{tick_list[0]} | Autocorrelation Plot | {start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%y')}")
