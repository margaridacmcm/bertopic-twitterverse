import pandas as pd
from bertopic import BERTopic
import preprocessing, os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

df = pd.read_excel("results-01.xlsx")
df = preprocessing.NER(df)
df = preprocessing.TopicExtraction(df)

def bert_model(df):
    tweets = df['tweet'].tolist()
    model = BERTopic(language="english", calculate_probabilities=True, verbose=True)
    topics, probs = model.fit_transform(tweets)
    #model.visualize_topics()
    #model.visualize_distribution(probs[200], min_probability=0.02)
    return model

def bert_freq(model):
    freq = model.get_topic_info()
    top_freqs = freq.sort_values(by=['Count'], ascending=False).head(15)
    print(top_freqs)
    #save top_freqs data
    os.makedirs('results', exist_ok=True)  
    top_freqs.to_json('results/frequent_topics.json')
    return None

model = bert_model(df)
bert_freq(model)
