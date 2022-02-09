import pyupbit
import numpy as np
import time

# 7일 동안의 OHLCV(open, high, low, close, volume)로 
# 당일 시가, 고가, 저가, 종가, 거래량에 대한 데이터
df = pyupbit.get_ohlcv("KRW-BTC", "minute1", count = 60 * 24 * 3)

# 평균가 계산
df['mean'] = (df['open'] + df['close']) / 2

# 최근 2분간 기울기(변동폭) 계산
df['slope'] = df['mean'] - df['mean'].shift(1)

print(df)

KRWB = 210000
BTCB = 0

def findk(k):
    global KRWB
    global BTCB
    lastBTC = 0

    BUY = False
    purValue = 0
    ror = 1.0

    for index, d in df.iterrows():
        lastBTC = d['close']
        
        if d['slope'] > k and KRWB > 0:
            KRW_BTC_price = 1 / d['open']
            money = KRWB / 1.0005
            fee = money * 0.0005
            print("TIME: %s \nCOIN: BTC \nSLOPE: %f \nPurchase %f at %f price" %(index, d['slope'], KRWB, d['open']))
            print("Fee is: %f" %fee)
            KRWB = 0
            BTCB = BTCB + KRW_BTC_price * money
            print_myBalance(d['open'])

        elif d['slope'] < 0 and BTCB > 0:
            fee = BTCB * d['open'] * 0.0005
            print("TIME: %s \nCOIN: BTC \nSLOPE: %f \nSell %f BTC coin with %f value" %(index, d['slope'], BTCB, d['open']))
            print("Fee is: %f" %fee)
            KRWB = KRWB + BTCB * d['open'] - fee
            BTCB = 0
            print_myBalance(d['open'])

    return KRWB + BTCB * lastBTC

def print_myBalance(value):
    global KRWB
    global BTCB

    print("My Balance")
    print("  KRW: " + str(KRWB))
    print("  BTC: " + str(BTCB))
    print("  TOTAL: %f" %(KRWB + BTCB * value))
    print()

print(findk(30000))




# for k in range(0, 100001, 2500):
#     KRWB = 210000
#     BTCB = 0
#     print(k, findk(k))


#print(maxK, maxKWB)

# ror(수익률), np.where(조건문, 참일때 값, 거짓일때 값)
#df['ror'] = np.where(df['high'] > df['target'],df['close'] / df['target'],1)

# 누적 곱 계산(cumprod) => 누적 수익률
#df['hpr'] = df['ror'].cumprod()

# Draw Down 계산 (누적 최대 값과 현재 hpr 차이 / 누적 최대값 * 100)
#df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100

#MDD 계산
#print("MDD(%): ", df['dd'].max())

#엑셀로 출력
#df.to_excel("dd.xlsx")
#print(df)