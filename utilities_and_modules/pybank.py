
# This module provides a trading account class to be used
# in the simulator. It is meant to simulate a trading account.
# It should be imported into programs using the import statement.

# AUTHOR: Daniel Hernandez H.
# LICENSE: MIT License (https://opensource.org/licenses/MIT)

### HELPER FUNCTIONS ###

def update_trailing_stop(account, ticker):
    current_price = account.stocks_owned[ticker]["current_p"]
    order = account.stocks_owned[ticker]["options"]["trailing_stop"]

    # if price has gone down
    if order["highest"] > current_price:

        # calculating bottom limit based on percentage
        if order["percentage"] == True:
            bottom_limit = order["highest"] - (order["highest"] * order["points"])
        else:
            bottom_limit = order["highest"] - order["points"]

        # executing AND deleting the order
        if current_price <= bottom_limit:
            account.sell_stock(ticker, order["quantity"])
            # in case the whole stock has been deleted, use an 'if'
            if ticker in account.stocks_owned:
                del account.stocks_owned[ticker]["options"]["trailing_stop"]

    # if price has gone up
    else:
        account.stocks_owned[ticker]["options"]["trailing_stop"]["highest"] = current_price


### END OF HELPER FUNCTIONS ###

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
        # the price you want to buy the stock at, making the API simpler to
        # use.
        self.latest_prices = {}

        # stocks_owned is in the form
        # { "AAPL" : {"quantity" : 100, "bought_p" : 110.56, "current_p" : 132.00, "options" : {} }}}
        # the "options" option will house data for special orders, such as a trailing stop,
        # for the update() function to easily access.
        self.stocks_owned = {}

    def __str__(self):
        return_str = ""
        return_str += "Funds in account: " + str(round(self.funds, 2)) + "\n"
        return_str += "Stocks owned: " + str(self.stocks_owned)
        return return_str

    def update(self, latest_prices):
        """Vital function updates all the stock prices of the account.
        Furthermore, it also takes care of automated trades like a trailing stop.
        """
        self.latest_prices = latest_prices
        for ticker, info in self.stocks_owned.items():
            if ticker in self.latest_prices:
                # updating the price of the current stock
                self.stocks_owned[ticker][
                    "current_p"] = self.latest_prices[ticker]
                if "trailing_stop" in info["options"]:
                    update_trailing_stop(self, ticker)


    def buy_stock(self, ticker, quantity):
        try:
            # checking funds are available
            price = self.latest_prices[ticker]
            if self.funds - ((quantity * price) + self.TRANSACTION_FEE) >= 0:
                self.funds -= ((quantity * price) + self.TRANSACTION_FEE)
                self.transactions += 1
                if ticker not in self.stocks_owned:
                    self.stocks_owned[ticker] = {
                        "quantity": quantity, "bought_p": price, "current_p": price, "options" : {}}
                else:
                    # for calculating averaged price
                    old_amount = (self.stocks_owned[ticker]["quantity"] *
                                  self.stocks_owned[ticker]["bought_p"])
                    new_amount = quantity * price

                    # calculating average bought price
                    average_bought_p = float((old_amount + new_amount) /
                                            (self.stocks_owned[ticker]["quantity"] + quantity))

                    # updating stock holding values
                    self.stocks_owned[ticker]["quantity"] += quantity
                    self.stocks_owned[ticker]["bought_p"] = average_bought_p

            else:
                raise ValueError("You do not have enough funds to make this purchase:", ticker,
                                price, quantity, self)

        # outputting error values
        except ValueError as e:
            print "ERROR:", type(e)
            print e.args[0], "Buy", e.args[1], "*", e.args[3], "at", e.args[2]
            print "Funds in account:", e.args[4].funds
            quit()

        except:
            print "ERROR: the stock you tried to buy does not exist."
            quit()

    def sell_stock(self, ticker, quantity):
        try:
            if ticker not in self.stocks_owned:
                raise KeyError("You do not own the stock you are trying to sell:", ticker)

            if quantity == "all":
                quantity = self.stocks_owned[ticker]["quantity"]

            current_price = self.stocks_owned[ticker]["current_p"]
            # checking if quantity is owned
            if self.stocks_owned[ticker]["quantity"] - quantity >= 0:
                self.funds += (quantity * current_price) - self.TRANSACTION_FEE
                self.stocks_owned[ticker]["quantity"] -= quantity
                # checking if no more stock is owned
                if self.stocks_owned[ticker]["quantity"] == 0:
                    del self.stocks_owned[ticker]
            else:
                raise ValueError("You cannot sell more stock than what you own.", ticker,
                                quantity, self)
            self.transactions += 1

        # selling more stock than what is owned
        except ValueError as e:
            print "ERROR:", type(e)
            print e.args[0]
            print "Attempting to sell:", e.args[2], "shares of", e.args[1]
            print "Shares owned:", e.args[3].stocks_owned[e.args[1]]["quantity"]
            quit()

        # selling stock which you don't own
        except KeyError as e:
            print "ERROR:", type(e)
            print e.args[0], e.args[1]
            quit()

    def trailing_stop(self, ticker, quantity, points, percentage=False):

        """Will set a trailing stop based on the price provided, or, if
        the percentage option is set to True, on the percentage provided.
        This function does NOT actually check the trailing stop conditions -
        that is what the helper function is for."""

        try:
            if self.funds - self.TRANSACTION_FEE >= 0:
                self.transactions += 1
                self.funds -= self.TRANSACTION_FEE

                if "trailing_stop" not in self.stocks_owned[ticker]["options"]:
                    self.stocks_owned[ticker]["options"] = {"trailing_stop" :
                     {"percentage" : False, "points" : points, "highest" : self.stocks_owned[ticker]["current_p"],
                     "quantity" : quantity}}

                # if order already exists, then they will be merged into one using
                # the new order's data
                else:
                    self.stocks_owned[ticker]["options"]["trailing_stop"]["quantity"] += quantity
                    self.stocks_owned[ticker]["options"]["trailing_stop"]["points"] = points

                # if you try to sell more than what you own
                if (self.stocks_owned[ticker]["options"]["trailing_stop"]["quantity"] >
                    self.stocks_owned[ticker]["quantity"]):
                    raise ValueError("You cannot sell more stock than what you own.", ticker,
                                    quantity, self)

                if percentage:
                    # converting to percentage
                    points = points / 100.0
                    self.stocks_owned[ticker]["options"]["trailing_stop"]["percentage"] = True
                    self.stocks_owned[ticker]["options"]["trailing_stop"]["points"] = points

            # if account doesn't have enough money to execute
            else:
                raise IndexError("You do not have enough funds to place this order.")

        # selling more stock than what is owned
        except ValueError as e:
            print "ERROR:", type(e)
            print e.args[0]
            print "Attempting to sell:", e.args[2], "shares of", e.args[1]
            print "Shares owned:", e.args[3].stocks_owned[e.args[1]]["quantity"]
            quit()

        except IndexError as e:
            print e.args[0]
            quit()

    def sell_all(self):
        """Sells all stocks owned"""
        copy = self.stocks_owned
        for ticker, val in copy.items():
            self.funds += (self.stocks_owned[ticker]["quantity"] *
                           self.stocks_owned[ticker]["current_p"]) - self.TRANSACTION_FEE
            self.transactions += 1
            del self.stocks_owned[ticker]
