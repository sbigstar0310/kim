import pyupbit
import time
import numpy as np


def get_ror(ticket, k = 0.5):
    df = pyupbit.get_ohlcv(ticket, "minute30", count=48)  # get ohlcv in 30 days
    time.sleep(0.25)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)

    df['ror'] = np.where(df['high'] > df['target'],
                        df['close'] / df['target'],
                        1)

    ror = df['ror'].cumprod()[-2]
    #print(df)
    return ror

def get_bestk(ticket):
    max_ror =  0
    max_k = 0
    for k in np.arange(0, 1.0, 0.1):
        ror = get_ror(ticket, k)
        #print("%s: %f, %.2f" %(ticket, ror, k))
        if ror > max_ror:
            max_ror = ror
            max_k = k
    return max_k

#print(get_bestk("KRW-BTC"))
#print(get_bestk("KRW-SAND"))
#print(get_bestk("KRW-MANA"))
