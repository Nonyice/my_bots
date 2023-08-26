import ccxt
import talib
import time
import keyring

# Retrieve API keys from keyring
api_key = keyring.get_password('binance', 'binance_api_key')
api_secret = keyring.get_password('binance', 'binance_api_secret')

# Initialize Binance exchange instance
exchange = ccxt.binance({
    'rateLimit': 1500,  # adjust as needed
    'enableRateLimit': True,
    'apiKey': api_key,
    'secret': api_secret
})

# Set trading pair and timeframe
symbol = 'BTC/USDT'
timeframe = '1h'

# Define stop-loss and take-profit percentages
stop_loss_percent = 2.0  # 2%
take_profit_percent = 1.0  # 1%

def calculate_macd(data):
    close_prices = data['close']
    macd, signal, _ = talib.MACD(close_prices, fastperiod=12, slowperiod=26, signalperiod=9)
    return macd, signal

def main():
    while True:
        try:
            # Fetch historical data
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
            closes = [ohlcv[i][4] for i in range(len(ohlcv))]
            
            # Calculate MACD
            macd, signal = calculate_macd({'close': closes})
            
            # Determine buy/sell conditions
            if macd[-1] > signal[-1] and macd[-2] <= signal[-2]:
                # Buy signal
                balance = exchange.fetch_balance()
                base_balance = balance['total'][symbol.split('/')[0]]
                if base_balance > 0:
                    amount_to_buy = base_balance * 0.98  # Use 98% of available balance
                    order = exchange.create_market_buy_order(symbol, amount_to_buy)
                    print(f'Buy Order: {order}')
                    
                    # Calculate stop-loss and take-profit prices
                    current_price = exchange.fetch_ticker(symbol)['last']
                    stop_loss_price = current_price * (1 - stop_loss_percent / 100)
                    take_profit_price = current_price * (1 + take_profit_percent / 100)
                    
                    # Place stop-loss and take-profit orders
                    stop_loss_order = exchange.create_limit_sell_order(symbol, amount_to_buy, stop_loss_price)
                    take_profit_order = exchange.create_limit_sell_order(symbol, amount_to_buy, take_profit_price)
                    print(f'Stop-Loss Order: {stop_loss_order}')
                    print(f'Take-Profit Order: {take_profit_order}')
            
            elif macd[-1] < signal[-1] and macd[-2] >= signal[-2]:
                # Sell signal
                balance = exchange.fetch_balance()
                quote_balance = balance['total'][symbol.split('/')[1]]
                if quote_balance > 0:
                    amount_to_sell = quote_balance * 0.98  # Use 98% of available balance
                    order = exchange.create_market_sell_order(symbol, amount_to_sell)
                    print(f'Sell Order: {order}')
            
            time.sleep(900)  # Sleep for 15 minutes before next iteration
            
        except Exception as e:
            print(f'An error occurred: {e}')
            time.sleep(900)  # Sleep for 15 minutes before retrying

if __name__ == '__main__':
    main()
