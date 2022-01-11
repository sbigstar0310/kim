
import time
import pyupbit
import datetime

access = "emsE1HCqqG2xLmGcUNEsatFvhU9F1R9lvnBcXynT"
secret = "eUZJrsriOzaIvRLqH6cyxmcfCelNqyaP7BArcLbP"

# initial seed money
KRWB = 210000
BTCB = 0
SANDB = 0
MANAB = 0

def get_target_price(ticker, k):
    
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    
    # 09:00 return
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

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
    print("KRW: " + str(KRWB))
    print("BTC: " + str(BTCB))
    print("SAND: " + str(SANDB))
    print("MANA: " + str(MANAB))

# Log in
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# Start auto trading
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")                                # start_time == 09:00
        end_time = start_time + datetime.timedelta(days=1)                    # end_time == next day 09:00
        cnt = 0

        if start_time < now < end_time - datetime.timedelta(seconds=30):      # 09:00 < current time < 08:59:30
            BTC_target_price = get_target_price("KRW-BTC", 0.5)               # Set target price
            SAND_target_price = get_target_price("KRW-SAND", 0.5)
            MANA_target_price = get_target_price("KRW-MANA", 0.5)

            BTC_current_price = pyupbit.get_current_price("KRW-BTC")          # Current BTC price
            SAND_current_price = pyupbit.get_current_price("KRW-SAND")
            MANA_current_price = pyupbit.get_current_price("KRW-MANA")

            KRW_BTC_price  = 1 / BTC_current_price
            KRW_SAND_price = 1 / SAND_current_price
            KRW_MANA_price = 1 / MANA_current_price

            print("BTC  | target price is: %d, current price is: %d" %(BTC_target_price, BTC_current_price))
            print("SAND | target price is: %d, current price is: %d" %(SAND_target_price, SAND_current_price))
            print("MANA | target price is: %d, current price is: %d" %(MANA_target_price, MANA_current_price))

            if BTC_target_price < BTC_current_price:
                cnt += 1
            if SAND_target_price < SAND_current_price:
                cnt += 1
            if MANA_target_price < MANA_current_price:
                cnt += 1
            if cnt == 0:
                print()
                continue

            krw = get_balance("KRW") / cnt   

            if BTC_target_price < BTC_current_price:                           # Current BTC price > Target price -> Purchase           
                if krw > 5000:                                               
                    #upbit.buy_market_order("KRW-BTC", (krw/3)*0.9995)           
                    KRWB = KRWB - krw
                    BTCB = BTCB + KRW_BTC_price * krw
                    print("BTC 코인을 %f 만큼 구매했습니다." %krw)
                    

            if SAND_target_price < SAND_current_price:                          # Current SAND price > Target price -> Purchase
                if krw > 5000:                                               
                    #upbit.buy_market_order("KRW-SAND", (krw/3)*0.9995)           
                    KRWB = KRWB - krw
                    SANDB  = SANDB + KRW_SAND_price * krw
                    print("SAND 코인을 %f 만큼 구매했습니다." %krw)
                    

            if MANA_target_price < MANA_current_price:                           # Current MANA price > Target price -> Purchase
                if krw > 5000:                                               
                    #upbit.buy_market_order("KRW-MANA", (krw/3)*0.9995)           
                    KRWB = KRWB - krw
                    MANAB  = MANAB + KRW_MANA_price * krw
                    print("MANA 코인을 %f 만큼 구매했습니다." %krw)
                    
                    
            print_myBalance()
        else:                                                             # 08:59:50 ~ 09:00:00
            btc = get_balance("KRW-BTC")                                  # Check balance of BTC, SAND, MANA
            snd = get_balance("KRW-SAND")   
            mna = get_balance("KRW-MANA")   
            
            BTC_current_price = pyupbit.get_current_price("KRW-BTC")     # Current BTC price
            SAND_current_price = pyupbit.get_current_price("KRW-SAND")
            MANA_current_price = pyupbit.get_current_price("KRW-MANA")

            if btc * BTC_current_price > 5000:                              # BTC > 5000
                #upbit.sell_market_order("KRW-BTC", btc*0.9995)             # Sell all of them  
                KRWB = KRWB + btc * BTC_current_price
                BTCB = BTCB - btc
                print("BTC  코인을 %f 만큼 판매했습니다." %krw)

            if snd * SAND_current_price > 5000:                             # SAND > 5000 
                #upbit.sell_market_order("KRW-SAND", snd*0.9995)            # Sell all of them  
                KRWB = KRWB + snd * SAND_current_price
                SANDB = SANDB - snd
                print("SAND 코인을 %f 만큼 판매했습니다." %krw)

            if mna * MANA_current_price > 5000:                             # MANA > 5000
                #upbit.sell_market_order("KRW-MANA", mna*0.9995)            # Sell all of them  
                KRWB = KRWB + mna * MANA_current_price
                MANAB = MANAB - mna
                print("MANA 코인을 %f 만큼 판매했습니다." %krw)
            
            print_myBalance()
        
        print()
        time.sleep(1)

    except Exception as e:
        print(e)
        time.sleep(1)