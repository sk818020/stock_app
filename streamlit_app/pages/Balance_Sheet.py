import yfinance as yf
import streamlit as st
import plotly.express as px
import datetime
import pandas as pd
import numpy as np

fpath = r'stock_analysis3.xlsm'
sym_df = pd.read_excel(fpath, sheet_name='symbols')
symbols = sym_df['Symbol'].unique()
ticker = st.sidebar.multiselect('Select Ticker', symbols, default=st.session_state['main_ticker'])
st.title('{x} - Balance Sheet'.format(x=', '.join(ticker)))
st.caption('This page is to look at the balance sheet items for a given'
           ' company and its competitors. You can add competitors by selecting multiple'
           ' tickers. You can select multiple balance sheet items by selecting multiple'
           ' balance sheet catagories in the sidebar.')
st.divider()


########################################################################################################################
# Data Processing
########################################################################################################################
data = pd.DataFrame()
for tick in ticker:
    bs = yf.Ticker(tick).balance_sheet
    bs.columns = [str(x) for x in bs.columns]
    bs1 = bs.reset_index()
    bs2 = pd.melt(bs1, id_vars=['index'],value_vars=bs.columns[0:len(bs.columns)])
    bs2['ticker'] = tick
    data = pd.concat([bs2, data])


########################################################################################################################
# Side Bar
########################################################################################################################
bs_cat = st.sidebar.multiselect('Select Metric:',
                                bs2['index'].unique(),
                                default=['Cash And Cash Equivalents', 'Total Debt'])


########################################################################################################################
# More Data Processing
########################################################################################################################
data['value'] = data['value']/1_000_000
data = data.rename({'index':'bs_category','variable':'date', 'value':'value($M)'}, axis=1)
data['date'] = pd.to_datetime(data['date'])
data['date'] = data['date'].dt.strftime('%Y-%m-%d')


########################################################################################################################
# Main Page - two columns
########################################################################################################################

col1, col2 = st.columns((.6,.4), gap='small')

def create_plot(ticker, cat, data):
    data1 = data[(data['bs_category']==cat) &
                 (data['ticker'].isin(ticker))]
    fig = px.line(data1,
                  x='date',
                  y='value($M)',
                  color='ticker',
                  height=400,
                  title='Balance Sheet History - {x}'.format(x=cat),
                  )
    return fig

with col1:
    for cat in bs_cat:
        data1 = data[(data['bs_category']==cat) &
                     (data['ticker'].isin(ticker))]
        fig1 = create_plot(ticker=ticker, cat = cat, data=data1)
        st.plotly_chart(fig1, use_container_width=True)

with col2:
    for cat in bs_cat:
        data1 = data[(data['bs_category'] == cat) &
                     (data['ticker'].isin(ticker))]
        st.dataframe(data1, height=400, hide_index=True, width=500)

st.sidebar.subheader('Full name of companies:')
for tick in ticker:
    st.sidebar.caption('{y} ({x})'.format(x=tick, y= yf.Ticker(tick).info['longName']))
