from setuptools import setup, find_packages

setup(name='StockSentiment',
     version='0.0.1',
     description='Analysing sentiment polarity of stock news headlines',
     author='springlaughing',
     license = 'MIT License: http://opensource.org/licenses/MIT',
     packages=find_packages(include=['StockSentiment.*']), zip_safe=False, 
     url = 'https://github.com/springlaughing/StockSentiment',
     )