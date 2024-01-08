import pandas as pd
import plotly.express as px
import numpy as np
import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from dateutil.relativedelta import relativedelta
import datetime
from time import strftime
import chart_studio.plotly as py
from plotly.graph_objs import *

########################################################################################################################
# Title
########################################################################################################################


########################################################################################################################
# Function definitions
########################################################################################################################
def date_test(date):
    """
    The purpose of this date test is to see if the start or end date are on a weekend.
    If either day is on a weekend it moves the date up 2 days. This is okay because the
    focus of the analysis is on the prior year. Moving the start date up 2 days
    means that the start day is two days soon (because one year ago today is a weekday).
    :param date:
        Must be a datetime object. In the app this is chosen by the user in the side bar.
        - DEFAULT == 'XOM' or ExxonMobil's stock symbol.
    :return:
        This function returns dates that have been adjusted to not be on a weekend.
    """
    if date.weekday() in [5, 6]:
        date = datetime.datetime(
            year=date.year,
            month=date.month,
            day=(date + relativedelta(days=2)).day
        )
        return date
    else:
        date = datetime.datetime(
            year=date.year,
            month=date.month,
            day=date.day
        )
        return date


########################################################################################################################
# Get user input for symbol, end_date and start_date.
#   Symbol is pulled from a variable saved to the session state.
########################################################################################################################
symbol = st.sidebar.multiselect('Select a stock symbol: ',
                                st.session_state['symbol_list'],
                                default=st.session_state['main_ticker'])
end_date = st.sidebar.date_input('End date:',
                                 datetime.datetime.today())
start_date = st.sidebar.date_input('Start date:',
                                   end_date - relativedelta(years=1))


########################################################################################################################
# Use the function, date_test, to correct the dates to be on weekdays. Save the dates as application
# variables that can be used on other pages.
########################################################################################################################
end_date = date_test(end_date)
start_date = date_test(start_date)

st.session_state['start_date'] = start_date
st.session_state['end_date'] = end_date


########################################################################################################################
# Get the data from yfinance and clean it up. .
########################################################################################################################



data = yf.Ticker(symbol[0]).history(start=st.session_state['start_date'],end=st.session_state['end_date'])


data = data.reset_index()
data['Date'] = pd.to_datetime(data['Date']).dt.date
cols_replace = [x.lower() for x in data.columns]
cols_replace = [x.replace(' ', '_') for x in cols_replace]
cols_map = {data.columns[i]: cols_replace[i] for i in range(len(data.columns))}
data.rename(columns=cols_map, inplace=True)
data['ticker'] = symbol[0]

plt.figure(figsize=(10,5))
plt.title(f"{symbol[0]} - Autocorrelation Plot")
pd.plotting.autocorrelation_plot(series=data['close'],)
#plt.figure(figsize=(10,5))



col1, col2 = st.columns((.6,.4))
with col1:
    st.pyplot(plt, use_container_width=True)
    st.write('')
    st.caption('hello')





