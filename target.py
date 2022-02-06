import pyupbit
import bestk
import time
import schedule

def get_target_price(ticker, k):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    time.sleep(0.5)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def TCboard():
    print("BTC   | target price is: %d, current price is: %d" %(BTC_target_price, BTC_current_price))
    print("SAND  | target price is: %d, current price is: %d" %(SAND_target_price, SAND_current_price))
    print("MANA  | target price is: %d, current price is: %d" %(MANA_target_price, MANA_current_price))
    print()

schedule.every(3).minutes.do(TCboard)
k1 = bestk.get_bestk("KRW-BTC")
k2 = bestk.get_bestk("KRW-SAND")
k3 = bestk.get_bestk("KRW-MANA")

print("BTC  | %f" %k1)
print("SAND | %f" %k2)
print("MANA | %f" %k3)

while True:
    BTC_target_price  = get_target_price("KRW-BTC",  k1)              # Set target price 
    SAND_target_price = get_target_price("KRW-SAND", k2)              # Find best k in bestk.py - get_bestk()
    MANA_target_price = get_target_price("KRW-MANA", k3)
    
    BTC_current_price  = pyupbit.get_current_price("KRW-BTC")          # Current BTC price
    SAND_current_price = pyupbit.get_current_price("KRW-SAND")
    MANA_current_price = pyupbit.get_current_price("KRW-MANA")
    schedule.run_pending()