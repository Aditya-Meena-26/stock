# stockpredictor/prediction/views.py
from django.shortcuts import render
from .models import StockData, Prediction
from .tasks import update_stock_predictions

def home(request):
    # Trigger the update task
    update_stock_predictions.delay()

    predictions = []
    stock_symbols = ['^NSEI', '^BANKNIFTY']

    for stock_symbol in stock_symbols:
        historical_data = list(StockData.objects.filter(symbol=stock_symbol).order_by('date').values_list('close_price', flat=True))
        historical_dates = list(StockData.objects.filter(symbol=stock_symbol).order_by('date').values_list('date', flat=True))
        predicted_prices = list(Prediction.objects.filter(symbol=stock_symbol).order_by('date').values_list('predicted_price', flat=True))

        predictions.append({
            'symbol': stock_symbol,
            'historical_dates': historical_dates,
            'historical_prices': historical_data,
            'predicted_prices': predicted_prices,
        })

    context = {
        'predictions': predictions,
    }
    return render(request, 'home.html', context)
