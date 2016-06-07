
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

        # dictionary will house all the latest prices of all the stocks,
        # making it easier to buy and sell stock. You won't need to provide
        # the price you want to buy the stock at, making the API simpler to use.
        self.latest_prices = {}

        # stocks_owned is in the form
        # { "AAPL" : [100, 113.27], "TGT" : [50, 46.55]}
        # where in the list, the structure is [quantity, price]
        self.stocks_owned = {}

    def __str__(self):
        return_str = ""
        return_str += "Funds in account: " + str(round(self.funds, 2)) + "\n"
        return_str += "Stocks owned: " + str(self.stocks_owned)
        return return_str

    def update(self, latest_prices):
        self.latest_prices = latest_prices
        for ticker, info in self.stocks_owned.items():
            if ticker in self.latest_prices:
                # accessing the price of the current stock
                self.stocks_owned[ticker]["current_p"] = self.latest_prices[ticker]

    def buy_stock(self, ticker, quantity):
        # checking funds are available
        price = self.latest_prices[ticker]
        if self.funds - ((quantity * price) + self.TRANSACTION_FEE) >= 0:
            self.funds -= ((quantity * price) + self.TRANSACTION_FEE)
            self.transactions += 1
            self.stocks_owned[ticker] = {
                "q": quantity, "bought_p": price, "current_p": price}
        else:
            return -1

    def sell_stock(self, ticker, quantity):
        try:
            current_price = self.stocks_owned[ticker]["current_p"]
            # checking if quantity is owned
            if self.stocks_owned[ticker]["q"] - quantity >= 0:
                self.funds += (quantity * current_price) - self.TRANSACTION_FEE
                self.stocks_owned[ticker]["q"] -= quantity
                # checking if no more stock is owned
                if self.stocks_owned[ticker]["q"] == 0:
                    del self.stocks_owned[ticker]
        # if this happens, it is probably due to the account not having
        # the stock that it is trying to sell
        except:
            return -1

    # sells all stocks owned
    def sell_all(self):
        copy = self.stocks_owned
        for ticker, val in copy.items():
            self.funds += (self.stocks_owned[ticker]["q"] *
                           self.stocks_owned[ticker]["current_p"]) - self.TRANSACTION_FEE
            del self.stocks_owned[ticker]
