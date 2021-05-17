# -*- coding: utf-8 -*-
"""
Created on Fri May 14 15:22:23 2021

@author: genya
"""

from bs4 import BeautifulSoup
import os
import datetime
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import matplotlib.pyplot as plt
nltk.download('vader_lexicon')

class StockSentimentAnalyzer:
    """Identify whether negative, positive or neutral news about a stock
    appeared on a particular day or a time period. 
    Process the html files, and analyse the sentiment polarity of 
    news headers for several stocks. 
    
    :param data_derectory: directory with html files.
    :param add_lexicon: add specific words with negative or positive polarity.

    :ivar html_tables: open html files and extract the part needed.
    :ivar parsed_headlines: parse html_tables and extract news headers, 
    stock name, date and time.
    :ivar polarity_scores: get corresponding polarity scores for each news headline
    using the Vader method from NLTK library. 
    """
    
    def __init__(self, data_directory, add_lexicon = {
    'crushes': 10,
    'beats': 5,
    'misses': -5,
    'trouble': -10,
    'falls': -100,
}):
        self.directory = data_directory
        self.add_lexicon = add_lexicon
        self.html_tables = self._get_tables()
        self.parsed_headlines = self._parse()
        self.polarity_scores = self._get_scores()
        
    def _get_tables(self):
        html_tables = {}

        # For every table in the datasets folder...
        for table_name in os.listdir(self.directory):
            table_path = f'{self.directory}/{table_name}'
            # Open as a python file in read-only mode
            table_file = open(table_path, 'r') 
            # Read the contents of the file into 'html'/create beautiful soup instance
            html = BeautifulSoup(table_file)
            # Find 'news-table' in the Soup and load it into 'html_table'
            html_table = html.find(id = 'news-table')
            html_tables[table_name] = html_table
        return html_tables
        
    def _parse(self):
        # Hold the parsed news into a list
        parsed_news = []
        header = []
        dates = []
        for file_name, news_table in self.html_tables.items():
            for x in news_table.findAll('a'):
                header.append([x.get_text()])

        # Iterate through the news
        for file_name, news_table in self.html_tables.items():
            # Iterate through all tr tags in 'news_table'
            for x in news_table.findAll('tr'):
                # Read the text from the tr tag into text
                text = x.get_text() 
                # Split the text in the td tag into a list 
                date_scrape = x.td.text.split()
                # If the length of 'date_scrape' is 1, load 'time' as the only element
                # If not, load 'date' as the 1st element and 'time' as the second
                if len(date_scrape) == 1:
                    time = date_scrape[0]
                else:
                    date = date_scrape[0]
                    time = date_scrape[1]

                # Extract the ticker from the file name, get the string up to the 1st '_'  
                ticker = file_name.split('_')[0]
                # Append ticker, date, time and headline as a list to the 'parsed_news' list
                dates.append([ticker, date, time])
        parsed_news = [*map(lambda x, y: x+y, dates, header)]
        return parsed_news
    
    
    def _get_scores(self):
        vader = SentimentIntensityAnalyzer()
        # Update the lexicon
        vader.lexicon.update(self.add_lexicon)
        columns = ['ticker', 'date', 'time', 'headline']
        # Convert the list of lists into a DataFrame
        scored_news = pd.DataFrame(self.parsed_headlines,columns=columns)
        # Iterate through the headlines and get the polarity scores
        scores = [vader.polarity_scores(headline) for headline in scored_news.headline]
        # Convert the list of dicts into a DataFrame
        scores_df = pd.DataFrame(scores)
        # Join the DataFrames
        scored_news = pd.concat([scored_news, scores_df], axis=1)
        # Convert the date column from string to datetime
        scored_news['date'] = pd.to_datetime(scored_news.date).dt.date
        scored_news_clean = scored_news.drop_duplicates(subset=['headline', 'ticker'])
        return scored_news_clean
    
    def plot_scores(self, single_day = True, date = '2019-01-03', stock = 'fb'):
        """Method of the StockSentiment class that allows to plot sentiment polarity.

        :param single_day: if True - plots scores for a single day.
        Otherwise plots scores for the whole time period for all stocks. 
        :type single_day: bool
        :param date: if 'single_day' set True, the date 'YYYY-MM-DD' should be specified.
        Default: '2019-01-03'.
        :type date: str
        :param stock: if 'single day' set True, stock name should be specified. Default: 'fb'.
        Should be like in the names of original html files, e.g. 'tsla' or 'fb'. 
        :type stock: str
        :return: bar plot from matplotlib.pyplot
    
        >>> stock_news_sentiment = StockSentimentround('data_directory')
        >>> stock_news_sentiment.plot_scores(single_day=False)
        bar plot
        """
       
        if single_day == True:
            # Set the index to ticker and date
            one_day = self.polarity_scores.set_index(['ticker', 'date'])
            # Cross-section the fb row
            one_day = one_day.xs(stock)
            # Select the 3rd of January of 2019
            min_date = one_day.index.min().date()
            max_date = one_day.index.max().date()
            format_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            
            if format_date <= max_date and format_date >= min_date:                
                try:
                    one_day = one_day.loc[date]
                    # Convert the datetime string to just the time
                    one_day['time'] = pd.to_datetime(one_day['time']).dt.time
                    # Set the index to time and 
                    one_day = one_day.set_index('time')
                    # Sort it
                    one_day = one_day.sort_index()
                    TITLE = f"Negative, neutral, and positive sentiment for {stock} on {date}"
                    # Drop the columns that aren't useful for the plot
                    plot_day = one_day.drop(columns=['headline', 'compound'])
                    # Change the column names to 'negative', 'positive', and 'neutral'
                    plot_day.columns = ['negative', 'neutral', 'positive']
                    # Plot a stacked bar chart

                    plot_day.plot.bar(figsize = (10, 6), stacked=True, title=TITLE)
                except TypeError:
                    print(f"""No data available for this stock on the choosen day. 
Please choose another date within the range {min_date} and {max_date}.""")
                
            else:
                print(f'Date is out of range. Choose a date between {min_date} and {max_date}.')
                
        else:
            
           # Group by date and ticker columns from scored_news and calculate the mean
            mean_c = self.polarity_scores.groupby(['date', 'ticker']).mean()
            # Unstack the column ticker
            mean_c = mean_c.unstack('ticker')
            # Get the cross-section of compound in the 'columns' axis
            mean_c = mean_c.xs("compound", axis="columns")
            # y-value-borders for neg, pos, neutral compound score (see vader documentation https://github.com/cjhutto/vaderSentiment)
            y1 = 0.05
            y2 = -0.05
            y3 = 1
            y4 = -1
            stocks = ', '.join([mean_c.columns[x] for x in range(len(mean_c.columns))])
            TITLE = f"Daily average sentiment polarity score for stocks: {stocks}"
            mean_c.plot.bar(figsize = (10, 6), title = TITLE)

            plt.axhspan(y1, y2, alpha=0.2, color='yellow', label = 'neutral sentiment area')
            plt.axhspan(y2, y4, alpha=0.2, color = 'red', label = 'negative sentiment area')
            plt.axhspan(y1, y3, alpha=0.2, color = 'green', label = 'positive sentiment area')
            plt.legend()
            plt.ylabel('Compound polarity score')
            plt.show()