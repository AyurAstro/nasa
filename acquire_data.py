#this is run daily --there is presently an upper linmit of 100 articles per day per topic
import csv
import datetime
import openai
from gnews import GNews

openai.api_key = 'redacted'

topics=['accident','assassination','birth','coup','eruption','explosion','fire','game','hurricane','miracle','shooting','suicide','wedding']
google_news = GNews(language='en', exclude_websites=['tapinto.net','fashionista.com','romesentinel.com','northsidesun.com','tallahatchienews.ms','abc.net.au','rockpapershotgun.com','spokanecity.org','canyoncourier.com','lfpress.com','beincrypto.com','si.com','business2community.com','nst.com','healthnews.com','calgaryherald.com','kidspot.com','yahoo.com', 'cnn.com', 'imdb.com', 'forbes.com', 'newsweek.com', 'blackstarnews.com', 'barrons.com'])

now=datetime.datetime.now()
dayago=now-datetime.timedelta(1)

google_news.start_date = dayago
google_news.end_date = now
for topic in topics:
    print(topic)
    with open('today_'+topic+'.csv', mode='w',encoding="utf8") as csvfile:
        topic_news = google_news.get_news(topic)
        topic_news1 = []
        for value in topic_news:
            if value not in topic_news1:
                topic_news1.append(value)
        writer=csv.writer(csvfile, delimiter=',',quotechar='"')
        for num in range(len(topic_news1)):
            url=topic_news1[num]['url']
            published_date=topic_news1[num]['published date']
            try:
                article = google_news.get_full_article(url)
                text=article.text[0:999]
                strtext=text.replace('\n',' ')
                response = openai.Completion.create(
                  model="text-curie-001",
                  prompt="On what date, at what time, and in what town did the "+topic+" occur?\n\n"+text,
                  temperature=0,
                  max_tokens=80,
                  top_p=1,
                  frequency_penalty=0.5,
                  presence_penalty=0
                )
                line=[topic,strtext,url,published_date,response["choices"][0]["text"]]
                writer.writerow(line)
            except:
                print('error')
