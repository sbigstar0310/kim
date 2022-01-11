
import time
import pyupbit
import datetime

access = "emsE1HCqqG2xLmGcUNEsatFvhU9F1R9lvnBcXynT"
secret = "eUZJrsriOzaIvRLqH6cyxmcfCelNqyaP7BArcLbP"

# 초기 설정 잔고
KRWB = 200000  # 내 원화 잔고
BTCB = 0       # 내 BTC  잔고
STEEMB = 0      
SANDB = 0 

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
    elif ticker == "KRW-STEEM":
        return STEEMB
    elif ticker == "KRW-SAND":
        return SANDB
    return 0

def print_myBalance():
    print("KRW: " + str(KRWB))
    print("BTC: " + str(BTCB))
    print("STEEM: " + str(STEEMB))
    print("SAND: " + str(SANDB))

    #balances = upbit.get_balances()
    #for b in balances:
    #    if b['currency'] == ticker:
    #        if b['balance'] is not None:
    #            return float(b['balance'])
    #        else:
    #            return 0
    #return 0


#def get_current_price(coin):
    #"""현재가 조회"""
    #return pyupbit.get_orderbook(ticker=coin)["orderbook_units"][0]["ask_price"]

print_myBalance()

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-SAND")              # start_time == 09:00
        end_time = start_time + datetime.timedelta(days=1)    # end_time == 다음날 09:00

        if start_time < now < end_time - datetime.timedelta(seconds=10):     # 09:00 < 현재 시간 < 08:59:50
            target_price = get_target_price("KRW-SAND", 0.5)                # 목표가를 정함
            current_SAND_price = pyupbit.get_current_price("KRW-SAND")     # 현재 BTC 가격
            print("target price is: %d, current_SAND_price is: %d" %(target_price, current_SAND_price))
            if target_price < current_SAND_price:                           # 현재 BTC 가격 > 목표가 -> 구매
                krw = get_balance("KRW")                                     # 현재 원화 잔고 조회
                if krw > 5000:                                               # 만약 최소 구매 원화 가격 이상이면
                    #upbit.buy_market_order("KRW-BTC", krw*0.9995)           # 비트코인 구매
                    current_KRW_price = 1 / current_SAND_price
                    KRWB = KRWB - krw                                        # 원화 잔고 감소
                    SANDB = SANDB + krw * current_KRW_price                # BTC  잔고 증가
                    print("코인을 %d 만큼 구매했습니다." %krw)
                    print_myBalance()

        else:                                                               # 08:59:50 ~ 09:00:00
            snd = get_balance("KRW-SAND")                                  # 현재 비트코인 잔고 조회
            if snd > current_KRW_price * 5000:                              # 비트코인 최소 가격(5000원) 이상이면
                #upbit.sell_market_order("KRW-BTC", btc*0.9995)             # 시장에 모두 매도
                KRWB = KRWB + snd * current_SAND_price                     # 원화 잔고 증가
                SANDB  = SANDB - snd                                      # BTC  잔고 감소
                print("코인을 %f 만큼 판매했습니다." %krw)
                print_myBalance()
        
        time.sleep(1)

    except Exception as e:
        print(e)
        time.sleep(1)