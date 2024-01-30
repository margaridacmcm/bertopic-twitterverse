#preprocess the tweets in two stages, one for adequate for NER and other for Topic Extraction (which builds on the NER preprocessing)
import warnings
warnings.filterwarnings("ignore")
import pandas as pd 
import numpy as np
import re, string
from nltk import ngrams
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter
import matplotlib.pyplot as plt

def NER(df):
    #add party of each user
    color = {
        'RepAdamSchiff': 'blue',
        'AdamSchiff': 'blue',
        'RepAOC': 'blue',
        'AOC': 'blue',
        'RepAndyBiggsAZ': 'red',

        'SenSanders': 'white',
        'BernieSanders': 'white',
        'SenSchumer': 'blue',
        'chuckschumer': 'blue',

        'SenBooker': 'blue',
        'CoryBooker': 'blue',
        'SenWarren': 'blue',
        'ewarren': 'blue',
        'Jim_Jordan': 'red',

        'JoaquinCastrotx': 'blue',
        'JoeBiden': 'blue',
        'POTUS': 'blue',
        'JohnCornyn': 'red',

        'SenJohnKennedy':'red',
        'KamalaHarris': 'blue',
        'VP': 'blue',
        'GOPLeader': 'red',

        'RepLeeZeldin': 'red',
        'SenRubioPress': 'red',
        'marcorubio': 'red',
        'RepMTG': 'red',

        'MarshaBlackburn': 'red',
        'RepMattGaetz': 'red',
        'SenatorRomney': 'red',
        'MittRomney': 'red',

        'TeamPelosi': 'blue',
        'SpeakerPelosi': 'blue',
        'PattyMurray': 'blue',
        'RepJayapal': 'blue',

        'PramilaJayapal': 'blue',
        'RandPaul': 'red',
        'SenRickScott': 'red',
        'LeaderHoyer': 'blue',

        'StenyHoyer': 'blue',
        'SenTedCruz': 'red',
        'JohnFetterman': 'blue',
        'LeaderMcConnell': 'red'
        
    }

    #add account type to each tweet
    account_type = {
        'RepAdamSchiff': 'professional',
        'AdamSchiff': 'personal',
        'RepAOC': 'professional',
        'AOC': 'personal',
        'RepAndyBiggsAZ': 'professional',

        'SenSanders': 'professional',
        'BernieSanders': 'personal',
        'SenSchumer': 'professional',
        'chuckschumer': 'personal',

        'SenBooker': 'professional',
        'CoryBooker': 'personal',
        'SenWarren': 'professional',
        'ewarren': 'personal',
        'Jim_Jordan': 'professional',

        'JoaquinCastrotx': 'professional',
        'JoeBiden': 'personal',
        'POTUS': 'professional',
        'JohnCornyn': 'personal',

        'SenJohnKennedy': 'professional',
        'KamalaHarris': 'personal',
        'VP': 'professional',
        'GOPLeader': 'professional',

        'RepLeeZeldin': 'professional',
        'SenRubioPress': 'professional',
        'marcorubio': 'personal',
        'RepMTG': 'professional',

        'MarshaBlackburn': 'personal',
        'RepMattGaetz': 'professional',
        'SenatorRomney': 'professional',
        'MittRomney': 'personal',

        'TeamPelosi': 'professional',
        'SpeakerPelosi': 'personal',
        'PattyMurray': 'personal',
        'RepJayapal': 'professional',

        'PramilaJayapal': 'personal',
        'RandPaul': 'personal',
        'SenRickScott': 'professional',
        'LeaderHoyer': 'professional',

        'StenyHoyer': 'personal',
        'SenTedCruz': 'professional',
        'JohnFetterman': 'personal',
        'LeaderMcConnell': 'professional'
        
    }
    df['color'] = df['handle'].apply(lambda x: color.get(x))
    df['account_type'] = df['handle'].apply(lambda x: account_type.get(x))
    
    #use only tweets from when Congress 117th was in session: 2021 and 2022


    #remove web characters
    df['tweet'] = df['text'].replace(regex = {'\n': ' ', 
                                    '<br>': ' ', 
                                    '<\br>': ' ',
                                    '<b>': ' ',
                                    '<\b>': ' ',
                                    '&quot;': '"',
                                    '&#39;': '"',
                                    '&amp;': '&'})

    #create new column with '@'s
    df["mentions"] = df['tweet'].apply(lambda x: re.findall(r'@[^ ]+', str(x)))

    #create new column with hashtags
    df['hashtags'] = df['tweet'].apply(lambda x: re.findall(r'#[^ ]+', str(x)))

    #remove 'RT'
    df['tweet'] = df['tweet'].apply(lambda x: re.sub(r'^RT[\s]+', '', str(x)))

    #remove hyperlinks
    df['tweet'] = df['tweet'].apply(lambda x: re.sub(r'https?://[^\s\n\r]+', '', str(x)))

    #remove duplicates
    df = df.drop_duplicates(subset=['text'], keep=False)

    #remove tweets of len < 1
    df['len'] = df['tweet'].apply(lambda x: len(x))
    df = df[df['len'] > 0]

    return df

def TopicExtraction(df):
    #remove stopwords
    stop_words = stopwords.words('english')
    punctuation = string.punctuation 
    punctuation += "’"
    punctuation += "—"
    punctuation += "–"
    punctuation += "´"
    punctuation += "..."
    punctuation += "'s"
    punctuation += "´s"

    stopwords_dict = Counter(stop_words)
    df['tokens'] = df['tweet'].apply(lambda x: [word for sent in sent_tokenize(x) for word in word_tokenize(sent)])
    df['stopwords'] = df['tokens'].apply(lambda x: [w for w in x if w.lower() not in stopwords_dict])
    df['stopwords'] = df['stopwords'].apply(lambda x: [w for w in x if w.lower() not in punctuation])
    df['tweet'] = df['stopwords'].apply(lambda x: ' '.join(x))

    #lemmatize
    lemmatizer = WordNetLemmatizer()    
    df['tweet'] = df['tweet'].apply(lambda x: [lemmatizer.lemmatize(word, pos ='v') for word in word_tokenize(x)])
    df['tweet'] = df['tweet'].apply(lambda x: ' '.join(x))

    #remove tweets of len < 1 -> probably reduced size due to stopword removal
    df['len'] = df['tweet'].apply(lambda x: len(x))
    df = df[df['len'] > 0]
    return df

def n_grams(df, n):
    n_grams = []
    for tweet in df:
        tweet_n_grams = ngrams(tweet.split(), n) 
        for gram in tweet_n_grams:
            n_grams.append(gram)
    grams = Counter(n_grams)
    topgrams = grams.most_common(20)

    #plot top 20 n-grams
    grams_most = []
    vals =[]
    for i in range(len(topgrams)):
        grams_most.append(str(topgrams[i][0]))
        vals.append(topgrams[i][1])
    plt.bar(grams_most, vals)
    plt.xticks(rotation=45)
    plt.show()
    return topgrams

