import yfinance as yf
# Especifique o símbolo da empresa que você vai trabalhar
# Configure data de início e fim da sua base
def collect_data(code , period='180d'):
    df = yf.download(code,period='180d')
    return df

def save_training_data(code, period='180d'):
    df = collect_data(code, period='180d')
    df.to_parquet(f'data/{code}.parquet', index=True)
