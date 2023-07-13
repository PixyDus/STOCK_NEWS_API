import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = "U56G3ZKT2WB9FG78"
NEWS_API_KEY = "748f7e26ea1e45ac83d913d8e95b3d9b"
TWILIO_ACC_SID = "your account SID"
auth_token = 'your auth token'

stock_params = {
    "function": "TIME_SERIES_WEEKLY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY
}

response = requests.get(STOCK_ENDPOINT, stock_params)
data = response.json()["Weekly Time Series"]
data_list = [value for (key, value) in data.items()]
last_week = data_list[0]
last_week_closing = last_week["4. close"]
print(last_week_closing)

one_week_previous_to_last_week_data = data_list[1]
one_week_previous_to_last_week_closing_price = one_week_previous_to_last_week_data["4. close"]
print(one_week_previous_to_last_week_closing_price)

difference = float(last_week_closing) - float(one_week_previous_to_last_week_closing_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percentage = round((difference / float(last_week_closing)) * 100)


if abs(diff_percentage) >= .5:
    news_params = {
        "apikey": NEWS_API_KEY,
        "q": COMPANY_NAME
    }
    news_response = requests.get(NEWS_ENDPOINT, news_params)
    articles = news_response.json()["articles"]
    three_articles = articles[:3]


    formatted_articles = [f"{STOCK}: {up_down}{diff_percentage}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in
                          three_articles]
    client = Client(TWILIO_ACC_SID, auth_token)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_='your_number',
            to='where_you_want_send'
        )


