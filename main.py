# ------------------------------------------------------
# ---------------------- main.py -----------------------
# ------------------------------------------------------
import sys
import os
import pandas as pd
from pandas.core.tools.datetimes import to_datetime
from stock_predictor_lstm import stock_prediction
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *
from PyQt5.uic import loadUi 


class Window(QDialog):
    
    prediction_count = 0 #counter to make sure a prediction has been made before trying to save file

    def __init__(self):
        
        super().__init__()

        loadUi("stockpredictor.ui",self) #loads all the ui elements with the .ui file
        #connect buttons to functions
        self.btnRunPredict.clicked.connect(self.run_prediction)
        self.btnSavePred.clicked.connect(self.save_prediction)


    def run_prediction(self):
        ticker = self.tickerbox.text()
        start = self.frombox.text()
        end = self.tobox.text()
        try:

            to_datetime(start)
            to_datetime(end)
            if(start == "" or end == ""):
                raise Exception

        except Exception:
            
            msg = QMessageBox(self)
            msg.setWindowTitle("Error")
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Date Error")
            msg.setInformativeText("Check that your dates are in (YYYY-MM-DD) format.")
            msg.show()
            return 1
            
        try:

            if(ticker == ""):
                raise Exception
            global PREDICTION
            PREDICTION = stock_prediction(ticker, start, end)
            #self.btnRunPredict.setEnabled(False)

        except Exception:

            msg = QMessageBox(self)
            msg.setWindowTitle("Error")
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Prediction Error")
            msg.setInformativeText("Prediction failed. Make sure the stock symbol is correct and dates are valid.")
            msg.show()
            return 1

        self.prediction_count += 1
        PREDICTION = pd.DataFrame(PREDICTION)
        pixmap_plot = QPixmap('plot.png') #gets the plot saved to wd when stock_prediction was called
        self.PlotImage.setPixmap(pixmap_plot)
        #self.btnRunPredict.setEnabled(True)

    
    
    def save_prediction(self):
        if(self.prediction_count == 0): #disables saving if no prediction has been run
           return 1
        
        file_name, _ = QFileDialog.getSaveFileName(self,"Save Prediction",os.getcwd(),"CSV Files (*.csv)")
        content = PREDICTION.to_csv()

        if file_name:
            with open(file_name, 'w') as file:
                file.write(content)
        

if __name__ == "__main__":
    app = QApplication(sys.argv) 
    win = Window()
    win.show()
    sys.exit(app.exec())
