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
                           open = [float(entry[1]) for entry in klines]
                           high = [float(entry[2]) for entry in klines]
                           low = [float(entry[3]) for entry in klines]
                           close = [float(entry[4]) for entry in klines]
                           volume = [float(entry[7]) for entry in klines]
                           buyavg = ((close[-1] + high[-1]) / 2 - (high[-1] * (1 - open[-1] / close[-1]) * (1 - ((low[-1] * open[-1]) / (high[-1] * close[-1])))))
                           sellavg = (low[-1] + close[-1]) / 1.99 + (low[-1] * (1 - low[-1] / open[-1]) * (1 - ((low[-1] * open[-1]) / (close[-1] * high[-1]))) / 1.1)
                           volumeratio = volume[-1]/volume[-2]
                           print(symbol)
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
                           def telegramsat(id):
                            bot.sendMessage(chat_id=id, text=(shitemoji*1) + "SAT (TOP 200) 1 Saatlik Grafik" + "\n" + symbol + "\n" + "Satış girilecek değer: "+str("{:.16f}".format(sellavg    ))+ "\n1 saatlik dilimdeki düşüş oranı: "+str("{0:.4%}".format(ratiodown))+ thumbsdown +"\nEMA'ya Uzaklık: "+str("{0:.4%}".format(ratioEMAdown))+emojiema + "\nHacim "+str("{:.1f}".format(volumeratio))+ " kat arttı!")
                           def telegramal(id):
                            bot.sendMessage(chat_id=id, text=(fireemoji*1)+ "AL (TOP 200) 1 Saatlik Grafik" + "\n" + symbol + "\n" + "Alım girilecek değer: "+str("{:.16f}".format(buyavg))+     "\n1 saatlik dilimdeki yükseliş oranı: "+str("{0:.4%}".format(ratioup))+ thumbsup +"\nEMA'ya Uzaklık: "+str("{0:.4%}".format(ratioEMAup))+emojiema+ "\nHacim "+str("{:.1f}".format(volumeratio))+ " kat arttı!")
                           if (last_ema52 > last_ema26 or last_ema52 == last_ema26) and previous_ema26 > previous_ema52:
                            ratiodown=(high[-1] - low[-1])/high[-1]
                            ratioEMAdown=(last_ema26-close[-1])/close[-1]
                            if ratioEMAdown >0 and ratioEMAdown<0.01: emojiema='\U0001F6A9'
                            elif ratioEMAdown>=0.01 and ratioEMAdown<0.03: emojiema=('\U0001F6A9')*2
                            elif ratioEMAdown>=0.03 and ratioEMAdown<0.05: emojiema=('\U0001F6A9')*3
                            elif ratioEMAdown>=0.05 and ratioEMAdown<0.07: emojiema=('\U0001F6A9')*4
                            elif ratioEMAdown>=0.07: emojiema=('\U0001F6A9')*5
                            telegramsat(chatid)
                           elif (last_ema26 > last_ema52 or last_ema26 == last_ema52) and previous_ema26 < previous_ema52:
                            ratioEMAup=(close[-1]-last_ema26)/last_ema26
                            ratioup=(high[-1]-low[-1])/low[-1]
                            if ratioEMAup >0 and ratioEMAup<0.01: emojiema='\U0001F4B0'
                            elif ratioEMAup>=0.01 and ratioEMAup<0.03: emojiema=('\U0001F4B0')*2
                            elif ratioEMAup>=0.03 and ratioEMAup<0.05: emojiema=('\U0001F4B0')*3
                            elif ratioEMAup>=0.05 and ratioEMAup<0.07: emojiema=('\U0001F4B0')*4
                            elif ratioEMAup>=0.07: emojiema=('\U0001F4B0')*5
                            telegramal(chatid)
                           count += 1
                        except: count+=1
                except Exception as exp:
                    print(exp.status_code, flush=True)
                    print(exp.message, flush=True)
            break

        except Exception as exp:
            print(exp.status_code, flush=True)
            print(exp.message, flush=True)
