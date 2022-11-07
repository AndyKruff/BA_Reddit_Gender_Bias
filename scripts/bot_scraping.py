import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
import pandas as pd

def parse(url):
    # Open pages and ignore missing ssl certificate
    r = requests.get(url, verify=False)
    liste = ["B0tRank","Rank","Bot Name","Score","Good Bot Votes","Bad Bot Votes","Comment Karma","Link Karma","Prev","Next"]

    soup = BeautifulSoup(r.text, features="html.parser")
    lis = [bots.get_text() for bots in soup.findAll('a') if bots.get_text() not in liste]
    print(lis)
    return lis


if __name__ == '__main__':

    # create a list of all urls that neeed to be scraped. Amount was checked manually before
    url_list = []
    for i in range(1,301):
        url_list.append(f"https://botrank.pastimes.eu/?sort=score&page={i}")

    # Define a pool of 10 to run the parse function 10 times in parallel and therefore scrape 10 pages at a time
    p = Pool(10)
    with Pool(10) as p:
        records = p.map(parse, url_list)

    # Create one list from all resulting list of the 300 pages
    flat_list = [item for sublist in records for item in sublist]
    flat_list = list(set(flat_list))

    # Create dataframe and save botnames to csv
    df_botranks_pasttimes = pd.DataFrame(flat_list, columns=["bot_names"])
    df_botranks_pasttimes["source"] = "botranks_pasttimes"
    df_botranks_pasttimes.to_csv("../datasets/botranks_pasttimes.csv")
    #p.map(parse, url_list[:10])
    p.terminate()
    p.join()
