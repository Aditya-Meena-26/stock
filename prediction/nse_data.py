# stockpredictor/prediction/nse_data.py
import yfinance as yf

def fetch_stock_data(symbol, start_date, end_date):
    stock = yf.Ticker(symbol)
    data = stock.history(start=start_date, end=end_date)
    return data
