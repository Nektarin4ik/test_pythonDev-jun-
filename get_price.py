import datetime
import time
import pandas as pd

from binance import Client, AsyncClient, ThreadedWebsocketManager, ThreadedDepthCacheManager

api_key = 'vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgwCIPy6utIco14y7Ju91duEh8A'
secret_key = 'NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7H5fATj0j'
symbol_btc = 'BTCUSDT' # имя фьючерсной пары
symbol_eth = 'ETHUSDT' # имя фьючерсной пары
client = Client(api_key, secret_key)
last_time = time.time()
interval = Client.KLINE_INTERVAL_4HOUR

klines_eth = client.futures_klines(symbol=symbol_eth, interval=interval)
klines_btc = client.futures_klines(symbol=symbol_btc, interval=interval)
open_price_eth = float(klines_eth[-1][1]) #Цена открытия последней свечи на 4-х часовом таймфрейме
open_price_btc = float(klines_btc[-1][1]) #Цена открытия последней свечи на 4-х часовом таймфрейме
close_price_eth = float(klines_eth[-1][4]) #Цена закрытия последней свечи на 4-х часовом таймфрейме
close_price_btc = float(klines_btc[-1][4]) #Цена закрытия последней свечи на 4-х часовом таймфрейме
change_price_eth = ((open_price_eth - close_price_eth) / open_price_eth) * 100  #Изменение цены в %
change_price_btc = ((open_price_btc - close_price_btc) / open_price_btc) * 100  # Изменение цены в %

# Рассчитываем коэффициент относительной силы/слабости эфира к биткоину
rs = change_price_eth / change_price_btc

# Получаем цену ETHUSDT:
price_eth = client.futures_order_book(symbol=symbol_eth)['asks'][0][0]

# Второй вариант получения цены:
price_eth2 = client.futures_symbol_ticker(symbol=symbol_eth)['price']

# Алгоритм непосредственно для эфира с учетом коэффициента относительной силы/слабости:

last_price = price_eth2
while True:
    current_price = client.futures_symbol_ticker(symbol=symbol_eth)['price']
    current_time = time.time()
    # Проверяем изменение цены за последний час
    if current_time - last_time > 3600:  # 60 минут = 3600 секунд
        price_change = rs * ((float(current_price) - float(last_price)) / float(last_price) * 100)
        if abs(price_change) >= 1:
            print(f'Цена изменилась на {price_change: }% за последний час')
        last_price = current_price
        last_time = current_time

    time.sleep(1)  # Задержка обновления цены в 1 секунду


