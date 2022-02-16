from locale import currency
import time
import pyupbit
import datetime
import bestk

def myPro():
    balances = upbit.get_balances() 
    purValue = 0
    curValue = 0

    for balance in balances:
        if balance['currency'] != 'KRW':
            purValue += float(balance['balance']) * float(balance['avg_buy_price'])
            curValue += float(balance['balance']) * pyupbit.get_current_price("KRW-" + balance['currency'])
    
    if purValue == 0:
        return 0
    
    print("Profit is %f%%" %(curValue/purValue * 100 - 100))
    return curValue/purValue * 100 - 100

access = "5cI0QdQvmKxYfvyJAIYnwQVaiwnfQfdy4GiOffyo"
secret = "Sz6meGwNRQUr3Irpk0DQ88lKv8igRfO9f7riLDGN"

upbit = pyupbit.Upbit(access, secret)

#print(myPro())