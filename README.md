# [PyAlgosim](http://dhdaniel.github.io/PyAlgosim/)
#### The Python-built algorithmic backtester


# Getting started
To get started using the PyAlgosim algorithmic trading backtester, you must download the most recent version of the software. You can easily do this by either cloning the repository from GitHub [here](https://github.com/DHDaniel/PyAlgosim) or directly download the latest release from [here](https://github.com/DHDaniel/PyAlgosim/releases).

## Requirements
All that is required to start using PyAlgosim is:
- Python 2.7.X

## Project structure
On downloading, the project has a very specific structure that you should keep for everything to work as intended. Alternatively, you could set up your own structure, but it would require additional configuration (and would probably be a pain). After initialization, the project structure should look like this:

```bash
.
├── LICENSE
├── PyBank.py
├── PySimulator.py
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

For PyAlgosim to work, the project structure **should stay like this**. If you move the `stocks.db` file or the `tickers.json` file, you will need to reference them during the creation of a PySimulator object.

The program in which you wish to use the `Pysimulator` and `PyBank` modules in should ideally reside in the top-level directory of the project (that is, in the same directory as the PyBank and PySimulator files) for everything to run as smoothly as possible.

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

## PyAlgosim, the simulator
PyAlgosim is the module that takes care of running the algorithm that you wish to backtest. Using it is very simple and intuitive. First, you must import the module into your program - **note that your program should be created in the same directory as the PyAlgosim.py file for the program to properly communicate with the generated database and ticker file**.

```python
import PyAlgosim
```

### The PyAlgosim API
#### PyAlgosim.PyAlgosim(_account_, [_db_path_, _ticker_list_path_, _variables_])
This method initializes the PyAlgosim simulator. It returns an object that will function as the backtester for your algorithm.

**account** - a PyBank object. The trading account that you wish to use during the simulator.
**db_path** (optional) - the path to the database file you are using. Should be a `string`. If you used the initialize.py script and are running the program from PyAlgosim.py 's directory, then you shouldn't have to set this explicitly. Defaults to `./utils/stocks.db`.
**ticker_list_path** (optional) - the path to the ticker list file that should have been generated during the initialize.py script. Should be a `string`. Again, if you followed the initial setup instructions, you shouldn't have to explicitly set this. Defaults to `./utils/tickers.json`.
**variables** (optional) - an dictionary "template" (dictionary with empty fields) with any optional variables that you want your algorithm to have access to during the simulation. For example, the dictionary could store recurring averages, statistics, record highs and lows, etc. Defaults to `None`.

For example:
```python
import PySimulator
import PyBank

trade_account = PyBank.Account()

# this will use all of the default configuration, assuming all files have been kept in their original place
backtester = PySimulator.PySimulator(trade_account)

# this uses custom configuration for the stock database and the ticker list json file
backtester = PySimulator.PySimulator(trade_account, db_path="/some/other/path/mydata.db", ticker_list_path="/some/other/path/mytickers.json")

# this uses a variables dictionary, for potentially calculating a simple moving average for 50 days and the highest and lowest prices of the stock. Note that it is a "template" in the sense that it is empty - it will be provided exactly like that at the start of backtesting each stock.
my_variables = {
    highest_price = 0
    lowest_price = 0
    past_50_prices = []
}
backtester = PySimulator.PySimulator(trade_account, variables=my_variables)
```

#### _class_ PyAlgosim.simulate(_algorithm_[, _time_start_, _time_end_])
This method performs the backtesting on the algorithm provided, using the data specified in `time_start` and `time_end`.

**algorithm** - the name of the algorithm (function) that you wish to backtest. The function provided as an algorithm must take in the following variables in the order specified:
- A **stock data** dictionary that contains information about the stock being processed. The object will contain the following properties:
    -
