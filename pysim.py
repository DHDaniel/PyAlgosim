
import sqlite3
import json

from utilities_and_modules import pybank
import pysimcode


if __name__ == '__main__':

    # connecting to database
    conn = sqlite3.connect('utilities_and_modules/stocks.db')
    cur = conn.cursor()

    ticker_list = open("utilities_and_modules/tickers.json").read()

    ticker_list = json.loads(ticker_list)

    # initiating account with 100,000
    # CHANGE THAT VALUE IF YOU WANT TO
    account = pybank.Account(100000)
    start_val = account.funds

    latest_prices = {}

    for ticker in ticker_list:
        records = cur.execute("SELECT * FROM " + '"' + str(ticker) + '";')
        latest_prices[ticker] = 0

        # variables for algorithm
        open_price = 0
        close_price = 0
        high = 0
        low = 0
        vol = 0

        optional_variables = pysimcode.init()
        print "Backtesting " + str(ticker) + "..."

        for record in records:

            # variables that can be used in the algorithm
            date = str(record[0])
            open_price = record[1]
            close_price = record[2]
            high = record[3]
            low = record[4]
            vol = record[5]
            transaction_fee = account.TRANSACTION_FEE

            latest_prices[ticker] = close_price

            # algorithm code is run
            pysimcode.main(date, account, ticker, open_price, close_price,
                           high, low, vol, transaction_fee, optional_variables)

    account.sell_all(latest_prices)

    # Printing account status
    print account

    profit = account.funds - start_val
    profit_per = round(profit / start_val * 100, 2)

    print "Profit: " + str(round(profit, 2)) + " (" + str(profit_per) + ")"
    print "Transactions: " + str(account.transactions)
