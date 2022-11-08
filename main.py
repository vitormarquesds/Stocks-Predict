import yfinance as yf
from datetime import date, timedelta, time
import plotly.graph_objects as go
import streamlit as st
import plotly.graph_objects as go


st.header("Stock Prices")
st.info("Created by Vitor Moura - Machine Learning Engineer")

stockName, stockTime = st.columns(2)

with stockName:
    stock = st.text_input("Stock Name:", value="MSFT")

with stockTime:
    time = st.number_input("Range Time in Months:", min_value=1, step=1)

with st.sidebar:

    st.header("Stock Details")

    stock1 = yf.Ticker(stock)
    stock1 = stock1.info

    Name=stock1['longName']
    Logo=stock1['logo_url']
    Symbol=stock1['symbol']
    Market=stock1['market']
    CurrentPrice=stock1['currentPrice']
    website=stock1['website']
    country=stock1['country']
    fullTimeEmployees=stock1['fullTimeEmployees']
    industry=stock1['industry']
    sector=stock1['sector']
    #StarRating=stock1['morningStarRiskRating']
    DividensValue=stock1['lastDividendValue']
    TotalCash=stock1['totalCash']
    TotalDebt=stock1['totalDebt']
    ReturnEquity=stock1['returnOnEquity']
    nAlanystOp=stock1['numberOfAnalystOpinions']
    freeCashflow=stock1['freeCashflow']
    recommendationKey=stock1['recommendationKey']
    city=stock1['city']

    st.image(Logo, width=80)
    st.write("Company: {}".format(Name))
    st.write("Industry: {}".format(industry))
    st.write("Sector: {}".format(sector))
    st.write("Symbol Market: {}".format(Symbol))
    st.write("Market: {}".format(Market))
    st.write("Current Price: ${}".format(CurrentPrice))
    st.write("Website: {}".format(website))
    st.write("Country Founded: {}".format(country))
    st.write("Total Employees: {}".format(fullTimeEmployees))

@st.cache
def get_data(stockName, timeYear):

    stock = stockName

    time = timeYear*30

    today = date.today()

    d1 = today.strftime("%Y-%m-%d")
    end_date = d1

    d2 = date.today() - timedelta(days = time)
    d2 = d2.strftime("%Y-%m-%d")

    start_day = d2

    data = yf.download(stock, start = start_day, end= end_date, progress=False)

    data['Date'] = data.index
    data = data[["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]]

    data.reset_index(drop=True, inplace = True)

    return data

# Tab 1
df = get_data(stockName=stock, timeYear=time)


@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(df)

# Tab 2

figure = go.Figure(data=[go.Candlestick(x=df["Date"],
                                        open=df["Open"], 
                                        high=df["High"],
                                        low=df["Low"], 
                                        close=df["Close"])])
figure.update_layout(xaxis_rangeslider_visible= False,
                        margin =dict(l=0, r=0, t=30, b=0) )

# Tabs

graph,data = st.tabs([ "Graph","Data"])

with graph:
   st.header("{} Price Graph".format(Name))
   st.plotly_chart(figure)

with data:
    st.header("{} Data".format(Name))
    st.dataframe(df, width=720, height=260)
    if st.download_button(label = "Download Data", data = csv, file_name='{}_data.csv'.format(stock), mime='text/csv'):
        st.balloons()
        
        