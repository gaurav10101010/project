import streamlit as st,pandas as pd,numpy as np,yfinance as yf
import plotly.express as px

st.title('stock Dashboard')
ticker1 = st.sidebar.text_input('Ticker', key='ticker1')
start_date=st.sidebar.date_input('start Date')
end_date=st.sidebar.date_input('End Date')

data=yf.download(ticker1,start=start_date,end=end_date)
data= yf.download(ticker1,start=start_date,end=end_date)
print(data.columns)
fig =px.line(data,x=data.index,y =data['Adj Close'],title=ticker1)
st.plotly_chart(fig)  

pricing_data,fundamental_data,news=st.tabs(["Pricing Data","Fundamental Data","Top 10 News"])

with pricing_data:
    st.header('Price Movements')
    data2=data
    data2['% Changes'] = data['Adj Close']/data['Adj Close'].shift(1)-1
    data2.dropna(inplace=True)
    annual_return =data2['% Changes'].mean()*252*100
    st.write('Annual_return is ',annual_return,'%')
    stdev =np.std(data2['% Changes']*np.sqrt(252))
    st.write('standard Deviation is ',stdev*100,'%')


from alpha_vantage.fundamentaldata import FundamentalData

# Initialize the Alpha Vantage API
API_KEY = 'OW1639L63B5UCYYL'  # Replace with your API key
fd = FundamentalData(API_KEY, output_format='pandas')

# Streamlit App
st.title("Financial Data Viewer")

# Input for the stock ticker symbol
ticker2 = st.text_input("Enter the stock ticker symbol:", key='ticker2')

if ticker2:
    # Fetch and display the Balance Sheet
    st.subheader("Balance Sheet")
    balance_sheet, _ = fd.get_balance_sheet_annual(ticker2)
    bs = balance_sheet.T[2:]  # Transpose and slice columns
    bs.columns = list(balance_sheet.T.iloc[0])  # Set proper column names
    st.write(bs)

    # Fetch and display the Income Statement
    st.subheader("Income Statement")
    income_statement, _ = fd.get_income_statement_annual(ticker2)
    is1 = income_statement.T[2:]  # Transpose and slice columns
    is1.columns = list(income_statement.T.iloc[0])  # Set proper column names
    st.write(is1)

    # Fetch and display the Cash Flow Statement
    st.subheader("Cash Flow Statement")
    cash_flow, _ = fd.get_cash_flow_annual(ticker2)
    cf = cash_flow.T[2:]  # Transpose and slice columns
    cf.columns = list(cash_flow.T.iloc[0])  # Set proper column names
    st.write(cf)
else:
    st.warning("Please enter a stock ticker symbol to view the financial data.")


from stocknews import StockNews

# Input for the stock ticker symbol
ticker3 = st.text_input("Enter the stock ticker symbol:", key='ticker3')

if ticker3:
    # Fetch and display the news
    st.header(f"News of {ticker3}")
    sn = StockNews(ticker3, save_news=False)
    df_news = sn.read_rss()
    
    for i in range(min(10, len(df_news))):  # Ensure we don't exceed available news
        st.subheader(f'News {i+1}')
        st.write(df_news["published"][i])
        st.write(df_news["title"][i])
        st.write(df_news["summary"][i])
        
        title_sentiment = df_news['sentiment_title'][i]
        st.write(f'Title Sentiment: {title_sentiment}')
        
        news_sentiment = df_news["sentiment_summary"][i]
        st.write(f'News Sentiment: {news_sentiment}')
else:
    st.warning("Please enter a stock ticker symbol to view the news.")