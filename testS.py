
import time
import pyupbit
import datetime
import bestk

access = "emsE1HCqqG2xLmGcUNEsatFvhU9F1R9lvnBcXynT"
secret = "eUZJrsriOzaIvRLqH6cyxmcfCelNqyaP7BArcLbP"

numOfCoins = 3

# initial seed money
KRWB = 210000
BTCB = 0
SANDB = 0
MANAB = 0

# Coin bought FLAG
BTCBUY  = False
SANDBUY = False
MANABUY = False

def get_target_price(ticker, k = 0.2):
    df = pyupbit.get_ohlcv(ticker, interval="minute30", count=2)
    time.sleep(0.5)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_balance(ticker):
    if ticker == "KRW":
        return KRWB
    elif ticker == "KRW-BTC":
        return BTCB
    elif ticker == "KRW-SAND":
        return SANDB
    elif ticker == "KRW-MANA":
        return MANAB
    return 0

def print_myBalance():
    print("My Balance")
    print("  KRW: " + str(KRWB))
    print("  BTC: " + str(BTCB))
    print("  SAND: " + str(SANDB))
    print("  MANA: " + str(MANAB))

# Log in
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# find best k before starting the loop
print("initialize k")
k1 = bestk.get_bestk("KRW-BTC")
print("k1:%.2f" %(k1))

krw = get_balance("KRW")      # current krw balance
coinBalanceLimit = krw / numOfCoins    # coin balance can be purchased until 1/3 * krw 

# Start auto trading
while True:
    try:
        now = datetime.datetime.now()                                         # current time
        minute = now.minute
        second = now.second

        if not (minute == 29 or minute == 59 and 55 <= second <= 59):                                # XX:00:00 ~ XX:28:59 or XX:30:00 ~ XX:58:59                                                                
            BTC_target_price  = get_target_price("KRW-BTC",  k1)              # Set target price 
   
            BTC_current_price  = pyupbit.get_current_price("KRW-BTC")          # Current BTC price
            #print(BTC_target_price, BTC_current_price)

            KRW_BTC_price  = 1 / BTC_current_price

            if BTC_target_price < BTC_current_price:                           # Current BTC price > Target price -> Purchase           
                if krw > 5000 and not BTCBUY:                                               
                    print("BTC  | target price is: %d, current price is: %d" %(BTC_target_price, BTC_current_price))
                    #upbit.buy_market_order("KRW-BTC", (krw//3)*0.9995)           
                    KRWB = KRWB - krw 
                    BTCB = BTCB + KRW_BTC_price * (krw )
                    BTCBUY = True
                    print("%s || Purchase %f BTC coin." %(now, krw ))
                    print_myBalance()
 
        else:                                                             # 08:59:01 ~ 09:00:00
            btc = get_balance("KRW-BTC")                                  # Check balance of BTC, SAND, MANA

            # reset k
            k1 = bestk.get_bestk("KRW-BTC")

            BTC_current_price  = pyupbit.get_current_price("KRW-BTC")     # Current BTC price

            BTCBUY  = False


            if btc * BTC_current_price > 5000:                              # BTC > 5000
                #upbit.sell_market_order("KRW-BTC", btc*0.9995)             # Sell all of them  
                KRWB += btc * BTC_current_price * 0.9995
                BTCB = BTCB - btc
                print("%s || Sell %f BTC coin with %f value" %(now, btc, BTC_current_price))
                print_myBalance()    
        
            krw = get_balance("KRW")      # current krw balance
            coinBalanceLimit = krw / numOfCoins    # coin balance can be purchased until 1/3 * krw 
        time.sleep(0.8)

    except Exception as e:
        print(e)
        time.sleep(1)