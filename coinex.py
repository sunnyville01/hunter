import json
import time
import requests
from os import path
import urllib.request
from operator import itemgetter
from coins import Coins


# Cbrdige to Cryptopia
class Hunter:


    def __init__(self):

        # Coins
        coins = Coins()
        self.cbridge = coins.cbridge
        self.cryptopia = coins.cryptopia
        self.common = coins.common
        self.sleep_time = 2 # Interval between each coin check
        self.btc_per_order = 0.001
        self.buy_price_ratio = 0.85

        # Bitshares account/wellet info
        self.account_name = "###" # Add your name
        self.account = Account(self.account_name)
        self.balances = self.account.balances
        self.open_orders = self.account.openorders
        self.phrase = "###" # Add your phrase

        # Start loop
        self.loop_markets()


    def loop_markets(self):
        for coin in self.common:
            print(coin)
            try:
                cryptopiaData = self.cryptopia_data(coin)
                bidPrice = cryptopiaData[0]
                change = cryptopiaData[1]

                if change > 30 :
                    continue
                else:
                    # Check for available balance
                    significant_balance = self.significant_balance_exists(coin, bidPrice)
                    if significant_balance:
                        continue # Stop here and move to next coin
                        # Do pass or continue?

                    # Validate any existing orders
                    existing_order = self.get_order_id(coin)
                    if existing_order:
                        price = existing_order[1]
                        diff = bidPrice - price
                        diff_pct = (diff/bidPrice) * 100
                        if diff_pct > 10 and diff_pct < 20: # Skip if the desired order already exists
                            continue
                        else: # If order price is out of range replace it
                            order_id = existing_order[0]
                            self.cancel_order(coin, order_id) # Cancel old order
                            buyPrice = bidPrice * self.buy_price_ratio
                            print('Order Replaced')
                            self.place_buy_order(coin, buyPrice) # Place the right order
                    else:
                        buyPrice = bidPrice * self.buy_price_ratio
                        self.place_buy_order(coin, buyPrice) # Place the order

            except Exception as e:
                print(e)
                continue
            else:
                pass
            time.sleep(self.sleep_time)


        # Check for filled orders

    # Check Criterias for bids and asks at cbrdige
    def compare_orders(self, coin, price):
        market_id = 'BRIDGE.'+ coin +'/BRIDGE.BTC'
        market = Market(market_id)
        lowest_ask = market.orderbook()['asks'][0]["price"]
        highest_bid = market.orderbook()['bids'][0]["price"]

        # Note: price is the bidPrice, not buyPrice
        ask_diff = price - lowest_ask
        ask_diff_pct = (ask_0diff/price) * 100
        bid_diff = price - highest_bid
        bid_diff_pct = (bid_diff/price) * 100

        if ask_diff_pct > 10 or bid_diff_pct > 15:
            return False
        else:
            return True

    # Places a buy order
    def place_buy_order(self, coin, price):
        # Place order only if btc required is available
        btc_available_balance = self.available_balance('BTC')
        if btc_available_balance > self.btc_per_order:
            market_id = 'BRIDGE.'+ coin +':BRIDGE.BTC'
            market = Market(market_id)
            market.bitshares.wallet.unlock(self.phrase)
            order_market_id = "BRIDGE.BTC/BRIDGE."+ coin
            order_ammount = self.btc_per_order / price
            order_ammount_id = str(order_ammount) + ' BRIDGE.'+ coin
            market.buy(
                Price(price, order_market_id),
                Amount(order_ammount_id),
                account=self.account
            )

    # Get available balance of any coin
    def available_balance(self, coin):
        symbol = 'BRIDGE.'+ coin
        balance = self.account.balance(symbol).amount # float format
        return balance

    # Checks if an buy order has likely been filled in the past
    def significant_balance_exists(self, coin, price):
        result = False
        symbol = 'BRIDGE.'+ coin
        balance = self.account.balance(symbol).amount # float format
        threshold = 0.5 * (0.005/price)
        if balance > threshold:
            result = True
        return result

    # Cancel order
    def cancel_order(self, coin, order_id):
        market_id = 'BRIDGE.BTC/BRIDGE.'+ coin
        market = Market(market_id)
        market.bitshares.wallet.unlock(self.phrase)
        market.cancel(order_id, account=self.account)

    # Checks for existing orders and returns id and price
    def get_order_id(self, coin):
        order_id = False
        market_id = 'BRIDGE.BTC/BRIDGE.'+ coin
        market = Market(market_id)
        orders = market.accountopenorders(self.account)
        if orders:
            order_id = orders[0]["id"]
            order_price = orders[0]["price"]
            order = (order_id, order_price)
            return order
        return order_id

    ## Cryptopia
    def cryptopia_data(self, coin):
        market = coin + '_BTC'
        orders_url = 'https://www.cryptopia.co.nz/api/GetMarketOrders/'+ market
        market_url = 'https://www.cryptopia.co.nz/api/GetMarket/'+ market

        # Get bidPrice: Order book price when volume reaches 0.1btc
        buy_orders = requests.get(orders_url).json()['Data']['Buy']
        total = 0
        for order in buy_orders:
            total = total + order['Total']
            if total > 0.1:
                price = order['Price']
                price = float(price)
                break

        # Get 24hr change
        change = requests.get(market_url).json()['Data']['Change']
        change = float(change)

        # Return as tuple
        result = (price, change)
        return result



if __name__ == '__main__':

    while True:
        try:
            while True:
                i = Hunter()
                print('Restarting in 240 seconds...')
                time.sleep(120)
                print('Restarting in 120 seconds...')
                time.sleep(120)
        except Exception as e:
            print(e)
            print('Some error occured retrying in 120 seconds')

        time.sleep(120)
