#Predicts future stock prices given a ticker symbol
#Utilizes LSTM (Long Short-Term Memory Neural Network)


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from keras.layers import LSTM
from sklearn import preprocessing
from sklearn.model_selection import TimeSeriesSplit
from pandas_datareader import get_data_yahoo
from keras.models import Sequential
from keras.layers import Dense
from keras.utils.vis_utils import plot_model

def stock_prediction(ticker, start, end):

    #Data Manipulation and Scaling
    yf.pdr_override()

    df = get_data_yahoo(ticker, start, end)
    
    features = ["Open", "High", "Low", "Close"]
    scaler = preprocessing.MinMaxScaler()
    scale_features = scaler.fit_transform(df[features])
    scale_features = pd.DataFrame(columns = features, data = scale_features, index = df.index)
    depend_var = pd.DataFrame(df["Adj Close"])
    
    #Train/Test Split
    ts_split = TimeSeriesSplit(n_splits = 10)
    split_indices = ts_split.split(scale_features) #generates train/test indices for scaled df

    for train_ind, test_ind in split_indices:
        #initializes the (x,y) values of the train test split
        x_train, x_test = scale_features[:len(train_ind)], scale_features[len(train_ind): (len(train_ind) + len(test_ind))]
        y_train, y_test = depend_var[:len(train_ind)].values.ravel(), depend_var[len(train_ind): (len(train_ind)+len(test_ind))].values.ravel()

    trainX = np.array(x_train)
    testX = np.array(x_test)
    x_train = trainX.reshape(x_train.shape[0], 1, x_train.shape[1])
    x_test = testX.reshape(x_test.shape[0], 1, x_test.shape[1])

    #LSTM model 
    #Neural Network Compile and Fit
    lstm = Sequential()
    lstm.add(LSTM(32, input_shape=(1, trainX.shape[1]), activation = 'relu', return_sequences=False))
    lstm.add(Dense(1))
    lstm.compile(loss = 'mean_squared_error', optimizer = 'adam')
    plot_model(lstm, show_shapes=True, show_layer_names=True) #plots model to current working directory
    lstm.fit(x_train, y_train, epochs = 100, batch_size = 8, verbose = 1, shuffle=False)

    #Prediction & Plotting
    prediction = lstm.predict(x_test)
    
    plt.plot(y_test, label = 'True Value', color = 'firebrick')
    plt.plot(prediction, label = 'Predicted Value', color = 'mediumblue')
    plt.title(str(ticker) + " Price Prediction vs Real Values")
    plt.xlabel('Time Scale')
    plt.ylabel('US Dollar (Scaled)')
    plt.legend()
    plt.savefig('plot.png')
    plt.cla()
    
    return prediction