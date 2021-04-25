Title: Data Driven Portfolio Management, group project documentation
Date: 2021 Spring
Course: Programming for Data Science, UPM Madrid
Created By: Asmaa Abbassi, Marc de Froidefond, Thomas Monnier, Benedek Király

Structure of files:

|--- README.md 
|
├───data_harvesting---|--data_harvesting.py
|                     |--amundi-msci-wrld-ae-c.csv
|                     |--db-x-trackers-ii-global-sovereign-5.csv
|                     |--ishares-global-corporate-bond.csv
|                     |--spdr-gold-trust.csv
|                     |--usdollar.csv
|
├───portfolio_allocations---|--portfolio_allocations.py
|                           |--portfolio_allocations.csv
|
├───portfolio_performance---|--portfolio_metrics.py
|                           |--portfolio_metrics.csv
|                           |--asset_volatility.csv
|
└───trading_methodologies---|--oneoff.py
|                           |--oneoff_rebalancing.py
|                           |--DCA.py
|                           |--DCA_rebalancing.py
|                           |--missing_value.py
|                           |--main.py
|                           |--trading_methodologiescsv.zip (an archive of the csv file)
|
|---report.pdf


Description of files and directories in the project:

Instructions for running executables:

	Part 1.: Web Scraping
	
Before running data_hardvesting/data_harvesting.py, make sure Google Chrome and ChromeDriver is installed on the    computer. Webscraping can be CPU-heavy, so avoid running other processes while executing the file. As the execution finished, all assets portfolio data will be collected in separated .csv files. 
	
	Part 2.: Data Generation
	
There are two main components of data generation in our project. After generating the portfolio data files in the first part, portfolio_allocations/portfolio_allocations.py can be executed, creating all possible allocation sets for creating portfolio alternatives. This .py executable returns the portfolio_allocation.csv file used in the next step, applying trading methods for our dataset. To create the file for the performance analysis, trading_methodologies/main.py needs to be run, that will create all investment alternatives with the use of the allocations and the scraped datasets from part 1. Values for the amount of money to invest, the date of investment and the number of months to invest for can be changed in the main.py file, altering the amount, inv_date and inv_period variables.  After executing trading methodologies, the input file for our data analysis part will be ready in the trading_methodologies folder.
  
	Part 3.: Data Analysis

To analyze the different methods used in the previous part, we calculated different metrics in the file portfolio_performance/portfolio_metrics.py:
		-Cost:the sum of each individual asset cost multiplied by the weight of the asset in the portfolio.
		-Volatility: the amount of uncertainty or risk related to the size of changes in an asset value
		-Return: the percentage of the profit or loss in the portfolio. 

Information has been collected from the file trading_methodologies/trading_methodologies.csv . Metrics generated are located in the file portfolio_performance/portfolio_metrics.csv .

List of Python modules and files:
	-Chromedriver version 90.0.4430.24
	-Pandas version 1.2.4
	-NumPy version 1.20

Endnotes:
Developers reserve all rights on the entire project including code and documentation. Executables included in the project might run on different environments and versions of Python packages, but development and testing were only done using versions presented above.
