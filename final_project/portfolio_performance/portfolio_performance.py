import statistics
import pandas as pd
import csv
import math
from datetime import datetime
from datetime import timedelta

portfolio_df_assetprice = pd.read_csv('../trading_methodologies/trading_methodologies.csv', usecols = [5],skiprows=0)
portfolio_df_assetweight = pd.read_csv('../trading_methodologies/trading_methodologies.csv', usecols = [4],skiprows=0)
portfolio_df_amount = pd.read_csv('../trading_methodologies/trading_methodologies.csv', usecols = [6],skiprows=0)
df_time = pd.read_csv('../trading_methodologies/trading_methodologies.csv', usecols = [0],skiprows=0)
portfolio_df_total= pd.read_csv('../trading_methodologies/trading_methodologies.csv', usecols = [7],skiprows=0)

stocks_df = pd.read_csv('../data_harvesting/amundi-msci-wrld-ae-c.csv', usecols=[0, 1])
cbonds_df = pd.read_csv('../data_harvesting/ishares-global-corporate-bond.csv', usecols=[0, 1])
sbonds_df = pd.read_csv('../data_harvesting/db-x-trackers-ii-global-sovereign-5.csv', usecols=[0, 1])
gold_df = pd.read_csv('../data_harvesting/spdr-gold-trust.csv', usecols=[0, 1])
usd_df = pd.read_csv('../data_harvesting/usdollar.csv', usecols=[0, 1])

inv_date = datetime(2020, 7, 1)
inv_period = 3


def linealloc(duration, start_date=None):
    p=0
    if start_date is None:
        start_date = inv_date
    s = df_time.iterrows()
    for index,j in s:
        p = index
        if datetime.strptime(str(j['Date']), '%b %d, %Y') >= start_date + timedelta(days=duration):
            break
    return p

def volatilityofportfolio(duration,start_date=None):
    if start_date is None:
        start_date = inv_date
    S = portfolio_df_total.iterrows()
    res=[]
    for index , r in S:
        res.append(r['Total spending'])
    values = list()
    x=len(res)
    for k in (0, x):
        somme=0
        time = df_time.iterrows()
        for a,b in time:
            if datetime.strptime(str(b['Date']), '%b %d, %Y')<= start_date + timedelta(days=duration):
                for j in range(5):
                    m= k*5+j
                    if (m<=x):
                        somme += res[m]
                values.append(somme)
    return statistics.stdev(values)/sum(values)*len(values)*100



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
         vol = (statistics.stdev(temp)/sum(temp))*len(temp)*100
         lis.append(vol)
         temp = list()
    return lis   

def cost(duration):
    if duration == 0:
        return 0
    l=linealloc(duration)
    s = portfolio_df_assetprice.iterrows()
    res= list()
    q=0
    while q <10+l:
        for i,j in s:
            res.append(j['Asset price'])
            q+=1
    (st,cb,sb,go) = (res[l+i] for i in range(4))
    return (st*0.4+(sb+cb)*0.2+go*0.01)/100

def rets(duration):
    l = linealloc(duration)
    s = portfolio_df_assetprice.iterrows()
    res= list()
    q=0
    while q <10+l:
        for i,j in s:
            res.append(j['Asset price'])
            q+=1
    e = portfolio_df_amount.iterrows()
    tst= list()
    c=0
    while c <10:
        for a,b in e:
            tst.append(b['Amount to buy'])
            c+=1
    st = tst[1]
    cb = tst[2]
    sb = tst[3]
    go = tst[4]
    us = tst[5]
    t = res[1]
    c = res[2]
    s = res[3]
    g = res[4]
    t_f = res[l]
    c_f =res[l+1]
    s_f =res[l+2]
    g_f = res[l+3]
    u_f =res[l+4]
    buy_amount = sum([st,cb,sb,go,us])
    current_amount = sum([st*t_f/t,cb*c_f/c,sb*s_f/s,go*g_f/g,us*u_f])
    return ((current_amount/buy_amount)-1)*100


with open('portfolio_metrics.csv', mode = 'x', newline = '') as csvfile:
    csv.writer(csvfile).writerow(['Duration','Volatilityofportfolio','Cost', 'Returns'])
    for i in  [0,30,60]:
        a,b,c=  volatilityofportfolio(i),cost(i),rets(i)
        csv.writer(csvfile).writerow([i,a,b,c])

