# stockpricepredictor
Udacity Machine Learning Engineer Nanodegree Capstone Project<br>

## Overview
This software takes as inputs a list of stocks symbols and a number of days and estimates the price of each stock after the number of days specified. <br>
Developed as the capstone project of Udacity Machine Learning Engineer Nanodegree
## Requirements

- Python 2.7
- ta-lib 0.4.9
- pandas 0.20.1
- numpy 1.11.3
- scikit-learn 0.18.1

## Project structure
This project is composed by 4 files: <br>
* `predict.py`: The main routine that predicts the value of a given stock; <br>
* `StockHistoricalDataDownloader`: Download quotes from Yahoo Finance and pre-process data; <br>
* `TechnincalIndicators`: Compute some techinical indicators on data<br>
* `Util`: Shared utility functions. <br>

## Usage
Any stock available in Yahoo website can be queried. In order to predict values, it is necessary to know what is the exchange sufix in Yahoo (https://help.yahoo.com/kb/SLN2310.html)
 In order to predict, for instance, Petrobras and Embraer (Bovespa Exchange - Brazil) 5 days ahead from the current date, the following query does the job: <br>

 ```
python .\predict.py PETR3,EMBR3 5 -i SA
 ```
where -i parameter is the Yahoo Sufix for each exchange.
<br>
Note that if the query contains multiples stocks, all of them must me traded in the same exchange.

In case of the exchange has no suffix, just ommit the parameter.
For instance, quering Google data from Nasdaq for the period between January 1st, 2017 and December 4th, 2017, and then to predict the price for the next day (5th December, 2017):

 ```
python .\predict.py GOOG 1 -s 2017-01-01 -e 2017-12-04
 ```
Start and end periods are optional. Thus, you can specify only one of them.

For additional help, please type
 ```
python .\predict.py -h
 ```
