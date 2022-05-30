from random import random
from time import sleep
from turtle import forward
import yfinance as yf
import pandas as pd
from datetime import datetime, date, timedelta
import sys
import random
from pathlib import Path
from forex_python.converter import CurrencyRates
c = CurrencyRates()

df = pd.read_csv('portfolio.csv', index_col=False)
original_stdout = sys.stdout # Save a reference to the original standard output

pd.set_option('display.max_columns', None)
pd.options.mode.chained_assignment = None 


def get_balance():
    funds = open('funds.txt', 'r')
    balance = float(funds.read())
    funds.close()
    return balance


def update_balance(new_balance):
    funds = open('funds.txt', 'w')
    funds.write(str(new_balance))
    funds.close()


def display_portfolio():
    funds = open('funds.txt', 'r')
    balance = float(funds.read())
    funds.close()

    print("\n---")
    print(df,"\n")
    print("Your balance is: " + str(balance) + " USD")
    print("\n---\n")


def save_portfolio():
    df.to_csv('portfolio.csv', index=False)
    print("portfolio successfully saved!")


run = True

print("Loading...")


def confirmationCard(operation, userInput, sharesQuantity, currentDate, cost, stockPrice):
    print("Operation Type  | Spot\n")
    print("Ticker          |",userInput,"\n")
    print("Market          | Capitals\n")
    print("Portfolio       | Nayra1316\n")
    print("Buy/Sell        |", operation,"\n")
    print("Date            |" , currentDate,"\n")
    print("Quantity        |" , sharesQuantity,"\n")
    print("Price           |", stockPrice,"\n" )
    print("Cost            |" , str(cost),"\n")
    print("Fee comission   | N/A")
    print("IVA             | N/A")


def buyStock():
    print("Please introduce the shortname of the company you wish to buy stocks from:")
    userInput = input()

    print("Fetching stock price for " + userInput + "...\n")
    ticker = yf.Ticker(userInput)
    stockInfo = ticker.info

    if stockInfo.get('regularMarketPrice') is not None:

        currentPrice = stockInfo.get('currentPrice')
        fullName = stockInfo.get('longName')

        print("\nDo you wish to buy " + fullName + " stock at " + str(currentPrice) + " USD?")
        print("YES - NO")
        userInput2 = input()

        if userInput2 == "YES":
            print("How many shares do you wish to buy? ")
            sharesQuantity = input()

            cost = int(sharesQuantity) * currentPrice
            currentBalance = get_balance()

            if cost <= currentBalance:

                today = date.today()
                now = datetime.now()
                currentDate = today.strftime("%d-%m-%Y")
                currentTime = now.strftime("%H:%M:%S")

                exists = False
                index = -1

                # update if exists:
                global df 
                for x in range(0, len(df)):
                    if str(df['stock'][x]) == str(userInput):
                        exists = True
                        index = x

                        break

                if exists:

                    df['quantity'][index] = df['quantity'][index] + int(sharesQuantity)
                    df['bought_price'][index] = ((df['bought_price'][index] + currentPrice) / 2)
                    df['date'][index] = currentDate
                    df['hour'][index] = currentTime
                    df['total_cost'][index] = df['total_cost'][index] + cost
                    df['profit-loss'][index] = df['profit-loss'][index] - cost
                    df['stocks_remaining'][index] = df['stocks_remaining'][index] + int(sharesQuantity)

                else:
                    new_row = {'stock': userInput, 'quantity': sharesQuantity, 'bought_price': currentPrice,
                            'date': currentDate, 'hour': currentTime, 'total_cost': cost, 'quantity_sold': 0, 
                            'sold_price': 0, 'total_sell': 0, 'profit-loss': (-1 * cost), 'date_sold': None, 
                            'hour_sold': None, 'stocks_remaining': sharesQuantity}

                    df = df.append(new_row, ignore_index=True)

                print("\n"+str(sharesQuantity) + " shares of " + fullName + " stock bought successfully for " + str(cost)+"\n")
                confCard = input("Do you want to see your confirmation card? YES/NO\n")
                
                fle = Path('confirmationOrder'+userInput+currentTime+currentDate+'.txt')
                fle.touch(exist_ok=True)
                f = open(fle, 'w')

                sys.stdout = f # Change the standard output to the file we created.
                confirmationCard("Buy", userInput, sharesQuantity, currentDate, cost, currentPrice)
                sys.stdout = original_stdout # Reset the standard output to its original value


                if confCard == "YES":
                    confirmationCard("Buy", userInput, sharesQuantity, currentDate, cost, currentPrice)

                save_portfolio()
                update_balance(currentBalance - cost)

            else:
                print("Insufficient funds")

        elif userInput2 == "NO":
            print("Okey\n")
        else:
            print(userInput + " is not a valid option.")

    else:
        print("\nError: " + userInput + " stock couldn't be found. Please verify the shortname.\n")


