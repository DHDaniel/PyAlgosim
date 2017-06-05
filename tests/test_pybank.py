
import unittest
import sys
import os

# to be able to import PyBank
parent_path = os.path.dirname(os.getcwd())
sys.path.append(parent_path)

import PyBank


class PyBankTestCase(unittest.TestCase):

    def setUp(self):
        self.account = PyBank.Account()
        self.start_funds = self.account.funds
        self.fee = self.account.TRANSACTION_FEE
        self.test_data = [{"AAPL" : 120.00}, {"AAPL" : 110.00}, {"AAPL" : 90.00}]
        self.account.update(self.test_data[0], "AAPL")

    def tearDown(self):
        del self.account

    def test_buy_stock(self):
        self.account.buy_stock("AAPL", 100)
        q = self.account.stocks_owned["AAPL"]["quantity"]
        bought_p = self.account.stocks_owned["AAPL"]["bought_p"]

        self.assertEqual(self.account.funds, self.start_funds - ((100 * 120.00) + self.fee), "Funds in account do not match price of stock and transaction.")

        self.assertEqual(q, 100, "Quantity of stock owned not equal to transaction.")

        self.assertEqual(bought_p, self.test_data[0]["AAPL"], "Bought price not equal to the price when transaction occured.")

    def test_buy_multiple_stock(self):
        self.account.buy_stock("AAPL", 100)
        self.account.update(self.test_data[1], "AAPL")
        self.account.buy_stock("AAPL", 100)

        current_p = self.account.stocks_owned["AAPL"]["current_p"]
        bought_p = self.account.stocks_owned["AAPL"]["bought_p"]
        q = self.account.stocks_owned["AAPL"]["quantity"]

        self.assertEqual(self.test_data[1]["AAPL"], current_p, "Stock current price does not match latest price.")
        self.assertEqual(bought_p, 115.00, "Averaged bought price is incorrect.")
        self.assertEqual(q, 200, "Quantity is incorrect.")

    def test_sell_stock(self):
        self.account.buy_stock("AAPL", 100)
        self.account.sell_stock("AAPL", 100)

        # if you compare the values in assertEqual, they will evaluate to False. It may be an error with floating point numbers, hence why the round function is used

        self.assertEqual(round(self.start_funds - (2 * self.fee)), round(self.account.funds), "Account did not properly execute sell order.")

        self.assertTrue(len(self.account.stocks_owned) == 0, "Stock was not sold properly.")

    def test_trailing_stop_points(self):
        self.account.buy_stock("AAPL", 100)
        self.account.trailing_stop("AAPL", 50, 40)

        self.account.update(self.test_data[1], "AAPL")

        self.assertTrue(len(self.account.stocks_owned["AAPL"]["options"]) > 0, "Trailing stop order was not registered in options.")

        self.account.trailing_stop("AAPL", 50, 30)
        self.account.update(self.test_data[2], "AAPL")

        self.assertTrue(len(self.account.stocks_owned) == 0, "Stock was not sold and is still in account.")

    def test_sell_all_stock(self):
        self.account.buy_stock("AAPL", 100)
        self.account.sell_all()

        self.assertTrue(len(self.account.stocks_owned) == 0, "Stocks were not properly sold.")

    def test_value(self):
        self.account.buy_stock("AAPL", 100)
        self.assertEqual(100 * 120.00, self.account.value(), "Stock value does not match the value of shares bought.")

        # update prices
        self.account.update(self.test_data[1], "AAPL")

        self.account.buy_stock("AAPL", 100)

        # price has now changed
        self.assertEqual((200 * 110.00), self.account.value(), "Stock value does not match the value of shares bought (multiple purchases).")



# running tests
suite = unittest.TestLoader().loadTestsFromTestCase(PyBankTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)
