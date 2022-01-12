import pyupbit
import time
import numpy as np


def get_ror(ticket, k = 0.5):
    df = pyupbit.get_ohlcv(ticket, "minute30", count=10)  # get ohlcv with 30 minute interval
    time.sleep(0.1)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)

    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'],
                         1)

    ror = df['ror'].cumprod()[-2]
    return ror

def get_bestk(ticket):
    max_ror =  0
    max_k = 0
    for k in np.arange(0.1, 1.0, 0.1):
        ror = get_ror(ticket, k)
        #print("%s: %f, %.1f" %(ticket, ror, k))
        if ror > max_ror:
            max_ror = ror
            max_k = k
    return max_k

#print(get_bestk("KRW-BTC"))
#print(get_bestk("KRW-SAND"))
#print(get_bestk("KRW-MANA"))