def buyForward():

    print("Please introduce the name of the X currency you want to buy, X/Y example X/MXN\n")
    userInput = input()

    print("Please introduce the name of the Y currency you want to buy, X/Y example USD/Y\n")
    userInputY = input()

    price = c.get_rate(userInput, userInputY)
    print("The current rate change is:", "{:.2f}".format(price))

    currencyQuantity = input("How many "+userInput+" do you wish to buy?\n")
    total = c.convert(userInput, userInputY, int(currencyQuantity))

    print("The total at the current change will be: ", total)
    daysExecute = input("How many days you will wait to execute your trade?\n")

    forwardPrice = input("Please introduce the forward price you wish\n")
    
    print("Simulatioooooon ..........")
    sleep(1)
    finalPrice = random.uniform(float(forwardPrice)-1, float(forwardPrice)+1)
    print("The price it's " , finalPrice)

    profits = (float(forwardPrice) - float(finalPrice))*float(total)

    print("Your profit it's:", profits)

    today = date.today()
    currentDate = today.strftime("%Y-%m-%d")

    fle = Path('forwardConfirmationOrder'+userInput+currentDate+'.txt')
    fle.touch(exist_ok=True)
    f = open(fle, 'w')

    sys.stdout = f # Change the standard output to the file we created.
    print("Operation Type  | Forward\n")
    print("Ticker          | "+userInput+"/"+userInputY+"\n")
    print("Market          | Derivatives\n")
    print("Portfolio       | Nayra1316\n")
    print("Buy/Sell        | Buy \n")
    print("Date            |", currentDate, "\n")
    print("Quantity        |" , currencyQuantity,"\n")
    print("Price           |", price,"\n" )
    print("Cost            |" , str(finalPrice),"\n")
    print("Exution Date    |", date.today() + timedelta(days = int(daysExecute)),"\n")
    print("Final Profit    |", profits,"\n")
    print("Fee comission   | N/A")
    print("IVA             | N/A")
    sys.stdout = original_stdout # Reset the standard output to its original value

def catch_index_error(list,index):
    try:
        return list[index]
    except IndexError:
        return None

def sellStock():

    weStock = catch_index_error(df.iloc,0)

    if weStock is None :
        print("You don't have any stocks")
    else:
        print("Please select the index of the stock you want to sell:")
        userInput = int(input())
        index = userInput

        row_data = df.iloc[index]

        print(row_data)

        stockName = row_data.get('stock')
        quantity = row_data.get('quantity')

        print("\nYou have " + str(quantity) + " shares of " + stockName + " stock.")
        print("How many shares do you wish to sell?")
        userInput = input()
        sellQuantity = userInput

        while int(userInput) > quantity or int(userInput) <= 0:  # TODO Check for types here
            print("\n"+userInput + " is not a valid input.")
            print("How many shares do you wish to sell?")
            userInput = input()
            sellQuantity = userInput

        print("\nFetching stock price for " + stockName + "...\n")

        ticker = yf.Ticker(stockName)
        stockInfo = ticker.info

        currentPrice = stockInfo.get('currentPrice')
        fullName = stockInfo.get('longName')

        print("Are you sure you wish to sell " + userInput + " stock of " + fullName + " for " + str(currentPrice) + " USD?\n")
        print("YES - NO")
        userInput = input()

        if userInput == "YES":
            today = date.today()
            now = datetime.now()
            currentDate = today.strftime("%d-%m-%Y")
            currentTime = now.strftime("%H:%M:%S")
            currentBalance = get_balance()
            cash = int(currentPrice) * int(sellQuantity)

            df['quantity_sold'][index] = int(sellQuantity)
            df['sold_price'][index] = currentPrice
            df['total_sell'][index] = cash
            df['profit-loss'][index] = (cash - df['total_cost'][index])
            df['date_sold'][index] = currentDate
            df['hour_sold'][index] = currentTime
            df['stocks_remaining'][index] = df['stocks_remaining'][index] - int(sellQuantity)

            fle = Path('confirmationOrder'+userInput+currentTime+currentDate+'.txt')
            fle.touch(exist_ok=True)
            f = open(fle, 'w')

            sys.stdout = f # Change the standard output to the file we created.
            confirmationCard("Sell", userInput, sellQuantity, currentDate, cash, currentPrice)
            sys.stdout = original_stdout # Reset the standard output to its original value

            confCard = input("Do you want to see your confirmation card? YES/NO\n")
            if confCard == "YES":
                confirmationCard("Sell", userInput, sellQuantity, currentDate, cash, currentPrice)

            save_portfolio()

            update_balance(currentBalance + cash)

            print("\nStock successfully sold!")


def moneyMarket():
    print("The current rate of our CETE is 6.5% with a 16% of I.V.A on the rate during 1 year")
    investment = input("How much do you wish to invest in our CETE? \n")
    investment = float(investment)
    totalTime = input("How many years do you want to invest?\n")
    
    interestType = input("Do you want 1 * Simple or 2 * Compound interest? \n")

    i = 0
    sum = 0.0
    total = 0
    if interestType == "1":
        for i in range(int(totalTime)):
            gains = 0.0
            gains = investment * .065
            sum += gains - (gains * .16)
            print("Your gains in year "+ str(i) + " are: " + str(gains - (gains * .16)) + "\n")
        print("Your total profit is: " + str(sum))
    elif interestType == "2":
        for i in range(int(totalTime)):
            gainsAfterFees = 0
            gains = investment * .065

            gainsAfterFees = gains - (gains*.16)

            investment += gainsAfterFees
            total += gainsAfterFees

            print("Your gains in year "+ str(i) + " are: " + str(gainsAfterFees) + "\n")
            print(total)
        print("Your total profit is: " + str(total))

while run:

    print("Please select an option:")
    print("Buy - Sell - Portfolio - Forward - MoneyMarket - Exit")
    x = input()

## Buy action 
    if x == "Buy":
        buyStock()
## sell action
    elif x == "Sell":
        display_portfolio()
        sellStock()

    elif x == "Forward":
        buyForward()
    elif x == "MoneyMarket":
        moneyMarket()
    elif x == "Portfolio":
        
        print("Portfolio selected")

        display_portfolio()

    elif x == "Exit":
        print("Exiting...")
        run = False

    else:
        print("Please select a valid option:")

