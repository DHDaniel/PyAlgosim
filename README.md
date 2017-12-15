# [PyAlgosim](http://dhdaniel.github.io/PyAlgosim/)
#### The Python-built high frequency trading backtester
PyAlgosim provides a simple way for amateur high frequency traders to get a feel for automated trading. It is meant to be simple to use, and quick to produce results. We are always accepting contributions and suggestions to make the software better!

PyAlgosim allows you to backtest trading strategies accross S&P 500 data from **January 2nd, 1998** to **August 8th, 2013**!

## Contents
Quick links to parts of the documentation:
- [Getting started](#getting-started)
    - [Requirements](#requirements)
    - [Project structure](#project-structure)
    - [Initialization](#initialization)
- [PyAlgosim, the simulator](#pyalgosim-the-simulator)
    - [The PyAlgosim API](#the-pyalgosim-api)
- [PyBank, the trading account](#pybank-the-trading-account)
    - [The PyBank API](#the-pybank-api)
- [PyAlgosim and PyBank: putting it together](#pyalgosim-and-pybank-putting-it-together)
    - [Creating a trading algorithm](#creating-a-trading-algorithm)
- [Contributing](#contributing)

# Getting started
To get started using the PyAlgosim high frequency trading backtester, you must download the most recent version of the software. You can easily do this by either cloning the repository from GitHub [here](https://github.com/DHDaniel/PyAlgosim) or directly download the latest release from [here](https://github.com/DHDaniel/PyAlgosim/releases).

## Requirements
All that is required to start using PyAlgosim is:
- Python 2.7.X

## Project structure
On downloading, the project has a very specific structure that you should keep for everything to work as intended. Alternatively, you could set up your own structure, but it would require additional configuration (and would probably be a pain). After initialization, the project structure should look like this:

```bash
.
├── LICENSE
├── PyBank.py
├── PyAlgosim.py
├── README.md
├── raw_data/
├── tests/
└── utils/
    ├── __init__.py
    ├── initialize.py
    ├── reset.py
    ├── stocks.db
    └── tickers.json
```
What's inside `tests/` and `raw_data/` is not very important. However, note that the `initialize.py` script accesses the `raw_data/` directory to build the database, so you should keep this structure as is.

For PyAlgosim to work, the project structure **should stay like this**. If you move the `stocks.db` file or the `tickers.json` file, you will need to reference them during the creation of a PyAlgosim object.

The program in which you wish to use the `PyAlgosim` and `PyBank` modules should ideally reside in the top-level directory of the project (that is, in the same directory as the PyBank and PyAlgosim files) for everything to run as smoothly as possible.

## Initialization
To get PyAlgosim working, you must initialize the project from the directory in which you have placed it. **All the backtesting that you wish to do should be done from within this directory**, as specified later on in the documentation.

Initialization is required to create the database file which will hold all the stock information, and to create the ticker list that the backtester will use throughout the simulations. To initialize PyAlgosim, go to the command line and type the following commands:

```bash
$ cd ~/path/to/PyAlgosim
$ cd ./utils/
$ python initialize.py
```

That should run the initialization script, which will use the `raw_data` directory to generate the required files. Once it is done, you can start using PyAlgosim!

### Why is initialization necessary?
The database file that PyAlgosim uses to backtest algorithms is too big to upload to GitHub, so the project generates the database file during initialization, using raw .csv files which are much smaller.

# PyAlgosim, the simulator
PyAlgosim is the module that takes care of running the algorithm that you wish to backtest. Using it is very simple and intuitive. First, you must import the module into your program - **note that your program should be created in the same directory as the PyAlgosim.py file for the program to properly communicate with the generated database and ticker file**.

```python
import PyAlgosim
```

## The PyAlgosim API
#### _class_ PyAlgosim.PyAlgosim(_account_, [_db_path_, _ticker_list_path_, _variables_])
This method initializes the PyAlgosim simulator. It returns an object that will function as the backtester for your algorithm.

**account** - a PyBank object. The trading account that you wish to use during the simulator.
**db_path** (optional) - the path to the database file you are using. Should be a `string`. If you used the initialize.py script and are running the program from PyAlgosim.py 's directory, then you shouldn't have to set this explicitly. Defaults to `./utils/stocks.db`.
**ticker_list_path** (optional) - the path to the ticker list file that should have been generated during the initialize.py script. Should be a `string`. Again, if you followed the initial setup instructions, you shouldn't have to explicitly set this. Defaults to `./utils/tickers.json`.
**variables** (optional) - an dictionary "template" (dictionary with empty fields) with any optional variables that you want your algorithm to have access to during the simulation. For example, the dictionary could store recurring averages, statistics, record highs and lows, etc. Defaults to `None`.

For example:
```python
import PyAlgosim
import PyBank

trade_account = PyBank.Account()

# this will use all of the default configuration, assuming all files have been kept in their original place
backtester = PyAlgosim.PyAlgosim(trade_account)

# this uses custom configuration for the stock database and the ticker list json file
backtester = PyAlgosim.PyAlgosim(trade_account, db_path="/some/other/path/mydata.db", ticker_list_path="/some/other/path/mytickers.json")

# this uses a variables dictionary, for potentially calculating a simple moving average for 50 days and the highest and lowest prices of the stock. Note that it is a "template" in the sense that it is empty - it will be provided exactly like that at the start of backtesting each stock.
my_variables = {
    highest_price = 0
    lowest_price = 0
    past_50_prices = []
}
backtester = PyAlgosim.PyAlgosim(trade_account, variables=my_variables)
```

#### _classmethod_ PyAlgosim.simulate(_algorithm_[, _time_start_, _time_end_])
This method performs the backtesting on the algorithm provided, using the data specified in `time_start` and `time_end`.

**algorithm** - the name of the algorithm (function) that you wish to backtest. The function provided as an algorithm must take in the following variables in the order specified:
- A **stock data** dictionary that contains information about the stock being processed. The object will contain the following properties:
    - **date** - an integer of the form YYYYMMDD. The historical date of the data.
    - **price** - a float. The current price of the stock.
    - **ticker** - a string containing the ticker of the stock.

- A **PyBank.Account()** object, which will be the account you pass as an argument to PyAlgosim. The algorithm can access the account using this parameter.
- A **variables dictionary**, which will be the variables template dictionary that you provide PyAlgosim. The template will be used at the start of backtesting for each ticker (it will not remain the same across _all_ tickers, just the ticker that is being simulated at the time. Keep this in mind).

**time_start, time_end** - optional parameters to specify the time to start and end the backtesting. They should be **datetime** objects within the range of the data being used. If they exceed the ranges, or the date doesn't exist (e.g the market was closed on the date), then PyAlgosim will just use the closest date to the one specified. The range of data in the database is from **January 2nd, 1998 to August 9th, 2013**.

Example uses:
```python
import PyAlgosim
import PyBank
import datetime

trade_acc = PyBank.Account()
backtester = PyAlgosim.PyAlgosim(trade_acc)

# this algorithm checks to see if you currently own the stock, and if you have enough money to buy one share of the stock. It then buys one share if the conditions are met.
def algorithm(stock, account, variables):
    if stock["ticker"] not in account.stocks_owned and account.funds - (stock["price"] + account.TRANSACTION_FEE) > 0:
        account.buy_stock(stock["ticker"], 1)

# Here, the algorithm is passed to the simulate() method. Only a start date is provided.
backtester.simulate(algorithm, datetime.date(2008, 1, 1) )
```

-----


# PyBank, the trading account
The PyBank module allows you to simulate a trading account, working together with the PyAlgosim module. It is what you will use to buy stock, sell stock, and other things you might to in a real-life trading account. The API is simple and intuitive to use.

It should be noted that the PyBank module cannot be used on its own. It should be used in conjunction with the PyAlgosim module for the backtesting to work properly.

## The PyBank API

#### _class_ PyBank.Account([_funds=100000_, _transaction_fee=6.99_])
Returns an Account object, which you can perform various actions on, like in a trading account. Takes in two optional arguments:

**funds** - float that defaults to 100,000. This is the initial funds that you wish the account to start out with.
**transaction_fee** - float that defaults to 6.99. This is the value of the transaction fees charged by the trading account (charged on every trade you perform).

```python
import PyBank

# creating an account with different initial funds and transaction fee
account = PyBank.Account(funds=10000, transaction_fee=9.99)
```

#### _classmethod_ Account.buy_stock(_ticker_, _quantity_)
Method to buy a stock. An error will be thrown if you attempt to buy more shares than what your funds allow you to.

**ticker** - a `string` specifying the ticker symbol, e.g `"AAPL"`.
**quantity** - an `int` specifying the number of shares to buy.

#### _classmethod_ Account.sell_stock(_ticker_, _quantity_)
Method to sell a stock. An error will be thrown if you attempt to sell a stock that you do not own, or attempt to sell too much of a stock.

**ticker** - a `string` specifying the ticker symbol, e.g `"AAPL"`.
**quantity** - an `int` specifying the number of shares to buy. Alternatively, you can pass the string `"all"` to sell all the stock you own of that ticker.

#### _classmethod_ Account.trailing_stop(_ticker_, _quantity_, _points_[, _percentage=False_)
Method to set a trailing stop order on a stock, selling it when it goes below a certain point. A more detailed explanation of how a trailing stop works can be found [here](http://www.investopedia.com/terms/t/trailingstop.asp).

**ticker** - a `string` specifying the stock to place the order on. E.g `"AAPL"`.
**quantity** - an `int` specifying the amount of stock to sell.
**points** - a `float` sepcifying the number of points that the stock can fall before the sell order executing. For example, setting this to `1` would mean that a stock priced at `101` would sell if it dropped to `100`.
**percentage** - optional, defaults to `False`. Indicates whether the **points** parameter should be treated as a percentage or not i.e the stock would need to fall by the percentage specified for it to sell.

_**Note**_: If you attempt to place two trailing stop orders on the same stock, they will be merged into one - the latest one placed.

Examples using the previous methods:
```python

# Note: all the operations that the account can do only work inside the algorithm inside PyAlgosim (it does not have the relevant data if used outside of PyAlgosim). However, they are shown outside of PyAlgosim here for illustration purposes.

import PyBank

account = PyBank.Account()

# buy 100 shares of Apple
account.buy_stock("AAPL", 100)

# sell those 100 shares - way #1
account.sell_stock("AAPL", 100)
# sell those 100 shares - way #2
account.sell_stock("AAPL", "all")


account.buy_stock("AAPL", 100)
# this indicates the account to sell the stock if it drops 5% in price.
account.trailing_stop("AAPL", 100, 5, percentage=True)
```

#### _classmethod_ Account.sell_all()
Sells all the stocks owned.

#### _classmethod_ Account.report([verbose=False])
Print out a report to the console on the trading activities of the account at that moment in time. It presents information such as the total return (based on the value of stocks held and funds in the account), average market return during that same time period, and number of transactions. If **verbose** is set to `True`, each stock currently owned by the account is printed to the console, with the average profit made reported on each one.

# PyAlgosim and PyBank: putting it together

The two modules are used in conjunction to perform backtesting on algorithms. The following examples will illustrate how to do this.

## Creating a trading algorithm
When creating your trading algorithm, you must keep a few things in mind for everything to work properly. Specifically,
- Always checking whether you have enough money to buy the stock.
- Correctly using the data provided.
- Understand how the `variables` dictionary works

If you make a purchase which you don't have enough money for, the program will raise an error and stop. For your trading strategy to work, you do not want this. Furthermore, you should keep in mind how the backtesting works. The trading algorithm runs separately for each stock (it will only have access to one ticker at a time). When the trading algorithm begins running on any one of the tickers, the template dictionary variable (if provided) will be available to the algorithm. This variable is **separate** for each stock - you will not have access to the variable dictionary of other stocks.

```python
import PyBank
import PyAlgosim

# template dictionary for variables
myvariables = {
    "high" : float("-inf"),
    "low" : float("inf")
}

account = PyBank.Account()
backtester = PyAlgosim.PyAlgosim(account, variables=myvariables)

# this is an example of keeping track of highs and lows in the variables dictionary
def myalgorithm(stock, account, variables):
    # keep track of highs and lows
    if stock["price"] > variables["high"]:
        variables["high"] = stock["price"]

    if stock["price"] < variables["low"]:
        variables["low"] = stock["price"]

    # buy stock if not owned
    if (stock["ticker"] not in account.stocks_owned) and (account.funds - (stock["price"] + account.TRANSACTION_FEE) >= 0):
        account.buy_stock(stock["ticker"], 1)

# backtest algorithm
backtester.simulate(myalgorithm)

# print report of account
account.report()
```

# Contributing
PyAlgosim is completely opensource, licensed under the [MIT License](https://opensource.org/licenses/MIT). If you find any bugs, or have new ideas to extend the software, please do! Create a new issue or pull request and it will be reviewed.
