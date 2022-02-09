from http.client import MOVED_PERMANENTLY
import pyupbit
import time
import datetime
import schedule

access = "emsE1HCqqG2xLmGcUNEsatFvhU9F1R9lvnBcXynT"
secret = "eUZJrsriOzaIvRLqH6cyxmcfCelNqyaP7BArcLbP"

# initial seed money
KRWB = 210000
BTCB = 0

def print_myBalance():
    print("My Balance")
    print("  KRW: " + str(KRWB))
    print("  BTC: " + str(BTCB))
    print("  TOTAL: %f" %(KRWB + BTCB * pyupbit.get_current_price("KRW-BTC")))
    print()

def get_balance(ticker):
    if ticker == "KRW":
        return KRWB
    elif ticker == "KRW-BTC":
        return BTCB
    return 0

def getSlope(coin):
    df = pyupbit.get_ohlcv(coin, interval="minute1", count=2)  # get ohlcv in 30 days
    time.sleep(0.25)
    df['mean'] = (df['open'] + df['close']) / 2
    df['slope'] = df['mean'] - df['mean'].shift(1)
    #print(df)
    return df['slope'][1]

# Log in
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

while True:
    try:
        now = datetime.datetime.now()
        if now.second != 0:
            continue

        krw = get_balance("KRW")
        btc = get_balance("KRW-BTC")

        now = datetime.datetime.now()
        BTC_current_price  = pyupbit.get_current_price("KRW-BTC")

        KRW_BTC_price = 1 / BTC_current_price
        
        slope = getSlope("KRW-BTC")

        if slope > 30000 and krw > 0:       
            money = krw / 1.0005
            fee = money * 0.0005
            KRWB = 0
            BTCB = BTCB + KRW_BTC_price * money 
            print("TIME: %s \nCOIN: BTC \nSLOPE: %f \nPurchase %f at %f price" %(now, slope, krw, BTC_current_price))
            print("Fee is: %f" %fee)
            print_myBalance()
        
        elif slope < 0 and btc > 0:
            fee = btc * BTC_current_price * 0.0005
            KRWB = KRWB + btc * BTC_current_price - fee
            BTCB = 0
            print("TIME: %s \nCOIN: BTC \nSLOPE: %f \nSell %f BTC coin with %f value" %(now, slope, btc, BTC_current_price))
            print("Fee is: %f" %fee)
            print_myBalance()

        else:
            pass

    except Exception as e:
        print(e)
        time.sleep(1)