from locale import currency
import time
import pyupbit
import datetime
import bestk

def print_myBalance():
    print("My Balance")
    balances = upbit.get_balances()
    for balance in balances:
        print("  %5s : %s" %(balance['currency'], balance['balance']))

access = "5cI0QdQvmKxYfvyJAIYnwQVaiwnfQfdy4GiOffyo"
secret = "Sz6meGwNRQUr3Irpk0DQ88lKv8igRfO9f7riLDGN"

upbit = pyupbit.Upbit(access, secret)

while True:
    BTC_current_price  = pyupbit.get_current_price("KRW-BTC")         # Current BTC price
    SAND_current_price = pyupbit.get_current_price("KRW-SAND")
    MANA_current_price = pyupbit.get_current_price("KRW-MANA")

    print(BTC_current_price, SAND_current_price, MANA_current_price)
    time.sleep(0.5)
print_myBalance()