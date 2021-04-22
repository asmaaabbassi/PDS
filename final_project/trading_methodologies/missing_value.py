import pandas as pd

stocks_df = pd.read_csv('data_harvesting/amundi-msci-wrld-ae-c.csv')
cbonds_df = pd.read_csv('data_harvesting/ishares-global-corporate-bond.csv')
sbonds_df = pd.read_csv('data_harvesting/db-x-trackers-ii-global-sovereign-5.csv')
gold_df = pd.read_csv('data_harvesting/spdr-gold-trust.csv')
usd_df = pd.read_csv('data_harvesting/usdollar.csv')

def previous_neighbor(L, n):
    m = 0
    j = 0
    for i, x in enumerate(L):
        if x < n and x > m:
            m = x
            j = i
    return j

def missing_value(df, month):
    df_month = df[df['Date'].str.contains(month)]

    days = []
    for index, row in df_month.iterrows():
        days.append(int(row[0][4:6]))
    
    if 15 not in days:
        index_change = previous_neighbor(days, 15) + df_month.index[0]
        new_value = df_month.iloc[len(df_month)//2]['Date'][0:3] + ' 15' + df_month.iloc[len(df_month)//2]['Date'][6:]
        df.at[index_change, 'Date'] = new_value


def replace():
    files = [stocks_df, cbonds_df, sbonds_df, gold_df, usd_df]
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    for file in files:
        for month in months:
            missing_value(file, month)



        
                        
