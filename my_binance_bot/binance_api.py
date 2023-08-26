import requests
import keyring

class BinanceAPI:
    def __init__(self, api_key, api_secret):
        self.base_url = 'https://api.binance.com/api/v3'
        self.headers = {'X-MBX-APIKEY': api_key}
        self.api_secret = api_secret

    def get_ticker(self, trading_pair):
        endpoint = '/ticker/price'
        params = {'symbol': trading_pair}
        response = requests.get(self.base_url + endpoint, params=params)
        data = response.json()
        return float(data['price']) if 'price' in data else None

    def place_market_buy_order(self, trading_pair, quantity):
        endpoint = '/order'
        params = {
            'symbol': trading_pair,
            'side': 'BUY',
            'type': 'MARKET',
            'quantity': quantity
        }
        response = requests.post(self.base_url + endpoint, params=params, headers=self.headers)
        return response.json()

    def place_market_sell_order(self, trading_pair, quantity):
        endpoint = '/order'
        params = {
            'symbol': trading_pair,
            'side': 'SELL',
            'type': 'MARKET',
            'quantity': quantity
        }
        response = requests.post(self.base_url + endpoint, params=params, headers=self.headers)
        return response.json()

    # Add more methods for fetching historical data, managing trades, etc.

    

    def place_stop_loss_order(self, trading_pair, quantity, stop_price):
        endpoint = '/order'
        params = {
            'symbol': trading_pair,
            'side': 'SELL',
            'type': 'STOP_LOSS',
            'quantity': quantity,
            'stopPrice': stop_price
        }
        response = requests.post(self.base_url + endpoint, params=params, headers=self.headers)
        return response.json()

    def place_take_profit_order(self, trading_pair, quantity, take_profit_price):
        endpoint = '/order'
        params = {
            'symbol': trading_pair,
            'side': 'SELL',
            'type': 'TAKE_PROFIT',
            'quantity': quantity,
            'stopPrice': take_profit_price
        }
        response = requests.post(self.base_url + endpoint, params=params, headers=self.headers)
        return response.json()


if __name__ == '__main__':
    # Retrieve API keys from keyring
    api_key = keyring.get_password('binance', 'binance_api_key')
    api_secret = keyring.get_password('binance', 'binance_api_secret')
    
    trading_pair = 'BTCUSDT'
    quantity_to_buy = 0.01
    quantity_to_sell = 0.01  # Adjust as needed

    binance_api = BinanceAPI(api_key, api_secret)
    ticker_price = binance_api.get_ticker(trading_pair)

    if ticker_price is not None:
        print(f'Ticker Price for {trading_pair}: {ticker_price}')
        

        # Example: Place a market buy order
        buy_order = binance_api.place_market_buy_order(trading_pair, quantity_to_buy)
        print(f'Buy Order Response: {buy_order}')
    
        # Place stop-loss order
        stop_loss_order = binance_api.place_stop_loss_order(trading_pair, quantity_to_buy, stop_loss_price)
        print(f'Stop-Loss Order Response: {stop_loss_order}')
    
        # Place take-profit order
        take_profit_order = binance_api.place_take_profit_order(trading_pair, quantity_to_buy, take_profit_price)
        print(f'Take-Profit Order Response: {take_profit_order}')

        # Example: Place a market sell order
        sell_order = binance_api.place_market_sell_order(trading_pair, quantity_to_sell)
        print(f'Sell Order Response: {sell_order}')
    

    else:
        print(f'Failed to fetch ticker price for {trading_pair}')




        
