import statistics
import pandas as pd
import csv
import math
from datetime import datetime
from datetime import timedelta

portfolio_df_assetprice = pd.read_csv('../trading_methodologies/trading_methodologies.csv', usecols = [5],skiprows=0)
portfolio_df_assetweight = pd.read_csv('../trading_methodologies/trading_methodologies.csv', usecols = [4],skiprows=)
df6 = pd.read_csv('../trading_methodologies/trading_methodologies.csv', usecols = [0],skiprows=1)
df_time = pd.read_csv('../trading_methodologies/trading_methodologies.csv', usecols = [0],skiprows=0)



stocks_df = pd.read_csv('../data_harvesting/amundi-msci-wrld-ae-c.csv', usecols=[0, 1])
cbonds_df = pd.read_csv('../data_harvesting/ishares-global-corporate-bond.csv', usecols=[0, 1])
sbonds_df = pd.read_csv('../data_harvesting/db-x-trackers-ii-global-sovereign-5.csv', usecols=[0, 1])
gold_df = pd.read_csv('../data_harvesting/spdr-gold-trust.csv', usecols=[0, 1])
usd_df = pd.read_csv('../data_harvesting/usdollar.csv', usecols=[0, 1])

inv_date = datetime(2020, 7, 1)
inv_period = 3

alloc_30 = None
alloc_180 = None
alloc_360 = None

def linealloc(duration, start_date=None):
    p=0
    if start_date is None:
        start_date = inv_date
    s = df_time.iterrows()
    for i,j in s:
        if datetime.strptime(str(j['Date']), '%b %d, %Y') == start_date + timedelta(days=duration):
            p=i
            break
    new = list()
    u = portfolio_df_assetweight.iterrows()
    for r,s in u:
        new.append(s['Weight of asset'])
    st = new[p]
    cb = new[p+1]
    sb = new[p+2]
    go = new[p+3]
    us = new[p+4]
    return [st,cb,sb,go,us]


def volatilityofportfolio(duration,start_date=None):
    return 0

def volatilityofasset(duration, start_date=None):
    lis= list()
    temp= list()
    if start_date is None:
        start_date = inv_date
    for x in  ['../data_harvesting/amundi-msci-wrld-ae-c.csv',
              '../data_harvesting/ishares-global-corporate-bond.csv'
              ,'../data_harvesting/db-x-trackers-ii-global-sovereign-5.csv',
              '../data_harvesting/spdr-gold-trust.csv','../data_harvesting/usdollar.csv']:
         df6 = pd.read_csv(x, usecols = [0],skiprows=0)
         R = df6[::-1]
         s = R.iterrows()
         df7 = pd.read_csv(x, usecols = [1])
         esp=list()
         T = df7[::-1]
         v = T.iterrows()
         for j , r in v:
             esp.append(r['Price'])
         for i, row in s:
            if datetime.strptime(str(row['Date']), '%b %d, %Y')<= start_date + timedelta(days=duration):
             temp.append(esp[0])
             del esp[0]
            else:
                break
         vol = statistics.stdev(temp)/sum(temp)*len(temp)*100
         lis.append(vol)
         temp = list()
    return lis   

def cost(duration):
    if duration == 0:
        return 0
    l=linealloc(duration)
    st,cb,sb,go = (x for x in l)
    return (st*0.4+(sb+cb)*0.2+go*0.01)/100

def rets(duration):
    l = linealloc(duration)
    st = portfolio_df[1]['Amount to buy']
    cb = portfolio_df[2]['Amount to buy']
    sb = portfolio_df[3]['Amount to buy']
    go = portfolio_df[4]['Amount to buy']
    us = portfolio_df[5]['Amount to buy']
    t = portfolio_df[1]['Asset price']
    c = portfolio_df[2]['Asset price']
    s = portfolio_df[3]['Asset price']
    g = portfolio_df[4]['Asset price']
    t_f = portfolio_df[l[0]*5]['Asset price']
    c_f = portfolio_df[l[1]*5+1]['Asset price']
    s_f = portfolio_df[l[2]*5+2]['Asset price']
    g_f = portfolio_df[l[3]*5+3]['Asset price']
    u_f = portfolio_df[l[4]*5+4]['Asset price']
    buy_amount = sum([st,cb,sb,go,us])
    current_amount = sum([st*t_f/t,cb*c_f/c,sb*s_f/s,go*g_f/g,us*u_f])
    return ((current_amount/buy_amount)-1)*100


with open('metrics.csv', mode = 'w', newline = '') as csvfile:
    csv.writer(csvfile).writerow(['Duration','Volatilityofportfolio','Cost', 'Returns'])
    for i in  [0,30,180,360]:
        a,b,c=  volatilityofportfolio(i),cost(i),rets(i)
        csv.writer(csvfile).writerow([i,a,b,c])