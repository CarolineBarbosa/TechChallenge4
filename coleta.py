import yfinance as yf
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def get_dados():
    symbol = 'AAPL'
    start_date = '2018-01-01'
    end_date = '2024-07-01'

    df = yf.download(symbol, start=start_date, end=end_date)
    print(df)
    data = df[['Close']].copy()

    scaler = MinMaxScaler()
    #print(data)
    scaled_data = scaler.fit_transform(data)
    #print(scaled_data)
    return data, scaled_data