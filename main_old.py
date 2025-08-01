from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import numpy as np
import app.coleta as coleta
from datetime import datetime
import joblib

app = FastAPI(
    title="LSTM Stock Predictor API",
    description="API para previsão de preços de ações com LSTM",
    version="1.0"
)

@app.get("/sector")
def coletar_setor():
    return coleta.get_setor()

@app.get("/symbol")
def coletar_symbol(sector: str):
    return coleta.get_symbols(sector)

@app.get("/coletar_dados")
def coletar(data_inicial: str, data_final: str, symbol: str):
    return coleta.get_dados(symbol, data_inicial, data_final)
# # Carregando o modelo e o scaler
# model = load_model("app/model/modelo_lstm.h5")
# scaler = joblib.load("app/utils/scaler.pkl")

# # Modelo de entrada
# class PredictionInput(BaseModel):
#     inputs: List[float]

# @app.post("/predict")
# def predict(data: PredictionInput):
#     inputs = data.inputs

#     if len(inputs) != 60:
#         raise HTTPException(status_code=400, detail="A entrada deve conter exatamente 60 valores.")

#     # Normalização
#     scaled = scaler.transform(np.array(inputs).reshape(-1, 1))
#     X = np.reshape(scaled, (1, 60, 1))

#     # Previsão
#     prediction = model.predict(X)
#     predicted_price = scaler.inverse_transform(prediction)[0][0]

#     return {"predicted_price": float(predicted_price)}
