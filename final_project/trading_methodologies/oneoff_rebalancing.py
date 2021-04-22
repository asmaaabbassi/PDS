import pandas as pd
import csv
from datetime import datetime
import numpy as np

methodsFile = 'trading_methodologies/trading_methodologies.csv'

oneoff_df = pd.read_csv('trading_methodologies.csv')
oneoff_df = oneoff_df[oneoff_df['Trading method'] == 'One-off']
oneoff_rebal = oneoff_df.copy()
oneoff_rebal =  oneoff_rebal.replace({"One-off": "Oneoff-rebal"})
name_assets = ['stocks', 'cbonds', 'sbonds', 'gold', 'cash']

def new_quantities(assets, allocation, date, prec_portfolio):
    stocks_df, cbonds_df, sbonds_df, gold_df, usd_df = assets

    amount_to_buy = list(prec_portfolio['Amount to buy'])
    stocks_q = amount_to_buy[0]
    cbonds_q = amount_to_buy[1]
    sbonds_q = amount_to_buy[2]
    gold_q = amount_to_buy[3]
    usd_q = amount_to_buy[4]

    stocks_index = stocks_df.loc[stocks_df['Date'] == date.strftime('%b %d, %Y')]
    stocks_price = stocks_index.iloc[0]['Price']
    cbonds_index = cbonds_df.loc[cbonds_df['Date'] == date.strftime('%b %d, %Y')]
    cbonds_price = cbonds_index.iloc[0]['Price']
    sbonds_index = sbonds_df.loc[sbonds_df['Date'] == date.strftime('%b %d, %Y')]
    sbonds_price = sbonds_index.iloc[0]['Price']
    gold_index = gold_df.loc[gold_df['Date'] == date.strftime('%b %d, %Y')]
    gold_price = gold_index.iloc[0]['Price']
    usd_price = 1

    prices = [stocks_price, cbonds_price, sbonds_price, gold_price, usd_price]

    #How much money do I have in total
    total_usd = stocks_q*stocks_price + cbonds_q*cbonds_price + sbonds_q*sbonds_price + gold_q*gold_price + usd_q

    def new_quantity(w, price, total):
        quantity = total*w // price
        return quantity

    new_quantities = []
    for i in range(len(allocation)):
        new_quantities.append(new_quantity(allocation[i], prices[i], total_usd))

    return new_quantities, prices


def rebalancing(assets, allocation_no, allocation, inv_date, nb_months, portfolio, rebal_portfolio):
    rebal_portfolio1 = rebal_portfolio.append(portfolio)
    first_year, first_month = inv_date.year, inv_date.month
    dates = [datetime(first_year, first_month, 15)]
    #Dates à choisir en fonction de s'il existe ou pas
    for i in range(nb_months-1):
        month = inv_date.month + i + 1
        year = first_year + month // 12
        month = month % 12
        if month == 0:
            month = 12
        dates.append(datetime(year, month, 15))
        
    for date in dates:
        prec_portfolio = portfolio[-5:]
        new_portfolio = pd.DataFrame(columns=['Date','Trading method', 'Allocation no', 'Asset', 'Weight of asset', 'Asset price', 'Amount to buy', 'Total spending', 'Investment period'])
        new_quantity, prices = new_quantities(assets, allocation, date, prec_portfolio)
        
        new_portfolio['Date'] = [date.strftime('%b %d, %Y') for _ in range(5)]
        new_portfolio['Trading method'] = ["Oneoff-rebal" for _ in range(5)]
        new_portfolio["Allocation no"] = [allocation_no for _ in range(5)]
        new_portfolio['Asset'] = name_assets
        new_portfolio['Weight of asset'] = allocation
        new_portfolio['Asset price'] = prices
        new_portfolio['Amount to buy'] = new_quantity
        new_portfolio['Total spending'] = np.multiply(prices, new_quantity)
        new_portfolio['Investment period'] = nb_months

        rebal_portfolio1 = rebal_portfolio1.append(new_portfolio)

    return rebal_portfolio1


def oneoff_rebalancing(assets, portfolio_df, amount, inv_date, inv_period):
    stocks_df, cbonds_df, sbonds_df, gold_df, usd_df = assets
    
    rebal_portfolio = pd.DataFrame(columns=['Date','Trading method', 'Allocation no', 'Asset', 'Weight of asset', 'Asset price', 'Amount to buy', 'Total spending', 'Investment period'])
    
    for iteration, row in portfolio_df.iterrows():
        print('.', flush=True, end='')
        initial_portfolio = oneoff_df.loc[oneoff_df['Allocation no'] == iteration + 1]
        rebal_portfolio = rebalancing(assets, iteration + 1, list(row[1:]), inv_date, inv_period, initial_portfolio, rebal_portfolio)
    rebal_portfolio = rebal_portfolio.replace({"One-off": "Oneoff-rebal"}) 
    
    with open(methodsFile, 'a+', newline = '') as file:
        writer = csv.writer(file)
        for x in rebal_portfolio.values.tolist():
            writer.writerow(tuple(x))
    