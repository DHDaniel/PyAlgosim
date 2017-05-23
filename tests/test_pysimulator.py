
import sys
import unittest
import os

parent_path = os.path.dirname(os.getcwd())
sys.path.append(parent_path)

import PySimulator
import PyBank

class PySimulatorTestCase(unittest.TestCase):

    def test_db_connections(self):
        self.assertRaises(Exception, PySimulator.PySimulator, PyBank.Account(), "gibberish")

        pysim = PySimulator.PySimulator(PyBank.Account(), "test.db")
        self.assertRaises(IOError, pysim._disconnect_DB)




# running tests
suite = unittest.TestLoader().loadTestsFromTestCase(PySimulatorTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)
