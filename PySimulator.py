
# This module provides an interface to run simulations. It has many methods
# that take in the algorithm function, and run it against the specified dates, parameters,
# etc.
import sqlite3
import os

class PySimulator:

    def __init__(self, account, path, optional_variables=None):
        """
        Takes in the path to a database with stock information. Preferably an absolute path.
        """
        self.database = path
        self.account = account

        # verify that database is not empty (wrong path may have created a new database)
        if os.path.isfile(self.database) != True:
            raise Exception("The path entered is not a database file. Please make sure to run initialize.py to create the stock database, and point to the correct location.")

        if optional_variables:
            self.variables = optional_variables

    def __str__(self):
        """
        Simply prints out the configuration of the object. Shouldn't really be needed.
        """
        config = ""
        config += "DB path: " + str(self.database)
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
        else:
            raise IOError("There is no current active connection to the database.")

    def _iterate_algorithm(self, algorithm, data):
        """
        Given data returned by an SQL query call, iterates through it and applies the algorithm passed.
        """
        pass

    def simulate(algorithm, time_start=None, time_end=None):
        """
        Function that simulates the algorithm on data. Takes in an algorithm (function) that it will run, and optional times to start and end (timeframes within the data's range)
        """
        pass
