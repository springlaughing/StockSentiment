### AnalyzeStock - sentiment analysis of news header
Having row scraped html files as input, AnalyzeStock returns sentiment polarity of the news headers for a particular stock. 
User can feed in html files for multiple stocks, and either get summary results for all the stocks and the timeperiod, or for a certain day and a certain stock. 

### Installation
Using the command promt: <br>
>**pip install** git+https://github.com/springlaughing/StockSentiment.git#Egg=AnalyzeStock

### Example usage

>**from** AnalyzeStock.News **import** SentimentAnalyzer<br>
>sent = SentimentAnalyzer('Your_path_to_dataset')<br>
>sent.plot_scores(single_day=False)<br>
<img width="500" alt="example" src="https://github.com/springlaughing/StockSentiment/blob/main/img/output_example1.png">