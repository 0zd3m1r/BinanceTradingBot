#!/usr/bin/env python
import pandas
from binance.client import Client
import numpy as np
import time
import telegram
import emoji

class BinanceConnection:
    def __init__(self, file):
        self.connect(file)

    """ Creates Binance client """
    def connect(self, file):
        lines = [line.rstrip('\n') for line in open(file)]
        key = lines[0]
        secret = lines[1]
        self.client = Client(key, secret)

if __name__ == '__main__':
    credentials = '<PATH>/Credentials'
    markets = '<PATH>/Markets'
    connection = BinanceConnection(credentials)

    interval = '1d'
    limit = 500
    bot = telegram.Bot(token="<TOKEN>")
    chatid = "<CHATID>"
    chatidonder = "<CHATID>"
    fireemoji = emoji.emojize(':fire:')
    shitemoji = '\U0001F4A9'
    thumbsup = '\U0001F44D'
    thumbsdown = '\U0001F44E'
    while True:
        #time.sleep(20)

        try:

            with open(markets) as fp:
                lines = fp.read().splitlines()
                count = 0
                try:
                   for line in lines:
                        symbol = lines[count]

                        try:
                           klines = connection.client.get_klines(symbol=symbol, interval=interval, limit=limit)
                           print(symbol)
                           open = [float(entry[1]) for entry in klines]
                           high = [float(entry[2]) for entry in klines]
                           low = [float(entry[3]) for entry in klines]
                           close = [float(entry[4]) for entry in klines]
                           buyavg = ((close[-1] + high[-1]) / 2 - (high[-1] * (1 - open[-1] / close[-1]) * (1 - ((low[-1] * open[-1]) / (high[-1] * close[-1])))))
                           sellavg = (low[-1] + close[-1]) / 1.99 + (low[-1] * (1 - low[-1] / open[-1]) * (1 - ((low[-1] * open[-1]) / (close[-1] * high[-1]))) / 1.1)

                           last_closing_price = close[-1]
                           close_array = np.asarray(close)
                           close_finished = close_array[:-1]
                           emax = pandas.DataFrame(close_array)
                           last_ema1 = emax.ewm(span=1).mean().iloc[-1,-1]
                           last_ema26 = emax.ewm(span=26).mean().iloc[-1,-1]
                           previous_ema1 = emax.ewm(span=1).mean().iloc[-2,-1]
                           previous_ema26 = emax.ewm(span=26).mean().iloc[-2,-1]
                           if last_ema26 > last_ema1 and previous_ema1 > previous_ema26:
                            ratiodown=1-(close[-1]/last_ema26)
                            bot.sendMessage(chat_id=chatid, text=(shitemoji*5) + "SELL" +(shitemoji*5) + "\n" + symbol + "\n" + "Sell value point: "+str("{:.16f}".format(sellavg))+ "\nProfit lose on closing: "+str("{0:.4%}".format(ratiodown))+ thumbsdown)
                           elif last_ema26 < last_ema1 and previous_ema1 < previous_ema26:
                            ratioup=(close[-1]/last_ema26)-1
                            bot.sendMessage(chat_id=chatid, text=(fireemoji*5)+ "BUY" +(fireemoji*5) + "\n" + symbol + "\n" + "Buy value point: "+str("{:.16f}".format(sellavg))+ "\nProfit gain on closing: "+str("{0:.4%}".format(ratioup))+ thumbsup)
                           count += 1
                        except: count+=1
                except Exception as exp:
                    print(exp.status_code, flush=True)
                    print(exp.message, flush=True)
            break

        except Exception as exp:
            print(exp.status_code, flush=True)
            print(exp.message, flush=True)
