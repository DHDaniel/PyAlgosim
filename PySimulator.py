
# This module provides an interface to run simulations. It has many methods that take in the algorithm function, and run it against the specified dates, parameters, etc.

import sqlite3
import os
import copy

class PySimulator:

    def __init__(self, account, path, optional_variables=None):
        """
        Takes in the path to a database with stock information. Preferably an absolute path.
        """
        self.database = path
        self.account = account
        self.connection = None
        self.cursor = None
        self.variables = optional_variables

        # loading up the ticker list created from generating the database. The path must be correct.
        try:
            self.ticker_list = open("utilities_and_modules/tickers.json").read()
            self.ticker_list = json.loads(ticker_list)
        except:
            raise IOError("The tickers.json file could not be loaded. Please make sure that you have generated the database with the initialize script, and that you are running PySimulator from its original location.")

        # verify that database is not empty (wrong path may have created a new database)
        if os.path.isfile(self.database) != True:
            raise Exception("The path entered is not a database file. Please make sure to run initialize.py to create the stock database, and point to the correct location.")


    def __str__(self):
        """
        Simply prints out the configuration of the object. Shouldn't really be needed.
        """
        config = ""
        config += "DB path: " + str(self.database) + "\n"
        config += "Optional variables: " + str(self.variables) + "\n"
        return config

    def _connect_DB(self):
        """
        Helper function that connects to the DB. Adds a connection object and cursor object to the PySimulator object.
        """
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()

    def _disconnect_DB(self):
        """
        Helper function that closes the connection to the DB.
        """
        if self.connection and self.cursor:
            self.connection.close()
            self.connection = None
            self.cursor = None
        else:
            raise IOError("There is no current active connection to the database.")

    def _iterate_algorithm(self, algorithm, data, ticker):
        """
        Given data returned by an SQL query call, iterates through it and applies the algorithm passed. Used to apply algorithm to each stock.

        This function also takes care of keeping the Account object up to date with the latest prices, and making sure it executes trailing stops, etc.
        """

        # copying initial state of the optional variables for each stock
        if self.variables:
            variables_copy = copy.deepcopy(self.variables)
        else:
            variables_copy = None

        # each item in the "data" list will contain a tuple structured as (date, open_price, close_price, high, low, volume).

        for stock_record in data:

            # these variables are kept outside of the stock data (not passed directly on) but are passed on one at a time later
            open_price = records[1]
            close_price = records[2]

            stock_data = {
                date : record[0],
                price : open_price,
                ticker : ticker,
                transaction_fee : self.account.TRANSACTION_FEE
            }

            # updating internal prices of trading account to reflect actual selling and buying values
            self.latest_prices[stock_data.ticker] = open_price
            self.account.update(self.latest_prices)

            algorithm(stock_data, self.account, variables_copy)

            self.latest_prices[stock_data.ticker] = close_price
            self.account.update(self.latest_prices)
            stock_data["price"] = close_price

            algorithm(stock_data, self.account, variables_copy)


    def simulate(algorithm, time_start=None, time_end=None):
        """
        Function that simulates the algorithm on data. Takes in an algorithm (function) that it will run, and optional times to start and end (timeframes within the data's range).

        The algorithm should take in an object (which contains the date, open price, close price, high, low, and volume), an "account" variable which will be the PyBank account passed in to the PySimulator object, and an "optional variables" object (which will be the initial object passed in to the PySimulator object)
        """
