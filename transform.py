import os, json
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from argparse import ArgumentParser
import logging as log
log.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p',
                level=log.DEBUG)

class Transform():
    def __init__(self):
        '''
        Initialize with raw json twitter data from /data directory
        '''
        self.base_path = os.path.dirname(os.path.realpath(__file__))
        self.data_dir = os.path.join(self.base_path,'data')
        self.tweets = os.listdir(self.data_dir)

    def preprocess_(self, text):
        '''
        Some preprocessing will most likely need to be done to
        remove stop words, stemming, perhaps even by using synonyms
        TODO: NLTK library
        '''

    def construct_td_matrix(self, handle):
        '''
        Construct a TD Matrix from inputted tweets data
        TODO: Implement term frequency - inverse document frequency
              (tf-idf) statistic
        '''
        filename = self.base_path + '/data/{0}_tweets.json'.format(handle)
        with open(filename) as json_file:
            data = json.load(json_file)
        tweet_text = [tweet['text'] for tweet in data]
        vec = CountVectorizer()
        X = vec.fit_transform(tweet_text)
        df = pd.DataFrame(X.toarray(), columns=vec.get_feature_names())
        print(df)

    def main(self, handle):
        x = Transform()
        x.construct_td_matrix(handle)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-t", "--twitter_handle",
        help="Twitter handle to pull tweets against.")
    args = parser.parse_args()
    Transform().main(args.twitter_handle)
