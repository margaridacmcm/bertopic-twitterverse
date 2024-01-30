# README
This repo contains the work developed for my master thesis in Data Science (_Decoding U.S. Political Discourse: A Natural Language Processing Automatic Approach to Analyzing Major Politicians' Tweets_, Universidade do Porto).
Its goal was to optimize topic extraction using [BERTopic](https://maartengr.github.io/BERTopic/index.html) applied to 117th U.S. Congress Twitter data. It also provided an interpretation under the context of the [Morality Foundations Theory](https://moralfoundations.org/), and a visualization tool.
Included are scripts done for NER, although they were not included in the final document.

## Materials

### Data and Code

- results-01.csv: original twitter data
- main.py: calls auxiliary functions
  - preprocessing.py: data preprocessing steps
  - NER.py: NER steps
  - topic_extraction.py: topic extraction using BERTopic
 
### Data Visualization
- shiny/app.R: tool for visualizing the topics found
- shiny/topic_data.csv: cleaned data for visualization

### Thesis Contents
- EDA.ipynb: exploratory data analysis done for chapter 4
- BERT Topic Extraction.ipynb: global topic extraction for chapter 5
- BERTopic-CaseStudy.ipynb: monthly topic extraction and interpretation under MFT, chapter 6
