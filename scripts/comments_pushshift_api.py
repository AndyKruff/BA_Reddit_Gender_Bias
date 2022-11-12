from psaw import PushshiftAPI
#import praw
import pandas as pd
from datetime import datetime
from time import sleep


# Define list of subreddits to scrape
subreddits = ["TwoXChromosomes","gardening","Parenting","AskMen","AskWomen","unpopularopinion","teenagers",
              "Conservative","funny","technology","science"]



for i in subreddits:
    df = pd.DataFrame()
    # open api port for PushshiftAPI

    api = PushshiftAPI()
    # Define time observation window in POSIX format

    after = int(datetime(2022, 5, 1).timestamp()) - 1
    before = int(datetime(2022, 8, 1).timestamp()) + 1
    while after < before:
        if after < 1659304799:
            # scrape submissions in steps of 22 hours from API for the given subreddit

            reddit_comments = api.search_comments(after=after,before=after + 39744,
                                    subreddit=i,
                                    filter=['author','author_fullname', 'body','id','created_utc', 'name', 'parent_id', 'subreddit','permalink','link_id','score'])
            data=pd.DataFrame(k.d_ for k in reddit_comments)
            df = pd.concat([df, data], ignore_index=True)
            # update the variable after for next iterations observation window

            after += 39744
            print(after)
        else:
            reddit_comments = api.search_comments(after=after,before=after + 2,
                                    subreddit=i,
                                    filter=['author','author_fullname', 'body','id','created_utc', 'name', 'parent_id', 'subreddit','permalink','link_id','score'])
            data=pd.DataFrame(k.d_ for k in reddit_comments)
            df = pd.concat([df, data], ignore_index=True)
          
            after += 79488

        sleep(15)
    print(i)
    df.to_csv(f"../datasets/{i}_comments.csv")
    sleep(60)