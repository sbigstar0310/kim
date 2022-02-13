import pyupbit
import numpy as np
import time

def findBest(times, cnt, k):
    # 7일 동안의 OHLCV(open, high, low, close, volume)로 
    # 당일 시가, 고가, 저가, 종가, 거래량에 대한 데이터
    df = pyupbit.get_ohlcv("KRW-MANA", times, count = cnt)
    time.sleep(0.25)

    # 변동폭 * k 계산, (고가 - 저가) * k값
    df['range'] = (df['high'] - df['low']) * k

    # target(매수가), range 컬럼을 한칸씩 밑으로 내림(.shift(1))
    df['target'] = df['open'] + df['range'].shift(1)

    # ror(수익률), np.where(조건문, 참일때 값, 거짓일때 값)
    df['ror'] = np.where(df['high'] > df['target'],df['close'] / df['target'],1)

    # 누적 곱 계산(cumprod) => 누적 수익률
    df['hpr'] = df['ror'].cumprod()

    # Draw Down 계산 (누적 최대 값과 현재 hpr 차이 / 누적 최대값 * 100)
    #df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100

    #MDD 계산
    #print("MDD(%): ", df['dd'].max())

    #엑셀로 출력
    #df.to_excel("dd.xlsx")
    #print(df)
    print("%s, %f, %f" %(times, k, df['hpr'][len(df)-1]))

# 1, 3, 5, 10, 15, 30, 60, 240분봉에 대해서 최대 200개 조회 가능

timeList = ["minute30"]
cnt      = [ 2 * 24 ]
for times, cnt in zip(timeList, cnt):
    for k in np.arange(0, 1.0 ,0.1):
        findBest(times, cnt, k)