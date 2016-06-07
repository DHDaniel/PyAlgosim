
# THIS IS WHERE THE CODE FOR THE ALGORITHM GOES. All the code you wish
# to backtest goes in this file. The code below will be executed for all
# the existing records (days) of S&P 500 stocks from 1998 - 2013. In other words,
# it will be executed EVERY DAY from 1998 to 2013 on ALL of the stocks.

# VARIABLES THAT YOU CAN USE:
# date (the date of the certain day. The format is YEARMONTHDAY, all together, e.g "19980102". Note it is a string)
# ticker (the stock's ticker, used for purchasing or selling)
# open_price (the stock's opening price of the day)
# close_price (the stock's closing price of the day)
# high (the stock's high price of the day)
# low (the stock's low price of the day)
# vol (the stock's volume)
# account (your bank account)
# transaction_fee

# BESIDE THESE VALUES, you can use your own variables to keep track of any
# averages, or simply variables you want to remember. Write these variables in
# the "init" section. The "init" function will be called for every
# separate ticker

# HOW TO PURCHASE/SELL
# To purchase or sell any stocks: account.sell_stock(ticker, quantity_desired, price)
# OR account.buy_stock(ticker, quantity_desired, price). Note that "ticker" is already provided
# to you as a variable, but you must provide the quantity desired and the price. For price,
# you should use any of the price-related variables provided above. "account" will
# perform erroneously if you attempt to sell stock you don't own, or more than you
# own. Refer to the pybank.py documentation.

# REMEMBER
# remember to take into account your funds - you cannot continue buying
# forever, or the account will throw an error. Refer to the documentation of
# pybank

# should RETURN a dictionary of optional variables, if needed


def init():
    return {}

# the main algorithm that will be run for each stock, every day
# This is just an example to illustrate how to use this function

"""
The algorithm below buys the stock AAPL if it does not already own it. It will
buy 100 shares at the very start of the program (since it doesn't own any) and
will hold on to these shares. Before buying the shares though, it is making sure
that the account has enough funds to do so, in the second "if" statement. It is then
buying the AAPL shares at the day's opening price.
"""


def main(date, account, ticker, current_price, high, low, vol, transaction_fee, optional_variables={}):
    if ticker == "AAPL" and ticker not in account.stocks_owned:
        if account.funds - ((100 * current_price) + transaction_fee) >= 0:
            account.buy_stock(ticker, 100)
