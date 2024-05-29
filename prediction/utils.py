# stockpredictor/prediction/utils.py
from .models import StockData, Prediction
from .nse_data import fetch_stock_data
from .price_prediction_advanced import LSTMModel
from datetime import datetime, timedelta

def fetch_and_predict():
    stock_symbols = ['^NSEI', '^BANKNIFTY']  # Nifty 50 and Bank Nifty symbols
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')

    for stock_symbol in stock_symbols:
        data = fetch_stock_data(stock_symbol, start_date, end_date)

        # Clear existing data for the stock symbol
        StockData.objects.filter(symbol=stock_symbol).delete()
        Prediction.objects.filter(symbol=stock_symbol).delete()

        for index, row in data.iterrows():
            StockData.objects.create(
                symbol=stock_symbol,
                date=index,
                open_price=row['Open'],
                high_price=row['High'],
                low_price=row['Low'],
                close_price=row['Close'],
                volume=row['Volume']
            )

        historical_data = list(StockData.objects.filter(symbol=stock_symbol).order_by('date').values_list('close_price', flat=True))
        historical_dates = list(StockData.objects.filter(symbol=stock_symbol).order_by('date').values_list('date', flat=True))

        if len(historical_data) >= 60:
            lstm_model = LSTMModel()
            lstm_model.train(historical_data)
            prediction_data = historical_data[-60:]

            try:
                predicted_prices = lstm_model.predict(prediction_data)
            except Exception as e:
                predicted_prices = None
                print(f"Prediction error for {stock_symbol}: {e}")

            if predicted_prices is not None:
                prediction_start_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
                for i, price in enumerate(predicted_prices):
                    try:
                        Prediction.objects.create(
                            symbol=stock_symbol,
                            date=prediction_start_date + timedelta(days=i),
                            predicted_price=price
                        )
                    except Exception as e:
                        print(f"Error saving prediction for {stock_symbol}: {e}")
