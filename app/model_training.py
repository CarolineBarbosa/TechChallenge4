import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import os
from app.scrapper import *  # This should define save_training_data()

def fetch_data(code):
    df = pd.read_parquet(f'data/{code}.parquet')
    print(df.head())
    df = df[['Close']]  
    print(df.head())
    df.dropna(inplace=True)
    return df

def create_sequences(data, time_steps=60):
    X, y = [], []
    for i in range(len(data) - time_steps):
        X.append(data[i:i + time_steps])
        y.append(data[i + time_steps])
    return np.array(X), np.array(y)

def train_model(symbol):
    df = fetch_data(symbol)
    
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(df.values)  # ✅ shape: (n, 1)

    X, y = create_sequences(scaled, time_steps=60)
    
    # ✅ Reshape to (samples, time_steps, features)
    X = X.reshape((X.shape[0], X.shape[1], 1))
    
    print(f"Training data shape: X={X.shape}, y={y.shape}")

    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(X.shape[1], 1)),
        LSTM(50),
        Dense(1)
    ])
    
    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=30, batch_size=32)

    if not os.path.exists('models'):
        os.makedirs('models')
    
    model.save(f'models/{symbol}_lstm.h5')
    # ✅ Save full scaler object to use inverse_transform later
    import joblib
    joblib.dump(scaler, f'models/{symbol}_scaler.gz')  

if __name__ == "__main__":
    save_training_data("VALE")  # Ensure this saves .parquet at 'data/VALE.parquet'
    train_model("VALE")
