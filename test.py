
import time
import pyupbit
import datetime

access = "emsE1HCqqG2xLmGcUNEsatFvhU9F1R9lvnBcXynT"
secret = "eUZJrsriOzaIvRLqH6cyxmcfCelNqyaP7BArcLbP"

# 초기 시드머니
KRWB = 210000
BTCB = 0
SANDB = 0
MANAB = 0

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    # 09:00 리턴
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
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

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")              # start_time == 09:00
        end_time = start_time + datetime.timedelta(days=1)    # end_time == 다음날 09:00
        cnt = 0

        if start_time < now < end_time - datetime.timedelta(seconds=30):     # 09:00 < 현재 시간 < 08:59:30
            BTC_target_price = get_target_price("KRW-BTC", 0.5)                # 목표가를 정함
            SAND_target_price = get_target_price("KRW-SAND", 0.5)
            MANA_target_price = get_target_price("KRW-MANA", 0.5)

            BTC_current_price = pyupbit.get_current_price("KRW-BTC")     # 현재 BTC 가격
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

            if BTC_target_price < BTC_current_price:                           # 현재 BTC 가격 > 목표가 -> 구매           
                if krw > 5000:                                               # 만약 최소 구매 원화 가격 이상이면
                    #upbit.buy_market_order("KRW-BTC", (krw/3)*0.9995)           # 비트코인 구매
                    KRWB = KRWB - krw
                    BTCB = BTCB + KRW_BTC_price * krw
                    print("BTC 코인을 %f 만큼 구매했습니다." %krw)
                    

            if SAND_target_price < SAND_current_price:                           # 현재 BTC 가격 > 목표가 -> 구매
                if krw > 5000:                                               # 만약 최소 구매 원화 가격 이상이면
                    #upbit.buy_market_order("KRW-SAND", (krw/3)*0.9995)           # 비트코인 구매
                    KRWB = KRWB - krw
                    SANDB  = SANDB + KRW_SAND_price * krw
                    print("SAND 코인을 %f 만큼 구매했습니다." %krw)
                    

            if MANA_target_price < MANA_current_price:                           # 현재 BTC 가격 > 목표가 -> 구매
                if krw > 5000:                                               # 만약 최소 구매 원화 가격 이상이면
                    #upbit.buy_market_order("KRW-MANA", (krw/3)*0.9995)           # 비트코인 구매
                    KRWB = KRWB - krw
                    MANAB  = MANAB + KRW_MANA_price * krw
                    print("MANA 코인을 %f 만큼 구매했습니다." %krw)
                    
                    
            print_myBalance()
        else:                                                               # 08:59:50 ~ 09:00:00
            btc = get_balance("KRW-BTC")                                  # 현재 비트코인 잔고 조회
            snd = get_balance("KRW-SAND")   
            mna = get_balance("KRW-MANA")   
            
            BTC_current_price = pyupbit.get_current_price("KRW-BTC")     # 현재 BTC 가격
            SAND_current_price = pyupbit.get_current_price("KRW-SAND")
            MANA_current_price = pyupbit.get_current_price("KRW-MANA")

            if btc * BTC_current_price > 5000:                              # 비트코인 최소 가격(5000원) 이상이면
                #upbit.sell_market_order("KRW-BTC", btc*0.9995)              # 시장에 모두 매도  
                KRWB = KRWB + btc * BTC_current_price
                BTCB = BTCB - btc
                print("BTC  코인을 %f 만큼 판매했습니다." %krw)

            if snd * SAND_current_price > 5000:                              # 비트코인 최소 가격(5000원) 이상이면
                #upbit.sell_market_order("KRW-SAND", snd*0.9995)              # 시장에 모두 매도  
                KRWB = KRWB + snd * SAND_current_price
                SANDB = SANDB - snd
                print("SAND 코인을 %f 만큼 판매했습니다." %krw)

            if mna * MANA_current_price > 5000:                              # 비트코인 최소 가격(5000원) 이상이면
                #upbit.sell_market_order("KRW-MANA", mna*0.9995)              # 시장에 모두 매도  
                KRWB = KRWB + mna * MANA_current_price
                MANAB = MANAB - mna
                print("MANA 코인을 %f 만큼 판매했습니다." %krw)
            
            print_myBalance()
        
        print()
        time.sleep(1)

    except Exception as e:
        print(e)
        time.sleep(1)