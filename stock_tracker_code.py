import requests
import datetime as dt
from twilio.rest import Client
Api_Key_Stock = "stock_api_key"                               #API key for the website Alphavantage for tracking a stock
Api_Key_News = "news_spi_key"                                 #API key for the website for displaying news related to a stock

TW_SID = "twillio_SID"                                        #unique account SID for Twillio account used for messaging the user
TW_AUTH = "twillio_Auth"                                      #unique account Authentication code for twillio account used for messaging the user
STOCK_COMPANY = "Tesla"                                       #Name of the stock to be followed
STOCK_NAME = "TSLA"                                           #Name of the stock to be followed accoring to the Alphavatage website
TW_NUMBER = "Twillio_number"                                  #Number provided by twillio services 
USER_NUMBER = "User_number"                                   #User number that is registered to twillio

# Getting the Stock Information
params = {
    "symbol": STOCK_NAME,
    "apikey":Api_Key_Stock
}

response = requests.get(url="https://www.alphavantage.co/query?function=TIME_SERIES_DAILY", params=params)
response.raise_for_status()

data = response.json()
da = dt.date.today()
yest = da - dt.timedelta(days=2)
tod = da - dt.timedelta(days=1)
tod = str(tod)
yest = str(yest)

closing = float(data["Time Series (Daily)"][yest]["4. close"])
opening = float(data["Time Series (Daily)"][tod]["1. open"])

percentage = (opening - closing) / opening
percentage = percentage * 100
percentage = round(number=percentage, ndigits=2)


#Getting the News related to stock
news_params = {
    "country":"us",
    "q":STOCK_COMPANY,
    "apikey":Api_Key_News, 
}

news_response = requests.get(url="https://newsapi.org/v2/top-headlines", params=news_params)
news_response.raise_for_status()
news = news_response.json()

news_title = news["articles"][0]["title"]
news_description = news["articles"][0]["description"]
news_url = news["articles"][0]["url"]


#Messaging setup
if(percentage > 0):
    stock = str(percentage) + "% △"
elif(percentage == 0):
    stock = "0.00"
else:
    stock = str(percentage) + "% ▽"

text_message = f"Your stocks in {STOCK_COMPANY} : {stock} \nThe news related to your stock is as follows:\n{news_title}\n{news_description}\nFor more information - {news_url}" 


#Twilio setup
client = Client(TW_SID, TW_AUTH)

message  = client.messages.create(
    body=text_message,
    from_=TW_NUMBER,
    to= USER_NUMBER
)

