
# This module provides a trading account class to be used
# in the simulator. It is meant to simulate a trading account.
# It should be imported into programs using the import statement.

# AUTHOR: Daniel Hernandez H.
# LICENSE: MIT License (https://opensource.org/licenses/MIT)

TRANSACTION_FEE = 6.99

class Account:

    def __init__(self, funds):

        # funds to work with and transaction number
        self.funds = funds
        self.transactions = 0

        # stocks_owned is in the form
        # { "AAPL" : [100, 113.27], "TGT" : [50, 46.55]}
        # where in the list, the structure is [quantity, price]
        self.stocks_owned = {}

    def __str__(self):
        return_str = ""
        return_str += "Funds in account: " + str(self.funds) + "\n"
        return_str += "Stocks owned: " + str(self.stocks_owned)
        return return_str

    def getValue(self):
        return self.funds

    def getTransactions(self):
        return self.transactions

    def buyStock(self, ticker, quantity, price):
        # checking funds are available
        if self.funds - ((quantity * price) + TRANSACTION_FEE) >= 0:
            self.funds -= ((quantity * price) + TRANSACTION_FEE)
            self.transactions += 1
            self.stocks_owned[ticker] = [quantity, price]
        else:
            return -1

    def sellStock(self, ticker, quantity, current_price):
        try:
            # checking if quantity is owned
            if self.stocks_owned[ticker][0] - quantity >= 0:
                self.funds += (quantity * current_price) - TRANSACTION_FEE
                self.stocks_owned[ticker][0] -= quantity
                # checking if no more stock is owned
                if self.stocks_owned[ticker][0] == 0:
                    del self.stocks_owned[ticker]
        # if this happens, it is probably due to the account not having
        # the stock that it is trying to sell
        except:
            return -1
