import os, json, string, re
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from scipy.sparse import coo_matrix
from argparse import ArgumentParser
import logging as log
log.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p',
                level=log.DEBUG)

class Preprocess():
    def __init__(self, handle):
        '''
        Initialize with raw json twitter data from /data directory
        '''
        self.handle = handle
        log.info('Processing Tweets from ' + handle)
        base_path = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(base_path,'tweet_data/{0}/'.format(handle))
        tweet_files = os.listdir(data_dir)
        self.data = []
        for tweet_file in tweet_files:
            filename = data_dir + tweet_file
            with open(filename) as json_file:
                tweet_raw = json.load(json_file)
            self.data.append(tweet_raw)
        self.tweets = {(handle + '-' + tweet['id_str']):tweet['text'] \
            for tweet in self.data}
        self.clean_tweets = {}
        self.main()

    def preprocess(self, tweet):
        '''
        Some preprocessing will most likely need to be done to
        remove stop words, stemming, perhaps even by using synonyms
        TODO: NLTK library
        '''
        tweet = re.sub(r"https\S+", "", tweet)
        tokens = word_tokenize(tweet)
        # convert to lower case
        tokens = [w.lower() for w in tokens]
        # remove punctuation from each word
        table = str.maketrans('', '', string.punctuation)
        stripped = [w.translate(table) for w in tokens]
        # remove remaining tokens that are not alphabetic
        words = [word for word in stripped if word.isalpha()]
        # filter out stop words
        stop_words = set(stopwords.words('english'))
        words = [w for w in words if not w in stop_words]
        if words[0] == 'rt':
            words = words[2:]
        #words = ' '.join(words)
        return(words)

    def main(self):
        for tweet_id in self.tweets.keys():
            tweet_i = self.tweets[tweet_id]
            try:
                clean_tweet = self.preprocess(tweet_i)
                self.clean_tweets[tweet_id] = clean_tweet
            except IndexError:
                log.warn('ERROR: ' + tweet_i)
                continue
        #self.build_td()

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-t", "--twitter_handle",
        help="Twitter handle to pull tweets against.")
    args = parser.parse_args()
    Preprocess(args.twitter_handle).main()
