# stockpredictor/prediction/price_prediction_advanced.py
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

class LSTMModel:
    def __init__(self):
        self.model = Sequential([
            LSTM(50, return_sequences=True, input_shape=(60, 1)),
            LSTM(50, return_sequences=False),
            Dense(25),
            Dense(1)
        ])
        self.model.compile(optimizer='adam', loss='mean_squared_error')
        self.scaler = None

    def train(self, training_data):
        data = np.array(training_data)
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = self.scaler.fit_transform(data.reshape(-1, 1))

        x_train, y_train = [], []
        for i in range(60, len(scaled_data)):
            x_train.append(scaled_data[i-60:i, 0])
            y_train.append(scaled_data[i, 0])
        x_train, y_train = np.array(x_train), np.array(y_train)

        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
        self.model.fit(x_train, y_train, batch_size=1, epochs=1)

    def predict(self, historical_data):
        if len(historical_data) < 60:
            raise ValueError("Not enough data to make a prediction. Need at least 60 data points.")
        
        data = np.array(historical_data)
        scaled_data = self.scaler.transform(data.reshape(-1, 1))

        x_test = []
        for i in range(60, len(scaled_data) + 1):
            x_test.append(scaled_data[i-60:i, 0])
        x_test = np.array(x_test)

        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
        predicted_price = self.model.predict(x_test)
        predicted_price = self.scaler.inverse_transform(predicted_price)

        return predicted_price.flatten().tolist()
