
import unittest
import sys
import os

# to be able to import PyBank
parent_path = os.path.dirname(os.getcwd())
sys.path.append(parent_path)

from utilities_and_modules import PyBank

acc = PyBank.Account()
print acc
