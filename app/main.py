from fastapi import FastAPI, HTTPException, Body
import yfinance as yf
import numpy as np
import app.coleta as coleta
from tensorflow.keras.models import load_model, clone_model
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.losses import MeanSquaredError
import joblib
import os

app = FastAPI()

TIME_STEPS = 60
PRED_DAYS = 30

def fetch_data(symbol: str, period='180d'):
    df = yf.download(symbol, period=period)
    df = df[['Close']]
    df.dropna(inplace=True)
    return df

def create_sequences(data, time_steps=60):
    X, y = [], []
    for i in range(len(data) - time_steps):
        X.append(data[i:i + time_steps])
        y.append(data[i + time_steps])
    return np.array(X), np.array(y)

def fine_tune_model(general_model, X, y):
    model = clone_model(general_model)
    model.set_weights(general_model.get_weights())
    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=10, batch_size=32,
              callbacks=[EarlyStopping(patience=2, restore_best_weights=True)],
              verbose=0)
    return model

@app.get("/sector")
def coletar_setor():
    return coleta.get_setor()

@app.get("/symbol")
def coletar_symbol(sector: str):
    return coleta.get_symbols(sector)

@app.get("/coletar_dados")
def coletar(data_inicial: str, data_final: str, symbol: str):
    return coleta.get_dados(symbol, data_inicial, data_final)

@app.post("/predict")
def predict(stock_code: str):
    symbol = stock_code.upper()

    try:
        df = fetch_data(symbol)
        if len(df) < TIME_STEPS + PRED_DAYS:
            raise ValueError("Not enough historical data.")
    except Exception:
        raise HTTPException(status_code=404, detail="Could not fetch stock data.")

    scaler = joblib.load(f'app/models/scaler.joblib')
    scaled = scaler.fit_transform(df.values)
    X, y = create_sequences(scaled, time_steps=TIME_STEPS)

    if len(X) == 0:
        raise HTTPException(status_code=400, detail="Not enough data after preprocessing.")

    X = X.reshape((X.shape[0], X.shape[1], 1))

    model_path = os.path.join(os.path.dirname(__file__), "models", "general_lstm.h5")
    if not os.path.exists(model_path):
        raise HTTPException(status_code=500, detail="Pretrained model not found.")
    general_model = load_model(model_path,custom_objects={"mse": MeanSquaredError()})

    model = fine_tune_model(general_model, X, y)

    input_seq = scaled[-TIME_STEPS:].reshape(1, TIME_STEPS, 1)
    predictions = []
    next_price = model.predict(input_seq, verbose=0)
     
    predictions = scaler.inverse_transform(np.array(next_price).reshape(-1, 1)).flatten().tolist()

    return {"symbol": symbol, "predicted_prices": predictions}
