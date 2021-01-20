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
    markets = '<PATH>/MarketsTop200'
    connection = BinanceConnection(credentials)

    interval = '1h'
    limit = 500
    bot = telegram.Bot(token="<TOKEN>")
    chatid = "<CHATID>"
    fireemoji = emoji.emojize(':fire:')
    volumeemoji = '\U0001F310'
    shitemoji = '\U0001F4A9'
    thumbsup = '\U0001F44D'
    thumbsdown = '\U0001F44E'
    volumeupemoji = '\U0001F535'
    volumedownemoji = '\U0001F534'
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
                           open = [float(entry[1]) for entry in klines]
                           high = [float(entry[2]) for entry in klines]
                           low = [float(entry[3]) for entry in klines]
                           close = [float(entry[4]) for entry in klines]
                           volume = [float(entry[7]) for entry in klines]
                           buyavg = ((close[-1] + high[-1]) / 2 - (high[-1] * (1 - open[-1] / close[-1]) * (1 - ((low[-1] * open[-1]) / (high[-1] * close[-1])))))
                           sellavg = (low[-1] + close[-1]) / 1.99 + (low[-1] * (1 - low[-1] / open[-1]) * (1 - ((low[-1] * open[-1]) / (close[-1] * high[-1]))) / 1.1)
                           #if volume[-1]>volume[-2] and volume[-2]>volume[-3] and volume[-3]>volume[-4] and volume[-4]>volume[-5] and volume[-5]>volume[-6] and volume[-6]>volume[-7]  and volume[-7>volume[-8] and volume[-8]>volume[-9] and volume[-9]>volume[-10]:
                           # volumeinfo="Hacim artışta!"
                           #if volume[-1]>volume[-2] and volume[-2]>volume[-3] and volume[-3]>volume[-4] and volume[-4]>volume[-5] and volume[-5]>volume[-6] and volume[-6]>volume[-7] and volume[-7]>volume[-8] and volume[-8]>volume[-9] and volume[-9]>volume[-10]:
                           volumeratio = volume[-1]/volume[-2]
                           if volumeratio>3 and close[-1]>close[-2]:
                            volumeinfo='alım tarafında hacim çok güçlü artıyor!'
                            print(symbol,volumeinfo,volumeratio)
                            bot.sendMessage(chat_id=chatid, text=((volumeemoji)*1+" " + symbol+ "\nAlım tarafında hacim çok güçlü artıyor! "+volumeupemoji+"\n" + str("{:.1f}".format(volumeratio))+ " kat arttı!"))
                           elif volumeratio>3 and close[-1]<close[-2]:
                            volumeinfo='satış tarafında hacim çok güçlü artıyor!'
                            print(symbol,volumeinfo,volumeratio)
                            
                            bot.sendMessage(chat_id=chatid, text=((volumeemoji)*1+" " + symbol+ "\nSatış tarafında hacim çok güçlü artıyor! "+volumedownemoji+"\n" + str("{:.1f}".format(volumeratio))+ " kat arttı!"))
                           
                           else:print(symbol)
                           count += 1
                        except: count+=1
                except Exception as exp:
                    print(exp.status_code, flush=True)
                    print(exp.message, flush=True)
            break

        except Exception as exp:
            print(exp.status_code, flush=True)
            print(exp.message, flush=True)
