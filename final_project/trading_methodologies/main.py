import pandas as pd
from datetime import datetime

from oneoff import oneoff
from oneoff_rebalancing import oneoff_rebalancing
from DCA import DCA
from DCA_rebalancing import DCA_rebalancing
from missing_value import replace

def main(amount inv_date, inv_period):
    stocks_df, cbonds_df, sbonds_df, gold_df, usd_df = replace([15, 1])
    portfolio_df = pd.read_csv('../portfolio_allocations/portfolio_allocations.csv')
    
    with open("trading_methodologies.csv", "w") as my_empty_csv:
        pass
    
    assets = [stocks_df, cbonds_df, sbonds_df, gold_df, usd_df]
    
    oneoff(assets, portfolio_df, amount, inv_date, inv_period)
    oneoff_rebalancing(assets, portfolio_df, amount, inv_date, inv_period)
    DCA(assets, portfolio_df, amount, inv_date, inv_period)
    DCA_rebalancing(assets, portfolio_df, amount, inv_date, inv_period)
    
    return "CSV file has been created"

main(100000, datetime(2020, 7, 1), 3)
