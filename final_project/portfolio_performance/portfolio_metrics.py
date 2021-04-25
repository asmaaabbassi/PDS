
import statistics
import pandas as pd
import csv
import math
from datetime import datetime
from datetime import timedelta
import numpy as np


portfolio_df_method = pd.read_csv('../trading_methodologies/trading_methodologies.csv', usecols = [1],skiprows=0)
portfolio_df_assetprice = pd.read_csv('../trading_methodologies/trading_methodologies.csv', usecols = [1, 5, 4,7],skiprows=0)
portfolio_df_assetweight = pd.read_csv('../trading_methodologies/trading_methodologies.csv', usecols = [1, 4],skiprows=0)
portfolio_df_amount = pd.read_csv('../trading_methodologies/trading_methodologies.csv', usecols = [6],skiprows=0)
portfolio_df_amount_method = pd.read_csv('../trading_methodologies/trading_methodologies.csv', usecols = [1, 6],skiprows=0)
df_time = pd.read_csv('../trading_methodologies/trading_methodologies.csv', usecols = [0],skiprows=0)
portfolio_df_total= pd.read_csv('../trading_methodologies/trading_methodologies.csv', usecols = [7],skiprows=0)
portfolio_df_total_method= pd.read_csv('../trading_methodologies/trading_methodologies.csv', usecols = [1, 7],skiprows=0)


stocks_df = pd.read_csv('../data_harvesting/amundi-msci-wrld-ae-c.csv', usecols=[0, 1])
cbonds_df = pd.read_csv('../data_harvesting/ishares-global-corporate-bond.csv', usecols=[0, 1])
sbonds_df = pd.read_csv('../data_harvesting/db-x-trackers-ii-global-sovereign-5.csv', usecols=[0, 1])
gold_df = pd.read_csv('../data_harvesting/spdr-gold-trust.csv', usecols=[0, 1])
usd_df = pd.read_csv('../data_harvesting/usdollar.csv', usecols=[0, 1])

inv_date = datetime(2020, 7, 1)
inv_period = 3

def volatilityofasset(duration, start_date=None):
    lis= list()
    temp= list()
    if start_date is None:
        start_date = inv_date
    for x in  ['../data_harvesting/amundi-msci-wrld-ae-c.csv',
              '../data_harvesting/ishares-global-corporate-bond.csv'
              ,'../data_harvesting/db-x-trackers-ii-global-sovereign-5.csv',
              '../data_harvesting/spdr-gold-trust.csv','../data_harvesting/usdollar.csv']:
         date = pd.read_csv(x, usecols = [0],skiprows=0)
         date_reverse = date[::-1]
         date_list = date_reverse.iterrows()
         price = pd.read_csv(x, usecols = [1])
         esp=list()
         price_reverse = price[::-1]
         price_list = price_reverse.iterrows()
         for j , r in price_list:
             esp.append(r['Price'])
         for i, row in date_list:
            if datetime.strptime(str(row['Date']), '%b %d, %Y')<= start_date + timedelta(days=duration):
                temp.append(esp[0])
                del esp[0]
            else:
                break
         vol = (statistics.stdev(temp)/sum(temp))*len(temp)*100
         lis.append(vol)
         temp = list()
    return lis 

def volatilityofportfolio( method):
    portfolio_total = portfolio_df_total_method.iterrows()
    res=[]
    for  ind, meth in portfolio_total:
            if meth[0] == method:
                res.append(meth[1])
            elif (method == 'One-off' and meth[0] == 'Oneoff-rebal') or (method == 'Oneoff-rebal' and meth[0] == 'DCA') or (method == 'DCA' and meth[0] == 'DCA-rebal'):
                break
    values = (np.add.reduceat(res, np.arange(0,len(res),5))).tolist()
    return statistics.stdev(values)/sum(values)*len(values)*100


def cost(method):
    portfolio_asset_weight = portfolio_df_assetweight.iterrows()
    res = list()
    for  r, meth in portfolio_asset_weight:
            if meth[0] == method:
                res.append(meth[1])
            elif (method == 'One-off' and meth[0] == 'Oneoff-rebal') or (method == 'Oneoff-rebal' and meth[0] == 'DCA') or (method == 'DCA' and meth[0] == 'DCA-rebal'):
                break
    values = [res[i:i+5] for i in range(0,len(res),5)]
    val = [0.4,0.2,0.2,0.01,0]
    total=0
    for l in values:
        total += np.dot(l,val)
    return total


def returns(method):
    portfolio_asset_price = portfolio_df_assetprice.iterrows()
    res = list()
    rev = list()
    temp=0
    tmp=0
    portfolio_reversed = portfolio_df_assetprice[::-1]
    reverse = portfolio_reversed.iterrows()
    for  ind, meth in portfolio_asset_price:
            if meth[0] == method  :
                res.append(meth[3])
                temp+=1
            if (method == 'One-off' and meth[0] == 'Oneoff-rebal') or (method == 'Oneoff-rebal' and meth[0] == 'DCA') or (method == 'DCA' and meth[0] == 'DCA-rebal') or(temp==5):
                break
    for  ind, meth in reverse:
            if meth[0] == method  :
                rev.append(meth[3])
                tmp+=1
            if (meth[0] == 'One-off' and method == 'Oneoff-rebal') or (meth[0] == 'Oneoff-rebal' and method == 'DCA') or (meth[0] == 'DCA' and method == 'DCA-rebal') or(tmp==5):
                break
    buy = sum(res)
    current = sum(rev)
    return ((current/buy)-1)*100  
            



with open('portfolio_metrics.csv', mode = 'w', newline = '') as csvfile:
    csv.writer(csvfile).writerow([ 'Method', 'Cost',  'Volatility', 'Return'])
    for method in ['One-off', 'Oneoff-rebal', 'DCA', 'DCA-rebal']:
            a, b, c = cost(method),volatilityofportfolio(method), returns(method)
            csv.writer(csvfile).writerow([method,a, b, c])

with open('asset_volatility.csv', mode = 'w', newline = '') as csvfile:
        csv.writer(csvfile).writerow(['Asset','Duration','Volatility'])
        for i in  [0,30,180,360]:
            s = volatilityofasset(i)
            assetas = ['Stocks','Cbonds','svonds','Gold','USD']
            for t in range(5):
                csv.writer(csvfile).writerow([assetas[t],i,s[t]])