
# [PySimulator](http://dhdaniel.github.io/PySimulator)
A stock market back-tester for algorithmic trading built in Python.
[http://dhdaniel.github.io/PySimulator](http://dhdaniel.github.io/PySimulator)

## Getting started
The first thing you must do on downloading the software is, from the command line (you can use any way
  you want) navigate to the `utilities_and_modules` folder

  ```
  $ cd /path/to/PySimulator/
  $ cd utilities_and_modules
  ```

  From that folder, run the Python program `scraper_init.py`.

  ```
  $ python scraper_init.py
  ```

  Running this program is necessary to
  create the database `stocks.db`, which the program will communicate with. This database does *not* come
  with the software because it is a large file, and for the sake of saving space it was not
  uploaded to GitHub.

## Trading algorithm

  Once you have created the `stocks.db` file, you are ready to go. In the `pysimcode.py` file, in the main
  folder, is where all your algorithms and code will go. Open the file using any text editor that you like,
  and you will see some source code with *two functions:* `main()` and `init()`.

  ### The init() function
  The purpose of this function is to initialise any variables that you may want to use during your algorithm
  that are not already provided. You can store these variables in the dictionary returned by this function. For
  example, if you wanted to keep track of the lowest ever price of the stock, you could create an entry
  in the dictionary under the key `"lowest"`, and initialise it to `0` in the init() function. This function
  is called *once* for every separate stock - this means these variables will be different for each ticker.

  ### The main() function
  The `main()` function is what gets executed every day for each ticker. It contains the main algorithm and logic
  of your trading strategy. All the variables that are available for use are in the comments of the `pysimcode.py` file, and they are also described there. You can access the optional variables that you have created using the `optional_variables` variable, and looping through it (it is a dictionary).

## PyBank.Account()
One of the most important features of trading is actually having a **trading/bank account**. In PySimulator, this functionality is provided by the `pybank.Account()` class. It has numerous functions that you can use to buy and sell stock, and it also takes into account transaction fees for you, so you don't have to worry about it. Also, it is completely customizable - you can choose how many funds to start with, the cost of transactions, etc.

### Using pybank.Account()
Where you will write your code, `pysimcode.py`, the Account class is already imported, and is accessed in the `main()` method as `account`. If you wish to change the starting funds of the account (`$100,000` by default) you must open the `pysim.py` program, and look for the `Account()` declaration. Change the number to whatever number you wish to use.

To alter the transaction fee value, you must go into the `pybank.py` program, and alter the `self.TRANSACTION_FEE` value.

**Warning**: do not change anything else, or move these files out of place, as it may affect the program and produce errors at runtime.

## Methods

#### `account.getValue()`
Returns the value of the account, excluding the value of the stocks - the amount of cash in your account.

#### `account.getTransactions()`
Returns the number of transactions made by the account.

#### `account.getStocks()`

Returns a dictionary with all the stocks owned at the time, with each key being the stock ticker, and the values being a list with two values - the **quantity** and the **price (at which it was bought)**.

#### `account.getTransactionFee()`
Returns the current cost of transactions.

#### `account.buyStock(ticker, quantity, price)`
Buys the specified stock, using the ticker, quantity, and the price, and stores it in the account. If the stock does not exists, or the account does not have enough funds to purchase it, it will return `-1`.

_**Note**: the account does not check whether the price provided is the correct one - you must provide it yourself, using the variables offered in the `pysimcode.py` file._

#### `account.sellStock(ticker, quantity, price)`
Sells the specified stock, and, if all the stock owned is sold, it removes the stock from the account. The function will return `-1` if the stock is not owned by the account, or if you are trying to sell more than what you own.

_**Note**: the account does not check whether the price provided is the correct one - you must provide it yourself, using the variables offered in the `pysimcode.py` file._

#### `account.sellAll(latest_prices)`
Sells all the stocks in the account. This function is always called at the end of the backtesting program in order to return the profit/loss made at the end of backtesting. `latest_prices` is a variable provided in the `pysim.py` program with all the last stock prices for each ticker.


## Outcome
  Once you have included everything you want to in the `main()` and `init()` functions, you can run the `pysim.py` program (*not* the `pysimcode.py` file), like so:

  ```
  $ python pysim.py
  ```

  It will backtest every single stock in the S&P 500 from 1998 to 2013 using the algorithm you have provided,
  and will then print out the result of your trades.
