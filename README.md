# [PyAlgosim](http://dhdaniel.github.io/PyAlgosim)

A simple stock market back-tester for algorithmic trading built in Python. <http://dhdaniel.github.io/PyAlgosim>

## Getting started

The first thing you must do on downloading the software is, from the command line (you can use any way you want) navigate to the `utilities_and_modules` folder

```
  $ cd /path/to/PyAlgosim/
  $ cd utilities_and_modules
```

From that folder, run the Python program `scraper_init.py`.

```
  $ python scraper_init.py
```

Running this program is necessary to create the database `stocks.db`, which the program will communicate with. This database does _not_ come with the software because it is a large file, and for the sake of saving space it was not uploaded to GitHub.

## Trading algorithm

Once you have created the `stocks.db` file, you are ready to go. In the `pysimcode.py` file, in the main folder, is where all your algorithms and code will go. Open the file using your favourite text editor, and you will see some source code with _two functions:_ `main()` and `init()`.

### The init() function

The purpose of this function is to initialise any variables that you may want to use during your algorithm that are not already provided. You can store these variables in the dictionary returned by this function. For example, if you wanted to keep track of the lowest ever price of the stock, you could create an entry in the dictionary under the key `"lowest"`, and initialise it to `0` in the init() function. This function is called _once_ for every separate stock - this means these variables will be different for each ticker.

### The main() function

The `main()` function is what gets executed every day for each ticker. It contains the main algorithm and logic of your trading strategy. All the variables that are available for use are in the comments of the `pysimcode.py` file, and they are also described there. You can access the optional variables that you have created using the `optional_variables` variable, and looping through it (it is a dictionary).

## PyBank.Account()

One of the most important features of trading is actually having a **trading/bank account**. In PyAlgosim, this functionality is provided by the `PyBank.Account()` class. It has numerous functions that you can use to buy and sell stock, and it also takes into account transaction fees for you, so you don't have to worry about it. Also, it is completely customizable - you can choose how many funds to start with, the cost of transactions, etc.

### Using PyBank.Account()

Where you will write your code, `pysimcode.py`, the Account class is already imported, and is accessed in the `main()` method as `account`. If you wish to change the starting funds of the account (`$100,000` by default) you must open the `pysim.py` program, and look for the `PyBank.Account()` declaration. Change the number to whatever number you wish to use.

To alter the transaction fee value, you must go into the `PyBank.py` program, and alter the `self.TRANSACTION_FEE` value.

**Warning**: do not change anything else, or move these files out of place, as it may affect the program and produce errors at runtime.

## Accessing properties

### `account.funds`

The value of the account, excluding the value of the stocks - the amount of cash in your account.

### `account.transactions`

The number of transactions made by the account.

### `account.stocks_owned`

A dictionary with all the stocks owned at the time, with each key being the stock ticker, and the values being a list with two values - the **quantity** and the **price (at which it was bought)**.

### `account.TRANSACTION_FEE`

The current cost of transactions.

## Methods

### `account.buy_stock(ticker, quantity)`

Buys the specified stock, using the ticker and quantity and stores it in the account. If the stock does not exist, or the account does not have enough funds to purchase it, it will raise an error.

### `account.sell_stock(ticker, quantity)`

Sells the specified stock, and, if all the stock owned is sold, it removes the stock from the account. The function will raise an error if the stock is not owned by the account, or if you are trying to sell more than what you own, and quit. The parameter quantity can be either a numeric value, like 100, or the string "all", indicating the program to sell all of the stock owned.

### `account.trailing_stop(ticker, quantity, points, percentage=False)`

Begins a sell trailing stop order for the ticker provided and the quantity stated. The variable points indicates the tolerance of the order (how much you want to allow it to go down before selling), and percentage indicated whether points should be read as a percentage or as points. By default, it is set to False. If you attempt to sell more stock than what you own, an error will be raised and the program will quit.

**_Note_**: if you place two trailing stop orders for the _same_ stock (e.g placing a trailing stop for 100 shares of AAPL and then placing the same order again), the quantity will be accumulated (e.g now the order will be for 200 shares of AAPL) and the points variable will be **replaced by the last value provided**.

### `account.sell_all()`

Sells all the stocks in the account. This function is always called at the end of the backtesting program in order to return the profit/loss made at the end of backtesting.

## Outcome

Once you have included everything you want to in the `main()` and `init()` functions, you can run the `pysim.py` program (_not_ the `pysimcode.py` file), like so:

```
  $ python pysim.py
```

It will backtest every single stock in the S&P 500 from 1998 to 2013 using the algorithm you have provided, and will then print out the result of your trades.
