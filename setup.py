from setuptools import setup, find_packages

setup(name='AnalyzeStock',
     version='0.0.1',
     description='Analysing sentiment polarity of stock news headlines',
     author='springlaughing',
     license = 'MIT License: http://opensource.org/licenses/MIT',
     packages = find_packages(), 
     zip_safe = False, 
     url = 'https://github.com/springlaughing/StockSentiment',
     dependency_links = ['git+http://github.com/springlaughing/StockSentiment.git#egg=AnalyzeStock']
     )
