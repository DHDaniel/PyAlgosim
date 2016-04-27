
# This module provides a trading account class to be used
# in the simulator. It is meant to simulate a trading account.
# It should be imported into programs using the import statement.

# AUTHOR: Daniel Hernandez H.
# LICENSE: MIT License (https://opensource.org/licenses/MIT)


class Account:

    """A simple trading account for use in PyAlgosim

    :param funds: the starting funds of the account, e.g 100,000
    """

    def __init__(self, funds):

        # funds to work with and transaction number
        self.funds = funds
        self.transactions = 0

        self.TRANSACTION_FEE = 6.99

        # stocks_owned is in the form
        # { "AAPL" : [100, 113.27], "TGT" : [50, 46.55]}
        # where in the list, the structure is [quantity, price]
        self.stocks_owned = {}

    def __str__(self):
        return_str = ""
        return_str += "Funds in account: " + str(round(self.funds, 2)) + "\n"
        return_str += "Stocks owned: " + str(self.stocks_owned)
        return return_str

    def buy_stock(self, ticker, quantity, price):
        # checking funds are available
        if self.funds - ((quantity * price) + self.TRANSACTION_FEE) >= 0:
            self.funds -= ((quantity * price) + self.TRANSACTION_FEE)
            self.transactions += 1
            self.stocks_owned[ticker] = [quantity, price]
        else:
            return -1

    def sell_stock(self, ticker, quantity, current_price):
        try:
            # checking if quantity is owned
            if self.stocks_owned[ticker][0] - quantity >= 0:
                self.funds += (quantity * current_price) - self.TRANSACTION_FEE
                self.stocks_owned[ticker][0] -= quantity
                # checking if no more stock is owned
                if self.stocks_owned[ticker][0] == 0:
                    del self.stocks_owned[ticker]
        # if this happens, it is probably due to the account not having
        # the stock that it is trying to sell
        except:
            return -1

    # sells all stocks owned
    def sell_all(self, latest_prices):
        copy = self.stocks_owned
        for ticker, val in copy.items():
            self.funds += (self.stocks_owned[ticker][0] * latest_prices[ticker]) - self.TRANSACTION_FEE
            del self.stocks_owned[ticker]
