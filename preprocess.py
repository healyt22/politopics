import os, json, string, re
import pandas as pd
import numpy as np
#from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from scipy.sparse import coo_matrix
from argparse import ArgumentParser
import logging as log
log.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p',
                level=log.INFO)

class Preprocess():
    def __init__(self, handle, n_terms=None):
        '''
        Initialize with raw json twitter data from /data directory
        '''
        self.handle = handle
        self.n_terms = n_terms
        base_path = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(base_path,'tweet_data/{0}/'.format(handle))
        tweet_files = os.listdir(data_dir)
        self.data = []
        log.info('Gathering Tweets from ' + data_dir)
        for tweet_file in tweet_files:
            filename = data_dir + tweet_file
            with open(filename) as json_file:
                tweet_raw = json.load(json_file)
            self.data.append(tweet_raw)
        self.tweets = [tweet['text'] for tweet in self.data]
        self.ids = [tweet['id_str'] for tweet in self.data]
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
        word_list = [w for w in words if not w in stop_words]
        if word_list[0] == 'rt':
            word_list = word_list[2:]
        word_str = ' '.join(word_list)
        return(word_list, word_str)

    def clean_tweets(self):
        log.info('Processing Tweets from ' + self.handle)
        self.clean_tweets = []
        self.clean_tweets_str = []
        tweets_filtered = []
        for tweet in self.tweets:
            try:
                clean_tweet_list, clean_tweet_str = self.preprocess(tweet)
                self.clean_tweets.append(clean_tweet_list)
                self.clean_tweets_str.append(clean_tweet_str)
                tweets_filtered.append(tweet)
            except IndexError:
                log.warn('ERROR: ' + tweet)
                continue
        self.tweets = tweets_filtered

    def tf_idf(self):
        self.tfidf = TfidfVectorizer()
        self.td_matrix = self.tfidf.fit_transform(self.clean_tweets_str)
        self.vocab = self.tfidf.get_feature_names()
        self.key_terms = {}
        nonzero_rows = self.td_matrix.nonzero()[0]
        nonzero_cols = self.td_matrix.nonzero()[1]
        for row_idx, col_idx in zip(nonzero_rows, nonzero_cols):
            self.key_terms.update({self.vocab[col_idx]: self.td_matrix[row_idx, col_idx]})
        self.key_terms = dict(sorted(self.key_terms.items(), key=lambda x: x[1], reverse=True))
        if self.n_terms is None:
            self.n_terms = len(self.vocab)
        self.n_key_terms = []
        #print('\n' + str(self.n_terms) + ' Most Important Terms for: ' + self.handle)
        for term, score in list(self.key_terms.items())[0:self.n_terms]:
            #print(' | '.join([term, str(score)]))
            self.n_key_terms.append(term)

    def main(self):
        self.clean_tweets()
        self.tf_idf()

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-t", "--twitter_handle",
        help="Twitter handle to pull tweets against.")
    parser.add_argument("-n", "--n_terms",
        help="Number of top tf-idf terms")
    args = parser.parse_args()
    Preprocess(args.twitter_handle, args.n_terms).main()
