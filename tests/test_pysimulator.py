
import sys
import unittest
import os

parent_path = os.path.dirname(os.getcwd())
sys.path.append(parent_path)

import PySimulator
import PyBank

class PySimulatorTestCase(unittest.TestCase):

    def test_db_connections(self):

        pysim = PySimulator.PySimulator(PyBank.Account(), db_path="test.db", ticker_list_path="../utils/tickers.json")
        self.assertRaises(IOError, pysim._disconnect_DB)

    def test_initial_setup(self):
        # testing ticker list path
        self.assertRaises(IOError, PySimulator.PySimulator, PyBank.Account(), db_path="test.db", ticker_list_path="gibberish")

        # testing db path
        self.assertRaises(Exception, PySimulator.PySimulator, PyBank.Account(), db_path="gibberish", ticker_list_path="../utils/tickers.json")

        # testing PyBank error
        self.assertRaises(TypeError, PySimulator.PySimulator, "not a PyBank object", db_path="test.db", ticker_list_path="../utils/tickers.json")



# running tests
suite = unittest.TestLoader().loadTestsFromTestCase(PySimulatorTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)
