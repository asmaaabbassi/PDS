# Data Driven Portfolio Management, group project documentation

<div align="center"> Date: 2021 Spring </div>
<div align="center"> Course: Programming for Data Science, UPM Madrid </div>
<div align="center"> Created By: Asmaa Abbassi, Marc de Froidefond, Thomas Monnier, Benedek Király </div>

## Structure of files and description of files and directories in the project:

	|--- README.md 
	|
	├───data_harvesting---|--data_harvesting.py				-- retrieves the data from investing.com
	|                     |--amundi-msci-wrld-ae-c.csv
	|                     |--db-x-trackers-ii-global-sovereign-5.csv
	|                     |--ishares-global-corporate-bond.csv
	|                     |--spdr-gold-trust.csv
	|                     |--usdollar.csv
	|
	├───portfolio_allocations---|--portfolio_allocations.py			-- computes the portfolio allocations
	|                           |--portfolio_allocations.csv
	|
	├───portfolio_performance---|--portfolio_metrics.py			-- calculates the metrics for the given allocations and methodologies
	|                           |--portfolio_metrics.csv
	|                           |--asset_volatility.csv
	|
	└───trading_methodologies---|--oneoff.py				-- executes oneoff for all allocations
	|                           |--oneoff_rebalancing.py			-- executes oneoff rebalancing for all allocations
	|                           |--DCA.py					-- executes DCA for all allocations
	|                           |--DCA_rebalancing.py			-- executes DCA rebalancing for all allocations
	|                           |--missing_value.py				-- replaces the missing values of the data scraped
	|                           |--main.py					-- computes the four trading methodologies
	|                           |--trading_methodologiescsv.zip (an archive of the csv file)
	|
	|---report.pdf								-- analysis of part 3
	|
	|---exercise_statement.pdf						-- description of the project
	|
	|---requirements.txt							-- python packages to be installed



## Instructions for running executables:

First of all, in order to run the algorithms in the three parts of the project, you have to install all the python packages needed.
To do this, run 

	pip install -r requirements.txt

## Part 1.:Web Scraping
	
<div align="justify"> Before running **data_hardvesting/data_harvesting.py**, make sure Google Chrome and ChromeDriver is installed on the computer. Webscraping can be CPU-heavy, so avoid running other processes while executing the file. As the execution finished, all assets portfolio data will be collected in separated .csv files. </div>
Then, run:
	
	python data_harvesting.py
	
Each csv file downloaded has been handly renamed. 
	
## Part 2.: Data Generation
	
<div align="justify"> There are two main components of data generation in our project. After generating the portfolio data files in the first part, **portfolio_allocations/portfolio_allocations.py** can be executed, creating all possible allocation sets for creating portfolio alternatives. This programm returns the portfolio_allocation.csv file used in the next step, applying trading methods for our dataset. To create the file for the performance analysis, **trading_methodologies/main.py** needs to be run. Thanks to different investment alternatives created with the use of the allocations and the scraped datasets from part 1, we generate a csv file with the values for the amount of money to invest, the date of investment etc... The number of months to invest can be changed in the main.py file where you can alter the amount, inv_date and inv_period variables. After executing the trading methodologies, the input file for our data analysis part will be ready in the trading_methodologies folder. </div>

Therefore, run successively in the right folder:

	python portfolio_allocations.py
	
	python main.py

More details:

<div align="justify">Some of the data retrieved from the website investing.com has missing values. For instance, data for the first day of a month and data for the fifteenth can be missing. Since it is quite annoying (because rebalancing occurs every month on the 15th and because investments occur on the first day of a month), we decided to implement an algorithm, **trading_methodologies/missing_value.py**. This algorithm looks at all months for all data and in case that there is no data on the 15th day or the 1st day, then this will happen: data's date for the closest day before the 15th will be replaced by the 15th and data's date for the first day of data of the month will be changed to the 1st. </div>

For example:
<div class="resume">
<div class="resume_class">
    <ul>
    <h4> </h4>
	<li>13/07/2020 becomes 15/07/2020 if there is no data for July 15th, 2020</li>
	<li>03/09/2020 becomes 01/09/2020 if there is no data for September 1st, 2020</li>
    </ul>
</div>
</div>

<div align="justify">You can change anytime the three parameters directly in the main.py code: amount of investment, the date of the beginning of the investment and the number of investing months: </div>

	main(100000, datetime(2020, 7, 1), 3)

## Part 3.: Data Analysis

<div align="justify"> To analyze the different methods used in the previous part, we calculated different metrics in the file **portfolio_performance/portfolio_metrics.py**: </div>
<div class="resume">
<div class="resume_class">
    <ul>
    <h4> </h4>
	<li>Cost: the sum of each individual asset cost multiplied by the weight of the asset in the portfolio</li>
	<li>Volatility: the amount of uncertainty or risk related to the size of changes in an asset value</li>
	<li>Return: the percentage of the profit or loss in the portfolio</li>
    </ul>
</div>
</div>

Thus, run:

	python portfolio_metrics.py
	
<div align="justify"> Information has been collected from the file trading_methodologies/trading_methodologies.csv . Metrics generated are located in the file portfolio_performance/portfolio_metrics.csv . </div>

<div class="resume">
<div class="resume_class">
    <ul>
    <h4>List of Python modules and files:</h4>
	<li>Chromedriver version 90.0.4430.24</li>
	<li>Pandas version 1.2.4</li>
	<li>NumPy version 1.20</li>
    </ul>
</div>
</div>

## Endnotes:

<div align="justify"> Developers reserve all rights on the entire project including code and documentation. Executables included in the project might run on different environments and versions of Python packages, but development and testing were only done using versions presented above. </div>
