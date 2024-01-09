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
########################################################################################################################')
st.title('Analysis of Stock Performance')


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


def daily_returns(df, type1):
    df2 = df.loc[:, ['close', 'ticker', 'date']]
    df2['simple_rtn'] = df['close'].pct_change()
    df2['log_rtn'] = np.log(df['close'] / df['close'].shift(1))
    fig = px.line(df2,
                  x=df2['date'],
                  y=df2[st.session_state['log_or_simp']],
                  title=f'Daily Returns | {symbol[0]}'
                  )
    fig.update_layout(
        font=dict(
            family="Arial",
            size=18,
            color='RebeccaPurple'
        )
    )
    st.plotly_chart(fig, use_container_width=True)


def calc_return(data,
                start_1=st.session_state['start_date'],
                end_1=st.session_state['end_date']
                ):
    start_price = data[data['date'] == data['date'].min()]['close'].iloc[0]
    end_price = data[data['date'] == data['date'].max()]['close'].iloc[0]

    st.metric(f'Start price on {start_1.strftime("%Y-%m-%d")}',
              "$" + str(round(start_price,2)))
    st.metric(f'End price on {end_1.date().strftime("%Y-%m-%d")}',
              "$" + str(round(end_price,2)))
    st.metric(f'1-year return %', str(round((end_price - start_price)*100/start_price,2))+ '%',
              f'{round((end_price - start_price), 2)} per share')

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

col1, col2 = st.columns((.7,.3))
with col1:
    type1 = st.selectbox('How would you like to calculate daily return (simple or log)?',
                         ['simple_rtn', 'log_rtn'])
    st.session_state['log_or_simp'] = type1

    daily_returns(df=data, type1=st.session_state['log_or_simp'])
    st.pyplot(plt, use_container_width=True)

with col2:
    calc_return(data)

