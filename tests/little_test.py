
# move this program to the root directory of the project for it to work

import PyBank
import PyAlgosim
import datetime

account = PyBank.Account()
simulator = PyAlgosim.PyAlgosim(account)

def my_algorithm(stock_data, trade_acc, variables):

    if stock_data["ticker"] not in trade_acc.stocks_owned:
        trade_acc.buy_stock(stock_data["ticker"], 1)

simulator.simulate(my_algorithm, time_start=datetime.date(2013, 1, 1))

print account.report(verbose=False)
