#!/usr/bin/env python
#DETRENDED PRICE OSCILLATOR
import pandas
from binance.client import Client
import numpy as np
import time
import telegram
import emoji
from pyti.simple_moving_average import simple_moving_average as sma
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
    markets = '<PATH>/BuyMarkets'
    connection = BinanceConnection(credentials)
    interval = '1h'
    limit = 500
    bot = telegram.Bot(token="<TOKEN>")
    chatid = "<CHATID>"
    fireemoji = '\U00002705'
    shitemoji = '\U0001F198'
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
                           open = [float(entry[1]) for entry in klines]
                           high = [float(entry[2]) for entry in klines]
                           low = [float(entry[3]) for entry in klines]
                           close = [float(entry[4]) for entry in klines]
                           volume = [float(entry[7]) for entry in klines]
                           volumeratio = volume[-1]/volume[-2]
                           ratioup=(close[-1]-close[-2])/close[-2]
                           ratiodown=(close[-2]-close[-1])/close[-2]
#                           ratioup=(high[-1]-low[-1])/low[-1]
#                           ratiodown=(high[-1] - low[-1])/high[-1]
                           buyavg = ((close[-1] + high[-1]) / 2 - (high[-1] * (1 - open[-1] / close[-1]) * (1 - ((low[-1] * open[-1]) / (high[-1]* close[-1])))))
                           sellavg = (low[-1] + close[-1]) / 1.99 + (low[-1] * (1 - low[-1] / open[-1]) * (1 - ((low[-1] * open[-1]) / (close[-1]* high[-1])))/1.1)
                           last_closing_price = close[-1]
                           close_array = np.asarray(close)
                           last4 = close_array[-5:]
                           donchianconversionline = (last4.max() + last4.min())/2
                           close_finished = close_array[:-1]
                           emax = pandas.DataFrame(close_array)
                           last_ema1 = emax.ewm(span=1).mean().iloc[-1,-1]
                           last_ema26 = emax.ewm(span=26).mean().iloc[-1,-1]
                           previous_ema1 = emax.ewm(span=1).mean().iloc[-2,-1]
                           previous_ema26 = emax.ewm(span=26).mean().iloc[-2,-1]
                           last_ema52 = emax.ewm(span=52).mean().iloc[-1,-1]
                           previous_ema52 =  emax.ewm(span=52).mean().iloc[-2,-1]
                           period_=21
                           ma=sma(close,period_)
                           ma14 = sma(close,14)
                         # barsback=int(period_/2)+1
                           dpo14=close-ma14
                           dpo=close-ma
                           dpo_orj=close-ma[-12]
                           def telegramsat(id):
                            bot.sendMessage(chat_id=id, text=(shitemoji*3) + "SAT "+ interval+ " Grafik(DPO)" + "\n" + symbol + "\n" + "Satış girilecek değer: "+str("{:.16f}".format(sellavg)) + thumbsdown + "\nHacim "+str("{:.1f}".format(volumeratio))+ " kat arttı!\nDPO-21: "+str(dpo[-1])+"\nDPO-orj: "+str(dpo_orj[-1]))
                           def telegramal(id):
                            bot.sendMessage(chat_id=id, text=(fireemoji*3)+ "AL " + interval+" Grafik(DPO)" + "\n" + symbol + "\n" + "Alım girilecek değer: "+str("{:.16f}".format(buyavg))+ thumbsup +"\nHacim "+str("{:.1f}".format(volumeratio))+ " kat arttı!\nDPO-21: "+str(dpo[-1])+"\nDPO-orj: "+str(dpo_orj[-1])+"\nStop Loss: "+str("{:.16f}".format(buyavg*0.93)))
                           print(symbol,dpo[-1],dpo_orj[-1])
                           if dpo[-1]>0 and dpo[-2]<0:
                            telegramal(chatid)
                           elif dpo[-1]<0 and dpo[-2]>0:
                            telegramsat(chatid)
                           count += 1
                        except: count+=1
                except Exception as exp:
                    print(exp.status_code, flush=True)
                    print(exp.message, flush=True)
            break

        except Exception as exp:
            print(exp.status_code, flush=True)
            print(exp.message, flush=True)
