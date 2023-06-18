# evaluated daily

import csv
import datetime
import openai
import json
from gnews import GNews
from dateutil.tz import gettz

# Read the OpenAI API key from the config file
with open('config.json', 'r') as file:
    config = json.load(file)

openai.api_key = config['openai_key']

topics=['accident','political assassination','birth','political coup','volcano eruption','explosion','fire','game','religious miracle','shooting','suicide','wedding']

#topics=['shooting','suicide','wedding']

google_news = GNews(language='en', exclude_websites=['etnow.com','charlotteobserver.com','says.com','seattletimes.com','news7noida.com','iheart.com','parade.com','triblive.com','wowt.com','mahoningmatters.com','rvtravel.com','newindianexpress.com','bizjournals.com','chronline.com','middle-east-online.com','ntnews.com.au','onenews.ph','wsj.com','dailytelegraph.com.au','thechronicle.com.au','bringmethenews.com','al.com','herald-citizen.com','thehockeynews.com','newsobserver.com','torontosun.com','news9.com','creators.com','thestreet.com','popkavoice.com','safety4sea.com','theolivepress.es','wafa.ps','news.com.au','windsorstar.com','newsdaytonabeach.com','thejournal-news.net','hsvvoice.com','sunnewsonline.com','mckenziebanner.com','montrealgazette.com','legacy.com','publicpower.org','uniindia.com','environewsnigeria.com','ottawacitizen.com','bangkokpost.com','wng.com','eurasiareview.com','nationalpost.com','bleedingcool.com','keyc.com','tapinto.net','fashionista.com','romesentinel.com','northsidesun.com','tallahatchienews.ms','abc.net.au','rockpapershotgun.com','spokanecity.org','canyoncourier.com','lfpress.com','beincrypto.com','si.com','business2community.com','nst.com','healthnews.com','calgaryherald.com','kidspot.com','yahoo.com', 'cnn.com', 'imdb.com', 'forbes.com', 'newsweek.com', 'blackstarnews.com', 'barrons.com'])

now=datetime.datetime.now(gettz('US/Mountain'))
print(now)

dayago=now-datetime.timedelta(1)
print(dayago)

google_news.start_date = dayago
google_news.end_date = now

for topic in topics:
    print(topic)
    with open('today_'+topic+'.csv', mode='w', encoding="utf8") as csvfile:
        topic_news = google_news.get_news(topic)
        topic_news1 = []
        for value in topic_news:
            if value not in topic_news1:
                topic_news1.append(value)
        writer=csv.writer(csvfile, delimiter=',',quotechar='"')
        print(len(topic_news1))
        for num in range(len(topic_news1)):
            line=[]
            url=''
            text=''
            published_date=''
            response={}   
            url=topic_news1[num]['url']
            published_date=topic_news1[num]['published date']
            try:
                article = google_news.get_full_article(url)
                text = article.text
                if text.find("embargo") == -1:
                    response = openai.Completion.create(
                      model="text-curie-001",
                      prompt="From the following article, tell me on what day, at what time, and in what town the "+topic+" occurred.\n\n"+text[0:4000]+"...",
                      temperature=0.4,
                      max_tokens=80,
                      top_p=1
                    )
                    line=[topic,text,url,published_date,response["choices"][0]["text"]]
                    writer.writerow(line)
            except:
                print('error')
