import math
import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler 
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from keras import layers
import datetime as dt
from datetime import datetime
import plotly.express as px

class StockPricePredictor:
  def __init__(self, stock_name, start_date="2018-01-01", end_date=dt.date.today(), num_epochs=50, batch_size=4):
    self.stock_name = stock_name
    self.start_date = start_date
    self.end_date = end_date
    self.stock_path = r"C:\NEA_Folder\stock_website\model_files\{}_stock_prediction_model.h5".format(self.stock_name)
    self.context = {}
    self.num_epochs = num_epochs
    self.batch_size = batch_size
    
    
    stock_data = yf.download(self.stock_name, start=self.start_date, end=self.end_date)
    stock_data = stock_data.reset_index()
    stock_data = pd.DataFrame(stock_data)
    
    remove = ['Open', "High", "Low", "Adj Close", "Volume"]

    for i in remove:
      stock_data.__delitem__(i)
    
    # stock_data = stock_data.round(decimals=3)
  
    stock_data['Date'] = stock_data['Date'].astype('object')
    
    for i in range(len(stock_data)):
      date = stock_data.at[i,"Date"]
      updated_date = date.strftime(r"20%y-%m-%d")
      stock_data.loc[i, 'Date'] = updated_date
      
    
      
    close_prices = stock_data['Close']
    self.values = close_prices.values
    self.training_data_len = math.ceil(len(self.values))
    
    self.stock_data = stock_data
    self.scaler = MinMaxScaler(feature_range=(0,1))
    self.scaled_data = self.scaler.fit_transform(self.values.reshape(-1,1))
    self.train_data = self.scaled_data[0: self.training_data_len, :]
    self.scaled_data_len = len(self.scaled_data)
    
    
  def get_current_data(self):
    ticker = yf.Ticker(self.stock_name)
    todays_data = ticker.history(period='1d')
    current_price =  todays_data['Close'][0]
    open_price =  todays_data['Open'][0]
    daily_change = current_price - open_price
    daily_perc_change = round((daily_change/current_price) * 100, 1)
    return {"current_price": current_price, "daily_change": daily_change, "daily_perc_change": (daily_perc_change), "open_price": open_price}
  
  def _train_model(self):
    self.training_data_len = math.ceil(len(self.values)*0.9)
    x_train = []
    y_train = []

    for i in range(60, len(self.train_data)):
      x_train.append(self.scaled_data[i-60:i, 0])
      y_train.append(self.scaled_data[i, 0])
        
    x_train, y_train = np.array(x_train), np.array(y_train)


    test_data = self.scaled_data[self.training_data_len-60: , : ]
    x_test = []
    y_test = self.values[self.training_data_len:]

    for i in range(60, len(test_data)):
      x_test.append(test_data[i-60:i, 0])

    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    
    self.model = keras.Sequential()
    self.model.add(layers.LSTM(100, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    self.model.add(layers.LSTM(100, return_sequences=False))
    self.model.add(layers.Dense(25))
    self.model.add(layers.Dense(1))
    
    self.model.compile(optimizer='adam', loss='mean_squared_error')
    self.model.fit(x_train, y_train, batch_size=self.batch_size, epochs=self.num_epochs)
   
    
    self.model.save(self.stock_path)
    
    predict1 = self.model.predict(x_test)
    predict1 = self.scaler.inverse_transform(predict1)
    
    rmse = np.sqrt(np.mean(predict1 - y_test)**2)
    print(rmse)

    data = self.stock_data['Close']
    dates = self.stock_data["Date"]
    train = data[:self.training_data_len]
    train_dates = dates[:self.training_data_len]
    validation_data = data[self.training_data_len:self.scaled_data_len]
    validation_dates = dates[self.training_data_len:self.scaled_data_len]
    prediction_data = data[self.scaled_data_len:]
    prediction_dates = dates[self.scaled_data_len:]
    fig = px.line(x=train_dates, y=train, title = "Stock Data")
    fig.add_scatter(x=validation_dates, y=predict1)
    # fig.add_scatter(x=validation_dates, y=validation_data)
    fig.show()
    # plt.figure(figsize=(16,8))
    # plt.title('Model')
    # plt.xlabel('Date')
    # plt.ylabel('Close Price USD ($)')
    # plt.plot(train_dates, train)
    # plt.plot(prediction_dates, prediction_data)
    # plt.plot(validation_dates, validation_data)
    # plt.plot(validation_dates, predict1)
    # plt.legend(['Train', 'Predictions','validation' ,'predict1'], loc='lower right')
    # plt.show()
  
  def predict_future_price(self):
    loaded_model = keras.models.load_model(self.stock_path)

    for day in range(120):
      x_predict = []
      x_predict.append(self.scaled_data[len(self.scaled_data)-60:])
      x_predict = np.array(x_predict)
      prediction = loaded_model.predict(x_predict)
      self.scaled_data = np.append(self.scaled_data, prediction, axis=0)
      predictions = self.scaler.inverse_transform(prediction)
      prediction_date = dt.date.today() + dt.timedelta(days=day)
      self.stock_data.loc[len(self.stock_data)] = [prediction_date.strftime(r"20%y-%m-%d"), predictions[0][0]]
    
    # self.stock_data['Date'] = self.stock_data['Date'].astype('datetime64')
    # self.stock_data = self.stock_data.round(decimals=3)
    data = self.stock_data['Close']
    dates = self.stock_data["Date"]
    train = data[:self.scaled_data_len]
    train_dates = dates[:self.scaled_data_len]
    prediction_data = data[self.scaled_data_len:]
    prediction_dates = dates[self.scaled_data_len:]
    # fig = px.line(x=train_dates, y=train, title = "Stock Data")
    # fig.add_scatter(x=prediction_dates, y=prediction_data)
    # fig.show()
    # fig.write_html(r"C:\NEA_Folder\stock_website\homepage\templates\test.html")
    # plt.figure(figsize=(16,8))
    # plt.title('Model')
    # plt.xlabel('Date')
    # plt.ylabel('Close Price USD ($)')
    # plt.plot(train_dates, train)
    # plt.plot(prediction_dates, prediction_data)
    # plt.legend(['Train', 'Predictions'], loc='lower right')
    # plt.show()
    self.context = {'train': train.values.tolist(), 'train_dates': train_dates.values.tolist(), 'prediction_data': prediction_data.values.tolist(), 'prediction_dates': prediction_dates.values.tolist()}
    return self.context
 
  def predict_future_price_recursive(self, num_days=120, i=0):
    if i == num_days:
        data = self.stock_data['Close']
        dates = self.stock_data["Date"]
        train = data[:self.scaled_data_len]
        train_dates = dates[:self.scaled_data_len]
        prediction_data = data[self.scaled_data_len:] 
        prediction_dates = dates[self.scaled_data_len:]
        self.context = {'train': train.values.tolist(), 'train_dates': train_dates.values.tolist(), 'prediction_data': prediction_data.values.tolist(), 'prediction_dates': prediction_dates.values.tolist()}
        return self.context
    
    loaded_model = keras.models.load_model(self.stock_path)

    x_predict = []
    x_predict.append(self.scaled_data[len(self.scaled_data)-60:])
    x_predict = np.array(x_predict)
    prediction = loaded_model.predict(x_predict)
    self.scaled_data = np.append(self.scaled_data, prediction, axis=0)
    predictions = self.scaler.inverse_transform(prediction)
    prediction_date = dt.date.today() + dt.timedelta(days=i)
    self.stock_data.loc[len(self.stock_data)] = [prediction_date.strftime(r"%y-%m-%d"), predictions[0][0]]
    
    return self.predict_future_price_recursive(num_days, i+1)

        
# tsla_stock = StockPricePredictor("TSLA")
# aapl_stock = StockPricePredictor("AAPL")
# amzn_stock = StockPricePredictor("AMZN")
# msft_stock = StockPricePredictor("MSFT")
# nvda_stock = StockPricePredictor("NVDA")
# goog_stock = StockPricePredictor("GOOG")

# print(tsla_stock.predict_future_price())

# nvda_stock._train_model()