#from flask import Flask,jsonify
from flask import Response,Flask, request 
import pandas as pd
import yfinance as yf
import pandas_ta as ta
from datetime import datetime, timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer #  pip install vaderSentiment

from bs4 import BeautifulSoup as bs
import requests

app = Flask(__name__)

url="https://fr.coinalyze.net/?order_by=oi_24h_pchange&order_dir=desc"
response_req = requests.get(url)
print(response_req.content)

def sentiment_scores(sentence):

    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()

    # polarity_scores method of SentimentIntensityAnalyzer
    # object gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)

    print("Overall sentiment dictionary is : ", sentiment_dict)
    print("sentence was rated as ", sentiment_dict['neg']*100, "% Negative")
    print("sentence was rated as ", sentiment_dict['neu']*100, "% Neutral")
    print("sentence was rated as ", sentiment_dict['pos']*100, "% Positive")

    print("Sentence Overall Rated As", end = " ")

    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05 :
        print("Positive")

    elif sentiment_dict['compound'] <= - 0.05 :
        print("Negative")

    else :
        print("Neutral")

print("\n1st statement :")
sentence = "Geeks For Geeks is the best portal for \
            the computer science engineering students."

# function calling
#sentiment_scores(sentence)

print("\n2nd Statement :")
sentence = "study is going on as usual"
#sentiment_scores(sentence)

print("\n3rd Statement :")
sentence = "I am very sad today."
#sentiment_scores(sentence)


@app.route('/')
def index():    
    return 'Api-flask'

@app.route('/test')
def test():   
    # http://10.1.1.1:5000/login?username=alex&password=pw1
    # username = request.args.get('username')
    username = request.args.get('username')
    return {'user': username}


@app.route('/data')
def data():
    # Define the stock symbol and timeframe
    symbol = 'ICP-USD'
    end_date = datetime.today()
    start_date = end_date - timedelta(days=120)  # 4 months   
    stock_data = yf.download(symbol, start=start_date,end=end_date)
    #print(stock_data)
    return Response(stock_data.to_json(orient="records"), mimetype='application/json')


