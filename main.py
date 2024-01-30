import pandas as pd
import preprocessing, entities, authors

#Conversion Dictionary
conversion = {
    #'Organization' - 5, 'Location' - 5, 'Person' - 5, 'Temporal' - 2
    #nltk
    'ORGANIZATION': 'Organization',
    'LOCATION': 'Location',
    'PERSON': 'Person',
    #spacy
    'ORG': 'Organization',
    'NORP': 'Organization',
    'LOC': 'Location',
    'DATE': 'Temporal',
    'FAC': 'Location',
    #tweetnlp
    'corporation': 'Organization',
    'group': 'Organization',
    'location': 'Location',
    'person': 'Person',
    #flair (ORG and LOC already done for spacy)
    'PER': 'Person'
    #stanza uses the same categories as spacy
}

#read original data
df = pd.read_excel("results-01.xlsx")


# ---------------------------------------------------------------
# Preprocessing

#perform NER preprocessing
ner_df = preprocessing.NER(df)
#perform Topic preprocessing
topic_df = preprocessing.TopicExtraction(ner_df)

#export ner and topic preprocessed data
ner_df.to_json("ner_data.json")
topic_df.to_json("topic_data.json")

# ---------------------------------------------------------------
# NER

#generate a json file with all entities found in a tweet
# entities.vote(df, conversion)

# #'authors' depends on 'entities' file 
# #generate a json file with all entities mentioned by an authors
# authors.entities_per_author()
# #generate a json file with all authors by entity in the data
# authors.authors_per_entity()