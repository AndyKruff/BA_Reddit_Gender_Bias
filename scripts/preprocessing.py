import pandas as pd
from ast import literal_eval
from tqdm.notebook import tqdm
tqdm.pandas()


def read_comment_df():
    # important_columns = ['author','author_fullname', 'body','created_utc', 'name', 'parent_id', 'subreddit','permalink']
    # Read raw dataframe containing all submissions and comments  
    
    df = pd.read_csv("../datasets/reddit_dump.csv") 
    df["body"] = df["body"].fillna('')
       
    # Delete rows with empty body's
    df = df[df["body"] != ""]
    return df


def drop_bots_from_comments(df):
    df_botranks_pasttimes = pd.read_csv("../datasets/botranks_pasttimes.csv")
    df_botranks = pd.read_csv("../datasets/botranks.csv")
    bots = pd.concat([df_botranks_pasttimes, df_botranks])
    bots = bots[["bot_names", "source"]]
    manual_added = {'bot_names': 'reddit-timestamp-bot', 'source': 'manually_added'}
    bots = bots.append(manual_added, ignore_index=True)

    bot = bots.drop_duplicates(["bot_names"], keep="first")
    
    # Remove bot authors from dataset
    df = df[~df['author'].isin(bot["bot_names"].tolist())]
    return df


def sentence_splitting(df):
    import spacy
    
    #load spacy model
    nlp = spacy.load("en_core_web_sm")
    
    # disable all unnecessary pipelines to reduce computational cost
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in []]
    nlp.disable_pipes(*other_pipes)
    
    # Add sentencizer to pipeline for splitting the sentences
    sbd = nlp.create_pipe('sentencizer')
    nlp.add_pipe("sentencizer")

    df["sentence_list"] = df.progress_apply(lambda x: [i.text for i in nlp(x["body"]).sents], axis=1)
    return df


def remove_by_regex_pattern(liste, emoji_pattern):
    import re
    # Remove links and filenames, subreddits (r/...) , users (u/...) , tags with @... and #... 
    for i in range(len(liste)):
        liste[i] = re.sub(r'http(s)?://[^\s]+\.[^\s]+', r'', liste[i], flags=re.MULTILINE | re.DOTALL)
        liste[i] = re.sub(r'(\*+)?\[(.+?)\]\(http(s)?://[^\s]+\.[^\s\)]+\)(\*+)?', r'\2', liste[i],
                          flags=re.MULTILINE | re.DOTALL)
        liste[i] = re.sub(r'r/[^\s]+|u/[^\s]+', r'', liste[i], flags=re.MULTILINE | re.DOTALL)
        liste[i] = re.sub(r'R/[^\s]+|U/[^\s]+', r'', liste[i], flags=re.MULTILINE | re.DOTALL)
        liste[i] = re.sub(r'#[^\s]+', r'', liste[i], flags=re.MULTILINE | re.DOTALL)
        liste[i] = re.sub(r'[^\s]+\.jpg', r'', liste[i], flags=re.MULTILINE | re.DOTALL)
        liste[i] = re.sub(r'[^\s]+\.com', r'', liste[i], flags=re.MULTILINE | re.DOTALL)
        liste[i] = re.sub(r'@[^\s]*', r' ', liste[i], flags=re.MULTILINE | re.DOTALL)

        # Remove emojis

        liste[i] = re.sub(emoji_pattern, r'', liste[i], flags=re.MULTILINE)

        # Remove cpecial characters

        liste[i] = re.sub(r'&amp;#x200B;', r'', liste[i], flags=re.MULTILINE)
        liste[i] = re.sub(r'&amp;nbsp;', r'', liste[i], flags=re.MULTILINE)
        liste[i] = re.sub(r'&amp;', r'', liste[i], flags=re.MULTILINE)
        liste[i] = re.sub(r"&gt;", r' ', liste[i], flags=re.MULTILINE)
        liste[i] = re.sub(r"\n", r' ', liste[i], flags=re.MULTILINE)

        # Removing numbers, dates (completely when deleting punctuations), etc.

        liste[i] = re.sub(r"\d+", r' ', liste[i],
                          flags=re.MULTILINE)  

        # Remove non-alphanumeric chars

        liste[i] = re.sub(r"\W+", r' ', liste[i], flags=re.MULTILINE | re.DOTALL)

        # Remove punctuations

        import string

        liste[i] = str(liste[i]).translate(str.maketrans('', '', string.punctuation))

        liste[i] = re.sub(r"^\s+$", r'', liste[i], flags=re.MULTILINE | re.DOTALL)

        # Remove all non ascii chars

        liste[i] = re.sub(r"[^\u0020-\u007F\n]", "", liste[i])

    return liste


def stopwords_tokenization_lemmatization(df):
    import spacy
    import string
    
    # load spacy model
    nlp = spacy.load("en_core_web_sm")
    
    # Remove unnecessary pipes 
    nlp.remove_pipe('ner')
    nlp.remove_pipe('parser')

    from nltk.corpus import stopwords
    nltk.download('stopwords')
    # get english stopword list from nltk
    stopwords_ = list(stopwords.words('english'))
    
    # remove punctuations from stopwords, to better match tokens
    for i in range(len(stopwords_)):
        stopwords_[i] = str(stopwords_[i]).translate(str.maketrans('', '', string.punctuation))
    
    # Exclude pronouns from the stopword list. Will be used in the analysis later 
    exclude_list = ['he', 'him', 'his', 'himself', 'she', 'shes', 'her', 'hers', 'herself']

    stopwords_ = [x for x in stopwords_ if x not in exclude_list]
    
    # Tokenize, lemmatize and remove stopwords
    df["token_list"] = df.progress_apply(
        lambda x: helper_function_stopwords_tokenization_lemmatization(x["prepro_sentence_list"], nlp, stopwords_),
        axis=1)
    return df


def helper_function_stopwords_tokenization_lemmatization(liste, nlp, stopwords_):
    
    # Tokenized sentences are added as list into the list
    list_of_list_of_tokens = []
    for sentence in liste:
        # Tokens from sentence will be added to this list
        sentence_to_token_list = [] 
        for token in nlp(sentence):
            if token.text.lower() not in stopwords_ and len(
                    token.text) > 1:  # just add lower case tokens to the list, that are not in stopwords and longer than one, 
                                      # two would also be possible, but words like gf (girlfriend) would be excluded 
                sentence_to_token_list.append(token.lemma_.lower()) # Added lowercase lemmtaized term to list
                # liste_3.append(token.text.lower())
        list_of_list_of_tokens.append(sentence_to_token_list)

    return list_of_list_of_tokens

if __name__ == "__main__":
    df = read_comment_df()
    df = drop_bots_from_comments(df)
    print("splitting")
    df = sentence_splitting(df)
    import emoji
    import re
    # Define regex pattern for emojis (once)
    emojis = sorted(emoji.EMOJI_DATA, key=len, reverse=True)
    pattern = u'(' + u'|'.join(re.escape(u) for u in emojis) + u')'
    print("regex")
    df["prepro_sentence_list"] = df.progress_apply(lambda x: remove_by_regex_pattern(x["sentence_list"], pattern),
                                                   axis=1)
    print("lemmatization")
    df = stopwords_tokenization_lemmatization(df)
    df.to_csv("../datasets/preprocessed_df.csv")
    df = df.drop(
        columns=["body", "sentence_list", "prepro_sentence_list"],
        axis=1)
    df.to_csv("../datasets/preprocessed_df_sm.csv")