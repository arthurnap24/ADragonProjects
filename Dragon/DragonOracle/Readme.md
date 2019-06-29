Create a stock suggester app that takes symbols from the web, and presents them in a web page or app. Need to use finviz and yahoo finance in conjunction to achieve this. The idea is not to create a fully tweak able app, but add enough parameterization to enable users to change the values of factors that will “obviously” affect price action.



1. Use Finviz to scrape psi and a web scraping framework to get all the symbols in sorted ascending order. Parameterize the RSI top end as well. Use this link: https://finviz.com/screener.ashx?v=111&f=sh_avgvol_o1000,ta_rsi_os40&ft=3&o=rsi



2. Use Yahoo Finance’s Full Screen chart to scrape:

- support

- resistance

- stop loss

- bullishness on short, mid, and long term



3. Look for stocks that have “potential growth” based on how far it’s current price is relative to the support and resistance. 

- Enable the client software to tweak this parameter to the desired distance (in percentage) from the support or resistance. 

- At the same time, for data gathering, we can try all possible percentages and see which one is more accurate at predicting highs and lows.



4. Present these data to the client app:

- symbols that passed RSI criteria

- support

- resistance

- how far the current price is from support/resistance (as possible percentage gain)

- stop loss price from yahoo

- take profit price (75% of resistance—this is another parameter we can run our simulations with and see which take home profit percentages is safest)