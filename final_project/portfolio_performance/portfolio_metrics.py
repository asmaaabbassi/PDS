import statistics
import pandas as pd
import csv
import math
from datetime import datetime
from datetime import timedelta
import numpy as np

portofolio_df = pd.read_csv(
    '../trading_methodologies/trading_methodologies.csv')
portfolio_df_method = pd.read_csv(
    '../trading_methodologies/trading_methodologies.csv', usecols=[1], skiprows=0)
portfolio_df_assetprice = pd.read_csv(
    '../trading_methodologies/trading_methodologies.csv', usecols=[1, 5, 4, 7], skiprows=0)
portfolio_df_assetweight = pd.read_csv(
    '../trading_methodologies/trading_methodologies.csv', usecols=[1, 4], skiprows=0)
portfolio_df_amount = pd.read_csv(
    '../trading_methodologies/trading_methodologies.csv', usecols=[6], skiprows=0)
portfolio_df_amount_method = pd.read_csv(
    '../trading_methodologies/trading_methodologies.csv', usecols=[1, 6], skiprows=0)
df_time = pd.read_csv(
    '../trading_methodologies/trading_methodologies.csv', usecols=[0], skiprows=0)
portfolio_df_total = pd.read_csv(
    '../trading_methodologies/trading_methodologies.csv', usecols=[7], skiprows=0)
portfolio_df_total_method = pd.read_csv(
    '../trading_methodologies/trading_methodologies.csv', usecols=[1, 7], skiprows=0)


stocks_df = pd.read_csv(
    '../data_harvesting/amundi-msci-wrld-ae-c.csv', usecols=[0, 1])
cbonds_df = pd.read_csv(
    '../data_harvesting/ishares-global-corporate-bond.csv', usecols=[0, 1])
sbonds_df = pd.read_csv(
    '../data_harvesting/db-x-trackers-ii-global-sovereign-5.csv', usecols=[0, 1])
gold_df = pd.read_csv('../data_harvesting/spdr-gold-trust.csv', usecols=[0, 1])
usd_df = pd.read_csv('../data_harvesting/usdollar.csv', usecols=[0, 1])

inv_date = datetime(2020, 7, 1)
inv_period = 3


def volatilityofasset(duration, start_date=None):
    lis = list()
    temp = list()
    if start_date is None:
        start_date = inv_date
    for x in ['../data_harvesting/amundi-msci-wrld-ae-c.csv',
              '../data_harvesting/ishares-global-corporate-bond.csv', '../data_harvesting/db-x-trackers-ii-global-sovereign-5.csv',
              '../data_harvesting/spdr-gold-trust.csv', '../data_harvesting/usdollar.csv']:
        date = pd.read_csv(x, usecols=[0], skiprows=0)
        date_reverse = date[::-1]
        date_list = date_reverse.iterrows()
        price = pd.read_csv(x, usecols=[1])
        esp = list()
        price_reverse = price[::-1]
        price_list = price_reverse.iterrows()
        for j, r in price_list:
            esp.append(r['Price'])
        for i, row in date_list:
            if datetime.strptime(str(row['Date']), '%b %d, %Y') <= start_date + timedelta(days=duration):
                temp.append(esp[0])
                del esp[0]
            else:
                break
        vol = (statistics.stdev(temp)/sum(temp))*len(temp)*100
        lis.append(vol)
        temp = list()
    return lis


def volatilityofportfolio(allocation, method):
    new_df = portofolio_df.loc[ (portofolio_df['Allocation no'] == allocation) & (portofolio_df['Trading method'] == method) ]
    portfolio_total = new_df[['Trading method', 'Total spending']].iterrows()
    res=[]
    for  ind, meth in portfolio_total:
            if meth[0] == method:
                res.append(meth[1])
            elif (method == 'One-off' and meth[0] == 'Oneoff-rebal') or (method == 'Oneoff-rebal' and meth[0] == 'DCA') or (method == 'DCA' and meth[0] == 'DCA-rebal'):
                break
    values = (np.add.reduceat(res, np.arange(0,len(res),5))).tolist()
    if len(values) < 2:
        return 0
    else:
        return statistics.stdev(values)/sum(values)*len(values)*100


def cost(allocation, method):
    new_df = portofolio_df.loc[(portofolio_df['Allocation no'] == allocation) & (
        portofolio_df['Trading method'] == method)]
    result = []
    date_end = 'Oct 01, 2020'
    rows = new_df.iloc[-5:]
    row_stocks, row_cbonds, row_sbonds, row_gold, row_cash = rows.iloc[
        0], rows.iloc[1], rows.iloc[2], rows.iloc[3], rows.iloc[4]
    result.append(row_stocks['Amount to buy'] *
                  float(stocks_df.loc[stocks_df.Date == date_end]['Price']))
    result.append(row_cbonds['Amount to buy'] *
                  float(cbonds_df.loc[cbonds_df.Date == date_end]['Price']))
    result.append(row_sbonds['Amount to buy'] *
                  float(sbonds_df.loc[sbonds_df.Date == date_end]['Price']))
    result.append(row_gold['Amount to buy'] *
                  float(gold_df.loc[gold_df.Date == date_end]['Price']))
    result.append(row_cash['Amount to buy'] * 1)
    cost = sum(result)
    return cost


def returns(allocation, method):
    new_df = portofolio_df.loc[(portofolio_df['Allocation no'] == allocation) & (
        portofolio_df['Trading method'] == method)]
    cost = 100000
    result = []
    date_end = 'Oct 01, 2020'
    rows = new_df.iloc[-5:]
    row_stocks, row_cbonds, row_sbonds, row_gold, row_cash = rows.iloc[
        0], rows.iloc[1], rows.iloc[2], rows.iloc[3], rows.iloc[4]
    result.append(row_stocks['Amount to buy'] *
                  float(stocks_df.loc[stocks_df.Date == date_end]['Price']))
    result.append(row_cbonds['Amount to buy'] *
                  float(cbonds_df.loc[cbonds_df.Date == date_end]['Price']))
    result.append(row_sbonds['Amount to buy'] *
                  float(sbonds_df.loc[sbonds_df.Date == date_end]['Price']))
    result.append(row_gold['Amount to buy'] *
                  float(gold_df.loc[gold_df.Date == date_end]['Price']))
    result.append(row_cash['Amount to buy'] * 1)
    portofolio_value = sum(result)
    return (portofolio_value - cost)/cost * 100


with open('portfolio_metrics.csv', mode='w', newline='') as csvfile:
    print('open')
    csv.writer(csvfile).writerow(
        ['Allocation', 'Method', 'Cost',  'Volatility', 'Return'])
    for method in ['One-off', 'Oneoff-rebal', 'DCA', 'DCA-rebal']:
        for allocation in range(1, 10627):
            print('.', end='', flush=True)
            a, b, c = cost(allocation, method), volatilityofportfolio(
                allocation, method), returns(allocation, method)
            csv.writer(csvfile).writerow([allocation, method, a, b, c])
print('ok')

with open('asset_volatility.csv', mode='w', newline='') as csvfile:
    csv.writer(csvfile).writerow(['Asset', 'Duration', 'Volatility'])
    for i in [0, 30, 180, 360]:
        s = volatilityofasset(i)
        assetas = ['Stocks', 'Cbonds', 'svonds', 'Gold', 'USD']
        for t in range(5):
            csv.writer(csvfile).writerow([assetas[t], i, s[t]])