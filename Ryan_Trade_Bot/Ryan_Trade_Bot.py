import os 
from dotenv import load_dotenv, dotenv_values
import ccxt 
import pandas as pd

load_dotenv()



exchange = ccxt.binance({
    'apiKey': os.getenv("apikey"),
    'secret': os.getenv('secret')
})

markets = exchange.load_markets()
ticker = exchange.fetch_ticker('BTC/GBP')
btc_to_gbp_rate = ticker['last']  # The last traded price for BTC/GBP

# Calculate how much BTC £10,000 can buy


symbol = 'BTC/USDT'    
limit = 1          

ohlcv5m = exchange.fetch_ohlcv(symbol, '5m', limit=limit)
ohlcv1s = exchange.fetch_ohlcv(symbol,'1s',limit=limit)


df = pd.DataFrame(ohlcv5m, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df2 = pd.DataFrame(ohlcv1s, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
df2['timestamp'] = pd.to_datetime(df2['timestamp'], unit='ms')

df['ema_9'] = df['close'].ewm(span=9, adjust=False).mean()



if(df2['close'].iloc[-1] > df['ema_9'].iloc[-1]):
    print('Buy Order')
    create_order('buy', 100/ btc_to_gbp_rate )
elif(df2['close'].iloc[-1] < df['ema_9'].iloc[-1]):
    print('Sell Order')


balances = exchange.fetch_balance()
print(balances['BTC'])

def create_order(side,amount):
    try:
        order = exchange.create_order(symbol, 'MARKET', side, amount,params = {'test': True,})
        print(order)

    except Exception as e:
        print(type(e).__name__, str(e))
