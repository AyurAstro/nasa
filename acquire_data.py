#this is run daily
import os
import csv
import datetime
import openai
import pandas as pd
from gnews import GNews

openai.api_key = 'redacted'

topics=['accident','assassination','birth','coup','eruption','explosion','fire','game','hurricane','miracle','shooting','suicide','wedding']
google_news = GNews(language='en', period='1d')

for topic in topics:
    
    with open('today_'+topic+'.csv', mode='w') as csvfile:
        topic_news = google_news.get_news(topic)
        writer=csv.writer(csvfile, delimiter=',',quotechar='"')
        for num in range(len(topic_news)):
            url=topic_news[num]['url']
            published_date=topic_news[num]['published date']
            try:
                article = google_news.get_full_article(url)
                text=article.text
                response = openai.Completion.create(
                  model="text-curie-001",
                  prompt="In the following text, tell me  in what place the "+topic+" took place, on what day, and at what time.\n\n"+text,
                  temperature=0,
                  max_tokens=60,
                  top_p=1,
                  frequency_penalty=0.5,
                  presence_penalty=0
                )
                line=[topic,text,url,published_date,response["choices"][0]["text"]]
                writer.writerow(line)
            except:
                print('error')
