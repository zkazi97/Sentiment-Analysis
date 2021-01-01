#%%  Import Packages
import requests 
import pandas as pd
from datetime import datetime, date, timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()

#Define URL and API Key (Key obtained from news api website)
url = 'https://newsapi.org/v2/everything?'
api_key = "f1398f43ec314c18a46cd8d2ce05055d"

#%% Run Querying  Debate Topics
parameters_news = {
    'qinTitle' : "",
    'pageSize' : 100,
    'apikey': api_key,
    'language' : 'en',
    'sort_by' : 'popularity',
    'from' : 
    'to'
    }

# Define queries
queries = [
    'Biden Trump Debate',
    'Biden AND debate',
    'Biden AND records',
    'Biden AND covid',
    'Biden AND economy', 
    'Biden AND race',
    'Biden AND violence',
    'Biden AND election',
    'Biden AND supreme court',
    'Trump AND debate',
    'Trump AND records',
    'Trump AND covid',
    'Trump AND economy', 
    'Trump AND race',
    'Trump AND violence',
    'Trump AND election',
    'Trump AND supreme court',
]

#Define sentiment score based on compound value
def sentiVal(compoundVal):
    if compoundVal == 0:
        score = 'Neutral'
    elif compoundVal > 0:
        score = 'Positive'
    else: 
        score = 'Negative'
    return score

#%% Run queries into dictionary named headlines
    
#Define columns for headlines file
newsdate = []
query = []
title = []
source = []
compound = []
score = []

# Prompt user to input days back to view headlines
back = input('From how many days back would you like to view headlines: ')

# Run queries for each day going back to user input
for d in range(int(back),-1,-1):
    parameters_news['from'] = date.today()-timedelta(days=d)
    parameters_news['to'] = date.today()-timedelta(days=d)

# Perform API call with each query
    for q in queries:
        parameters_news['qinTitle'] = q 
        API_Info = requests.get(url, params = parameters_news)
        newsInfo = API_Info.json()
        
        # Obtain article information
        for article in newsInfo['articles']:
            newsdate.append(parameters_news['from'].strftime("%D"))
            query.append(q)
            title.append(article['title'])
            source.append(article['source']['name'])
            
            # Analyze title if content is not available
            if article['content'] == None:
                article['content'] = article['title']
            
            # Append polarity scores on content 
            senti = sid.polarity_scores(article['content'])
            compound.append(senti['compound'])
            score.append(sentiVal(senti['compound']))

        
# Store lists from each article in dictionary. 
headlines = {'Date': newsdate, 'Query' :  query, 
             'Title' : title, 'Source' : source,
             'Sentiment Value' : compound, 'Sentiment Score' : score }

# Make DataFrame from headlines dictionary
df_titles = pd.DataFrame(headlines)


#%% CSV from headlines dataframe labeled with date (See "Files" after running) 
filepath = 'C:/Users/zaink/documents/Python Scripts/'
filename = filepath + parameters_news['from'].strftime("%B %d") + ' Headlines.csv'
df_titles = df_titles.to_csv(filename)



