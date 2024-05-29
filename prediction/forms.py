# stockpredictor/prediction/forms.py
from django import forms

class StockPredictionForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    prediction_days = forms.IntegerField(min_value=1)
    stock_symbols = forms.CharField(help_text="Enter comma separated stock symbols (e.g., RELIANCE.BO,TCS.BO)")
