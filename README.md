### AnalyzeStock - sentiment analysis of news header
Having row scraped html files as input, AnalyzeStock returns sentiment polarity of the news headers for a particular stock. Useser can feed in html files for multiple stocks, and get a summary results for all the stocks and the timeperiod, or pick up a certain day and a certain stock. 

### Installation
Using the command promt: pip install git+https://github.com/springlaughing/StockSentiment.git#Egg=AnalyzeStock

### Example usage

>**from** AnalyzeStock.News **import** SentimentAnalyzer<br>
>sent = SentimentAnalyzer('stock_news_dataset')<br>
>sent.plot_scores(single_day=False)<br>
