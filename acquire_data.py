from gnews import GNews
import os
from newspaper import Article
import csv
import pandas as pd
import datetime

topics=['accident']
topics=['accident','assassination','birth','coup','eruption','explosion','fire','game','hurricane','miracle','shooting','suicide','wedding']
google_news = GNews(language='en', period='24h')

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
                line=[topic,text,url,published_date]
                writer.writerow(line)
            except:
                print('error')
