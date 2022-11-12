# Bachelor thesis: Analysis of gender bias
in popular Subreddits
**Information**  
 
First examiner: Prof. Dr. Philipp Schaer 
Second examiner: M.Sc. Fabian Haak  

Student: Andreas Kruff  
  
```
Analysis of gender bias in popular Subreddits
```
**Keywords:** NLP, Reddit, Word Embeddings, Gender bias , NRC, WEAT

## Overview


The repository contains the following folders:
- **scripts:** Code for preprocessing the datasets and training the models.
- **experiments:** Code for the analysis of the gender bias. 
- **doc:** Past Presentations for this module can be found here.
- **driver:** Provides driver for Firefox and Chrome (Required for Selenium)
- **models:** Trained models are provided via Sciebo. Permissions were granted for folder "models".
- **datasets:** Contains necessary datasets for preprocessing and sentiment analysis. For reproducing the results additional datasets are provided via Sciebo. Permissions were granted for folder "datasets". Contained datasets are explained below.

Sciebo contains the following datasets:

- **XXX.h5:** Preprocessed datasets, one for each research object.
- **reddit_dump.csv:** Contains submissions and comments for the eleven subreddits within the observation window (not filtered nor preprocessed)   

- **author_metrics.csv:** Contains the calculated user metrics.
- **authors_usergroups_by_kmeans:** Contains the calculated user metrics and the assigned clusters/user groups by kmeans.
- **authors_usergroups_by_decision_rules.csv:** Contains the calculated user metrics and the assigned clusters/user groups by the decision rules.

# Notes:

- To scrape the bots from "https://botranks.com/" a driver (like geckodriver for firefox) needs to be downloaded and put into the system path.

