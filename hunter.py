import json
import time
import sqlite3
import requests
from os import path
import urllib.request
from operator import itemgetter
from coins import Coins
from bittrex import bittrex

class Hunter:

    def __init__(self):

        # All Coins
        self.coins = Coins()
        self.coinex_coins = {
        "bittrex": self.coins.coinex_to_bittrex,
        "binance": self.coins.coinex_to_binance,
        "hitbtc": self.coins.coinex_to_hitbtc,
        "cbridge": self.coins.coinex_to_cbridge,
        }
        self.cbridge_coins = {
        "bittrex": self.coins.cbridge_to_bittrex,
        }
        # Settings
        self.target_percentages = {"bittrex": 12, "binance": 12, "hitbtc": 30, "cbridge": 40}
        self.percentage_ranges = {"bittrex": 5, "binance": 5, "hitbtc": 10, "cbridge": 15}

        # Prices
        self.bittrex_prices = {}
        self.binance_prices = {}
        self.hitbtc_prices = {}
        self.cbridge_prices = {}

        # Connect to Database
        self.conn = sqlite3.connect('hunter.db')
        self.c = self.conn.cursor()


    # Create Table (Done)
    def create_table(self):
        self.c.execute('CREATE TABLE IF NOT EXISTS coinexOrders(toExchange TEXT, coin TEXT, exchangePrice REAL, buyOrderIdeal REAL, buyOrderCurrent REAL, targetPercentage INTEGER, currentDifference REAL, inRange INTEGER, Ignore INTEGER DEFAULT 0)')
        # self.c.execute('CREATE TABLE IF NOT EXISTS cbridgePrices(coin TEXT, lastPrice REAL, buyPrice REAL, sellPrice REAL)')

    # Update Bittrex Prices
    def bittrex_update_prices(self):
        try:
            url = 'https://api.bittrex.com/api/v1.1/public/getmarketsummaries'
            json_data = requests.get(url).json()["result"]
        except Exception as e:
            print(e)
        else:
            self.c.execute("DELETE FROM bittrexPrices") # Remove previous prices from table
            self.conn.commit()
            for item in json_data: # Add new prices to table
                if item["MarketName"].startswith('BTC'):
                    coin = item["MarketName"][4:]
                    last = item["Last"]
                    bid = item["Bid"]
                    ask = item["Ask"]
                    self.c.execute("INSERT INTO bittrexPrices (coin, lastPrice, buyPrice, sellPrice) VALUES (?, ?, ?, ?)",
                        (coin, last, bid, ask))
                    self.conn.commit()

    def binance_update_prices(self):
        try:
            url = 'https://api.binance.com/api/v1/ticker/24hr'
            json_data = requests.get(url).json()
        except Exception as e:
            print(e)
        else:
            self.c.execute("DELETE FROM binancePrices") # Remove previous prices from table
            self.conn.commit()
            for item in json_data: # Add new prices to table
                if item["symbol"].endswith('BTC'):
                    coin = item["symbol"][:-3]
                    last = item["lastPrice"]
                    bid = item["bidPrice"]
                    ask = item["askPrice"]
                    self.c.execute("INSERT INTO binancePrices (coin, lastPrice, buyPrice, sellPrice) VALUES (?, ?, ?, ?)",
                        (coin, last, bid, ask))
                    self.conn.commit()

    def hitbtc_update_prices(self):
        try:
            url = 'https://api.hitbtc.com/api/2/public/ticker'
            json_data = requests.get(url).json()
        except Exception as e:
            print(e)
        else:
            self.c.execute("DELETE FROM hitbtcPrices") # Remove previous prices from table
            self.conn.commit()
            for item in json_data: # Add new prices to table
                if item["symbol"].endswith('BTC'):
                    coin = item["symbol"][:-3]
                    last = item["last"]
                    bid = item["bid"]
                    ask = item["ask"]
                    self.c.execute("INSERT INTO hitbtcPrices (coin, lastPrice, buyPrice, sellPrice) VALUES (?, ?, ?, ?)",
                        (coin, last, bid, ask))
                    self.conn.commit()

    def cbridge_update_prices(self):
        try:
            url = 'https://api.crypto-bridge.org/api/v1/ticker'
            json_data = requests.get(url).json()
        except Exception as e:
            print(e)
        else:
            self.c.execute("DELETE FROM cbridgePrices") # Remove previous prices from table
            self.conn.commit()
            for item in json_data: # Add new prices to table
                if item["id"].endswith('_BTC'):
                    coin = item["id"][:-4]
                    last = item["last"]
                    bid = item["bid"]
                    ask = item["ask"]
                    self.c.execute("INSERT INTO cbridgePrices (coin, lastPrice, buyPrice, sellPrice) VALUES (?, ?, ?, ?)",
                        (coin, last, bid, ask))
                    self.conn.commit()

    def update_all_exchanges(self):
        self.bittrex_update_prices()
        self.binance_update_prices()
        self.hitbtc_update_prices()
        self.cbridge_update_prices()

    # Updaate Coinex Main Table
    def update_coinex_table(self):
        pricesTables = {
        "bittrex": "bittrexPrices",
        "binance": "binancePrices",
        "hitbtc": "hitbtcPrices",
        "cbridge": "cbridgePrices",
        }

        self.c.execute("DELETE FROM coinexOrders") # Remove previous prices from table
        self.conn.commit()

        for exchange in self.coinex_coins:
            coins = self.coinex_coins[exchange]
            table = pricesTables[exchange]
            query_init = "SELECT lastPrice FROM {}".format(table)

            for coin in coins:
                self.c.execute(query_init +" WHERE coin=?", ( coin,))
                last_price = self.c.fetchone()[0]
                target_percentage = self.target_percentages[exchange]
                percentage_range = self.percentage_ranges[exchange]
                buy_order_ideal = (100 - target_percentage) * last_price / 100
                self.c.execute("INSERT INTO coinexOrders (toExchange, coin, exchangePrice, buyOrderIdeal, buyOrderCurrent, targetPercentage, currentDifference, inRange, Ignore) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (exchange, coin, last_price, buy_order_ideal, buy_order_ideal, target_percentage, target_percentage, 1, 0))

        self.conn.commit()

    # Get exchange data from database and store in memory
    def retrieve_exchanges_data(self):

        # Bittrex
        self.c.execute("SELECT coin, lastPrice FROM bittrexPrices")
        for item in self.c.fetchall():
            self.bittrex_prices[item[0]] = item[1]
        # Binance
        self.c.execute("SELECT coin, lastPrice FROM binancePrices")
        for item in self.c.fetchall():
            self.binance_prices[item[0]] = item[1]
        # Hitbtc
        self.c.execute("SELECT coin, lastPrice FROM hitbtcPrices")
        for item in self.c.fetchall():
            self.hitbtc_prices[item[0]] = item[1]
        # Cbridge
        self.c.execute("SELECT coin, buyPrice FROM cbridgePrices")
        for item in self.c.fetchall():
            self.cbridge_prices[item[0]] = item[1]

    # Check Coinex Orders
    def check_coinex_prices(self):
        # Get prices from prices tables for each exchange
        self.retrieve_exchanges_data()

        # Update coin prices
        self.update_all_exchanges()

        # Fetch and store old data
        self.c.execute("SELECT * FROM coinexOrders")
        rows = self.c.fetchall()

        # Delete old data
        self.c.execute("DELETE FROM coinexOrders") # Remove previous prices from table
        self.conn.commit()

        # Add new data
        for row in rows:
            exchange = row[0] # toExchange
            coin = row[1] # coin

            if exchange == "bittrex":
                exchange_price_new = self.bittrex_prices[coin] # exchangePrice
            if exchange == "binance":
                exchange_price_new = self.binance_prices[coin] # exchangePrice
            if exchange == "hitbtc":
                exchange_price_new = self.hitbtc_prices[coin] # exchangePrice
            if exchange == "cbridge":
                exchange_price_new = self.cbridge_prices[coin] # exchangePrice

            buy_order_current = row[4] # buyOrderCurrent
            target_percentage = self.target_percentages[exchange] # targetPercentage
            percentage_range = self.percentage_ranges[exchange]
            buy_order_ideal = (100 - target_percentage) * exchange_price_new / 100 # buyOrderIdeal

            if exchange_price_new == 0:
                current_difference = 1000
            else:
                current_difference = ((exchange_price_new - buy_order_current) * 100) / exchange_price_new # currentDifference
                ignore = row[8]

            upper_limit = (100 - (target_percentage - percentage_range)) * exchange_price_new / 100
            lower_limit = (100 - (target_percentage + percentage_range)) * exchange_price_new / 100

            in_range = 1 if lower_limit <= buy_order_current <= upper_limit else 0 # inRange

            self.c.execute("INSERT INTO coinexOrders (toExchange, coin, exchangePrice, buyOrderIdeal, buyOrderCurrent, targetPercentage, currentDifference, inRange, Ignore) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (exchange, coin, exchange_price_new, buy_order_ideal, buy_order_current, target_percentage, current_difference, in_range, ignore))
            self.conn.commit()



if __name__ == '__main__':
    # i.create_table()
    # i.update_coinex_table()
    while True:
        i = Hunter()
        i.check_coinex_prices()
        i.c.close()
        i.conn.close()

        print("Restarting in 10 minutes")
        time.sleep(300)
        print("Restarting in 5 minutes")
        time.sleep(300)
