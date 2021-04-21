import csv
import pandas as pd
from statistics import stdev

portfolio_df = pd.read_csv('../trading_methodologies/trading_methodologies.csv', skiprows = 1)

stocks_df = pd.read_csv('../data_harvesting/amundi-msci-wrld-ae-c.csv')
cbonds_df = pd.read_csv('../data_harvesting/ishares-global-corporate-bond.csv')
sbonds_df = pd.read_csv('../data_harvesting/db-x-trackers-ii-global-sovereign-5.csv')
gold_df = pd.read_csv('../data_harvesting/spdr-gold-trust.csv')
usd_df = pd.read_csv('../data_harvesting/usdollar.csv')                          
                           
                             

def cost(allocation_number= None):
    if allocation_number==None:
        allocation_number=1
    st = portfolio_df[(allocation_number-1)*5]['Weight of asset']
    cb = portfolio_df[(allocation_number-1)*5+1]['Weight of asset']
    sb = portfolio_df[(allocation_number-1)*5+2]['Weight of asset']
    go = portfolio_df[(allocation_number-1)*5+3]['Weight of asset']
    return (st*0.4+(sb+cb)*0.2+go*0.01)/100

def volatility(asset):
    price = list()
    if asset == 'stocks':
        for row in stocks_df:
            price.append(row['Price'])
    if asset == 'cbonds':
        for row in cbonds_df:
            price.append(row['Price'])
    if asset == 'sbonds':
        for row in sbonds_df:
            price.append(row['Price'])
    if asset == 'stocks':
        for row in gold_df:
            price.append(row['Price'])
    if asset == 'usd':
        for row in usd_df:
            price.append(row['Price'])
    return stdev(price)/sum(price)*len(price)*100

def volatilityofportfolio():
    values=list()
    allocation_number=1
    for i,j,k,l,m in stocks_df,cbonds_df,sbonds_df,gold_df,usd_df:
            st = portfolio_df[(allocation_number-1)*5]['Weight of asset']
            cb = portfolio_df[(allocation_number-1)*5+1]['Weight of asset']
            sb = portfolio_df[(allocation_number-1)*5+2]['Weight of asset']
            go = portfolio_df[(allocation_number-1)*5+3]['Weight of asset']
            us = portfolio_df[(allocation_number-1)*5+4]['Weight of asset']
            allocation_number+=1
            values.append((sum(i*st,j*cb,k*sb,l*go,m*us)))
    return stdev(values)/sum(values)*len(values)*100

def Returns():
     st = portfolio_df[1]['Amount to buy']
     cb = portfolio_df[2]['Amount to buy']
     sb = portfolio_df[3]['Amount to buy']
     go = portfolio_df[4]['Amount to buy']
     us = portfolio_df[5]['Amount to buy']
     t = portfolio_df[1]['Asset price']
     c = portfolio_df[2]['Asset price']
     s = portfolio_df[3]['Asset price']
     g = portfolio_df[4]['Asset price']
     t_f = portfolio_df[-5]['Asset price']
     c_f = portfolio_df[-4]['Asset price']
     s_f = portfolio_df[-3]['Asset price']
     g_f = portfolio_df[-2]['Asset price']
     u_f = portfolio_df[-1]['Asset price']
     buy_amount = sum([st,cb,sb,go,us])
     current_amount = sum([st*t_f/t,cb*c_f/c,sb*s_f/s,go*g_f/g,us*u_f])
     return ((current_amount/buy_amount)-1)*100
    
 

with open('trading_metrics.csv', mode = 'x', newline = '') as csvfile:
        csv.writer(csvfile).writerow(['Cost', 'Return'])
        for 
        





