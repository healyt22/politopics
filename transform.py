import os, json, string, re
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from argparse import ArgumentParser
import logging as log
log.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p',
                level=log.DEBUG)

class Transform():
    def __init__(self, handle):
        '''
        Initialize with raw json twitter data from /data directory
        '''
        base_path = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(base_path,'data')
        tweet_file = '/{0}_tweets.json'.format(handle)
        filename = data_dir + tweet_file
        with open(filename) as json_file:
            self.data = json.load(json_file)
        self.tweets = [tweet['text'] for tweet in self.data]
        self.clean_tweets = []
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
        clean_words = ' '.join(words)
        return(clean_words)

    def construct_td_matrix(self):
        '''
        Construct a TD Matrix from inputted tweets data
        TODO: Implement term frequency - inverse document frequency
              (tf-idf) statistic
        '''
        vec = CountVectorizer()
        X = vec.fit_transform(self.clean_tweets)
        self.td_matrix = pd.DataFrame(X.toarray(), columns=vec.get_feature_names())
        return(self.td_matrix)

    def main(self):
        for i, tweet in enumerate(self.tweets):
            try:
                clean_tweet = self.preprocess(tweet)
                self.clean_tweets.append(clean_tweet)
            except IndexError:
                log.warn('ERROR: ' + tweet)
                continue
        self.construct_td_matrix()

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-t", "--twitter_handle",
        help="Twitter handle to pull tweets against.")
    args = parser.parse_args()
    Transform(args.twitter_handle).main()
