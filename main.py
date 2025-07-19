import os
from dotenv import load_dotenv, dotenv_values
from binance.client import Client
from datetime import datetime
import time
import sys
from datetime import datetime
import smtp 
FULL_PATH_TO_PROJECT = "your_path"
load_dotenv(dotenv_path=FULL_PATH_TO_PROJECT+"/.env")



BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET = os.getenv("BINANCE_SECRET")
PREFERED_CURRENCY_SYMBOL = "€"
FILE_OUTPUT_STRING = ""
FILE_ERROR_STRING = ""
now = int(time.time() * 1000)
one_year_ago = now - (365 * 24 * 60 * 60 * 1000)
date_and_time = datetime.now()


client = Client(api_key = BINANCE_API_KEY, api_secret = BINANCE_SECRET)

client_coins = client.get_all_coins_info()

# print("WALLET: \n")
# for coin in client_coins:
#     if coin["free"] != "0":
#         print(coin["coin"] + " : " , coin["free"] + "\n")



'''
    PROCESS USER DEPOSITS (FROM 1 YEAR AGO TO TODAY)
'''
client_payments = client.get_fiat_payments_history(transactionType = 0, beginTime=one_year_ago, endTime=now) #0 - buy 1 - sell

#[BTC] => 100.0 ...
payments_per_coin = dict()#this stores the sums of payments for each coin the user bought
profit_loss_per_coin = dict()#this stores the profit/loss for each currency the user bought

total_coin_bought = dict()
# print("DEPOSIT HISTORY: \n")
try:
    for payment in client_payments["data"]:
        if payment["status"] == "Completed":
            client_coin_symbols = [coin["coin"] for coin in client_coins if float(coin["free"]) > 0]
            if payment["cryptoCurrency"] not in client_coin_symbols:
                continue    #if coin is not in user's wallet skip it
            date = datetime.fromtimestamp(payment["createTime"] / 1000)
            # print(f"----- {date.strftime('%d-%m-%Y %H:%M:%S')} -----")
            # print(f"{payment['sourceAmount']} {payment['fiatCurrency']} ===> {payment['obtainAmount']} {payment['cryptoCurrency']} \n")

            if payment["cryptoCurrency"] in payments_per_coin:
                payments_per_coin[payment["cryptoCurrency"]] += float(payment["sourceAmount"])
            else:
                payments_per_coin[payment["cryptoCurrency"]] = float(payment["sourceAmount"])

            #get coin price now
            coin_price_now = client.get_klines(symbol=payment["cryptoCurrency"]+payment["fiatCurrency"], startTime=now-60*1000, endTime=now, interval=client.KLINE_INTERVAL_1MINUTE)
            open_time, open_price, high_price, low_price, close_price, *_ = coin_price_now[0]
            # print(f"Price now: {high_price} {payment['fiatCurrency']}")

            #calculate the profit/loss
            coin_worth_now = float(close_price) * float(payment["obtainAmount"])
            profit_loss = coin_worth_now - float(payment["sourceAmount"]) #if this is negative then it's loss
            profit_loss = round(profit_loss,2)
            if payment["cryptoCurrency"] in profit_loss_per_coin:
                profit_loss_per_coin[payment["cryptoCurrency"]] += profit_loss
            else:
                profit_loss_per_coin[payment["cryptoCurrency"]] = profit_loss

    

except Exception as e:
    FILE_ERROR_STRING += f"ERROR: could not fetch price for {payment['cryptoCurrency']+payment['fiatCurrency']}: {e}"



#print("PROFIT/LOSS PER COIN ")
output_coin_pl=""
for coin_name,profit_loss_on_coin in profit_loss_per_coin.items():
    output_coin_pl += f"{coin_name};{profit_loss_on_coin};"

FILE_OUTPUT_STRING = f"{date_and_time.strftime('%d.%m.%Y')};{output_coin_pl}"

with open(FULL_PATH_TO_PROJECT+"/crypto-report.txt","a") as f:
    f.write(FILE_OUTPUT_STRING + "\n")

#Call my email sending function 
smtp.send_email()




'''
    TODO: 
        -send parameters to send_email function and build an email with data
        -calculate the current price of BTC and calculate profit/loss since last deposit (DONE), 
        -monthly report sent to email in CSV format
        -bash script to run this weekly(DONE)
'''