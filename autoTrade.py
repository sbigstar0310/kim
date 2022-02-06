
from locale import currency
import time
import pyupbit
import datetime
import bestk

access = "5cI0QdQvmKxYfvyJAIYnwQVaiwnfQfdy4GiOffyo"
secret = "Sz6meGwNRQUr3Irpk0DQ88lKv8igRfO9f7riLDGN"

# Number of Coin
numOfCoins = 3

def get_target_price(ticker, k):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    time.sleep(0.5)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    # 09:00 return
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    time.sleep(0.1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    # get my balance of ticker
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def print_myBalance():
    print("My Balance")
    balances = upbit.get_balances()
    for balance in balances:
        print("  %5s : %s" %(balance['currency'], balance['balance']))

# Log in
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# find best k before starting the loop
print("initialize k")
k1 = bestk.get_bestk("KRW-BTC")
k2 = bestk.get_bestk("KRW-SAND")
k3 = bestk.get_bestk("KRW-MANA")
print("k1:%.2f, k2:%.2f, k3:%.2f" %(k1, k2, k3))

# Start auto trading
while True:
    try:
        now = datetime.datetime.now()                                         # current time
        now_minute = int(now.strftime("%M"))                                  # minute of current time
        start_time = get_start_time("KRW-BTC")                                # start_time == 09:00
        end_time = start_time + datetime.timedelta(days=1)                    # end_time == next day 09:00
        
        if start_time < now < end_time - datetime.timedelta(seconds=59):                               # 09:00 < current time < 08:59:01
            BTC_target_price  = get_target_price("KRW-BTC",  k1)              # Set target price 
            SAND_target_price = get_target_price("KRW-SAND", k2)              # Find best k in bestk.py - get_bestk()
            MANA_target_price = get_target_price("KRW-MANA", k3)

            BTC_current_price  = pyupbit.get_current_price("KRW-BTC")          # Current BTC price
            SAND_current_price = pyupbit.get_current_price("KRW-SAND")
            MANA_current_price = pyupbit.get_current_price("KRW-MANA")


            krw = get_balance("KRW")                                           # current krw balance
            coinBalanceLimit = krw / numOfCoins                                # coin can be purchased until 1/3 * krw 

            if BTC_target_price < BTC_current_price:                           # Current BTC price > Target price -> Purchase           
                if krw // numOfCoins > 5000 and BTC_current_price * get_balance("BTC") < coinBalanceLimit:                                               
                    print("BTC  | target price is: %d, current price is: %d" %(BTC_target_price, BTC_current_price))
                    upbit.buy_market_order("KRW-BTC", krw // numOfCoins)
                    print("%s || Purchase %d BTC coin." %(now, krw // numOfCoins))
                    print_myBalance()
                    

            if SAND_target_price < SAND_current_price:                         # Current SAND price > Target price -> Purchase
                if krw // numOfCoins > 5000 and SAND_current_price * get_balance("SAND") < coinBalanceLimit:                                               
                    print("SAND | target price is: %d, current price is: %d" %(SAND_target_price, SAND_current_price))
                    upbit.buy_market_order("KRW-SAND", krw // numOfCoins)           
                    print("%s || Purchase %d SAND coin." %(now, krw // numOfCoins))
                    print_myBalance()
                    

            if MANA_target_price < MANA_current_price:                         # Current MANA price > Target price -> Purchase
                if krw // numOfCoins > 5000 and MANA_current_price * get_balance("MANA") < coinBalanceLimit:    
                    print("MANA | target price is: %d, current price is: %d" %(MANA_target_price, MANA_current_price))                                         
                    upbit.buy_market_order("KRW-MANA", krw // numOfCoins)           
                    print("%s || Purchase %d MANA coin." %(now, krw // numOfCoins))
                    print_myBalance()
        
        else:                                                                  # 08:59:01 ~ 09:00:00
            btc = get_balance("BTC")                                       # Check balance of BTC, SAND, MANA
            snd = get_balance("SAND")   
            mna = get_balance("MANA")   
            
            # reset k
            print("reset k")
            k1 = bestk.get_bestk("KRW-BTC")
            k2 = bestk.get_bestk("KRW-SAND")
            k3 = bestk.get_bestk("KRW-MANA")
            print("k1:%.2f, k2:%.2f, k3:%.2f" %(k1, k2, k3))

            BTC_current_price  = pyupbit.get_current_price("KRW-BTC")          # Current BTC price
            SAND_current_price = pyupbit.get_current_price("KRW-SAND")
            MANA_current_price = pyupbit.get_current_price("KRW-MANA")

            if btc * BTC_current_price > 5000:                                 # BTC > 5000
                upbit.sell_market_order("KRW-BTC", btc)                        # Sell all of them  
                print("%s || Sell %f BTC coin with %f value" %(now, btc, BTC_current_price))
                print_myBalance()

            if snd * SAND_current_price > 5000:                                # SAND > 5000 
                upbit.sell_market_order("KRW-SAND", snd)                       # Sell all of them  
                print("%s || Sell %f SAND coin with %f value" %(now, snd, SAND_current_price))
                print_myBalance()

            if mna * MANA_current_price > 5000:                                # MANA > 5000
                upbit.sell_market_order("KRW-MANA", mna)                       # Sell all of them  
                print("%s || Sell %f MANA coin with %f value" %(now, mna, BTC_current_price))
                print_myBalance()     

        time.sleep(1)

    except Exception as e:
        print(e)
        time.sleep(1)