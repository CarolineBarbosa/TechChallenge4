import yfinance as yf
# Especifique o símbolo da empresa que você vai trabalhar
# Configure data de início e fim da sua base
symbol = 'VALE'
start_date = '2018-01-01'
end_date = '2025-07-05'
# Use a função download para obter os dados
df = yf.download(symbol, start=start_date, end=end_date)
print(df.head())
df.to_csv(f'data/{symbol}.csv', index=True)