# bertopic-twitterverse
Optimizing BERTopic to the 117th U.S. Congress Twitterverse

This repo contains the materials developed in the context of my master thesis. Its aim was to optimize BERTopic for Twitter data, interpreting its results in the context of the 117th U.S. Congress Twitterverse. It also provides a tool for visualizing the data at hand. NER is also performed, although it was not included in the final document.

### Materials
  ##### Data and Code
  - results-01.csv: original twitter data of selected congress members
  - main.py: code for running preprocessing, NER and topic extraction
    - preprocessing.py: implementation of preprocessing steps
    - NER.py: implementation of NER steps
    - topic_extraction.py: implementation of BERTopic extraction
    
  ##### Data Visualization
  - shiny/topic_data.csv: cleaned topics for visualization
  - shiny/app.R: visualization tool
 
  ##### Thesis Contents
  - EDA.ipynb: Exploratory Data Analysis, corresponds to chapter 4
  - BERTopic-Extraction.ipynb: contains the analysis performed for chapter 5 (global topic extraction)
  - BERTopic-CaseStudy.ipynb: contains the analysis performed for chapter 6 (interval data topic extraction and interpretation under Moral Foundations Framework)
