import pandas as pd
import yfinance as yf
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def get_symbols(sector):
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    tables = pd.read_html(url)
    df = tables[0]
    
    df['Symbol'] = df['Symbol'].str.replace('.', '-', regex=False)
    # Filtra por setor de tecnologia
    df_tech = df[df['GICS Sector'] == sector]
    
    symbol_list = df_tech[['Symbol', 'Security']].rename(columns={'Symbol': 'symbol', 'Security': 'name'})
    return symbol_list.to_dict(orient='records')

def get_setor():
   df = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
   return df['GICS Sector'].unique().tolist()
#     return ["Industrials",
#   "Health Care",
#   "Information Technology",
#   "Utilities",
#   "Financials",
#   "Materials",
#   "Consumer Discretionary",
#   "Real Estate",
#   "Communication Services",
#   "Consumer Staples",
#   "Energy"]


def get_dados(symbol, data_inicial, data_final):
    df = yf.download(symbol, start=data_inicial, end=data_final)
    df.columns = ['_'.join(col).strip() for col in df.columns.values]
    df = df.reset_index()
    return df.to_dict(orient='records')