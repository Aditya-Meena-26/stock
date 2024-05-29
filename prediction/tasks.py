# stockpredictor/prediction/tasks.py
from celery import shared_task
from stockpredictor.celery import app
from .utils import fetch_and_predict
@shared_task
def update_stock_predictions():
    fetch_and_predict()
