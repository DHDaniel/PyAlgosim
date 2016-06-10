
# THIS IS WHERE THE CODE FOR THE ALGORITHM GOES. All the code you wish
# to backtest goes in this file. The code below will be executed for all
# the existing records (days) of S&P 500 stocks from 1998 - 2013. In other words,
# it will be executed EVERY DAY from 1998 to 2013 on ALL of the stocks.

# VARIABLES THAT YOU CAN USE:
# date (the date of the certain day. The format is YEARMONTHDAY, all together, e.g "19980102". Note it is a string)
# ticker (the stock's ticker, used for purchasing or selling)
# current_price (the stock's current price)
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
# To purchase or sell any stocks: account.sell_stock(ticker, quantity_desired)
# OR account.buy_stock(ticker, quantity_desired). Note that "ticker" is already provided
# to you as a variable, but you must provide the quantity desired. "account" will
# raise errors if you attempt to sell stock you don't own, or more than you
# own. Refer to the PyBank.py documentation for these errors, on the website.

# REMEMBER
# remember to take into account your funds - you cannot continue buying
# forever, or the account will raise an error.

def init():

    # should RETURN a dictionary of optional variables, if needed
    return {}

# the main algorithm that will be run for each stock, every day
# This is just an example to illustrate how to use this function

"""
The algorithm below buys the stock AAPL if it does not already own it. It will
buy 100 shares at the very start of the program (since it doesn't own any) and
will hold on to these shares. Before buying the shares though, it is making sure
that the account has enough funds to do so, in the second "if" statement. It is then
buying the AAPL shares at the day's current price.
"""

def main(date, account, ticker, current_price, high, low, vol, transaction_fee, optional_variables={}):
    if ticker == "AAPL" and ticker not in account.stocks_owned:
        if account.funds - ((100 * current_price) + transaction_fee) >= 0:
            account.buy_stock(ticker, 100)
