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

print_myBalance()