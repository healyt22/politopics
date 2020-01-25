import os, time, json, yaml
from argparse import ArgumentParser
import logging as log

from util.mysql_interface import MySQLInterface
from util.tweet_interface import TweetInterface

log.basicConfig(
    format  = '%(asctime)s | %(levelname)s | %(message)s',
    datefmt = '%m/%d/%Y %I:%M:%S %p',
    level   = log.INFO
)
base_path = os.path.dirname(os.path.realpath(__file__))

class Politopics():
    def __init__(self, filepath):
        self.filepath = filepath
        with open(self.filepath) as f:
            self.tweet = json.load(f)
        self.retweet = self.tweet.get('retweeted_status', None)
        self.quoted_tweet = self.tweet.get('quoted_status', None)

        self.build_tweet_list()

    def build_tweet_list(self):
        self.tweets = [ self.tweet ]
        if self.retweet:
            self.tweets.append(self.retweet)
        if self.quoted_tweet:
            self.tweets.append(self.quoted_tweet)
        self.parsed_tweets = [ TweetInterface(tweet) for tweet in self.tweets ]

    def load_db(self):
        db = MySQLInterface()
        for parsed_tweet in self.parsed_tweets:
            db.execute('insert_facts.sql', parsed_tweet.facts)
            [ db.execute('insert_hashtags.sql', hashtag_tup)
                    for hashtag_tup in parsed_tweet.hashtags ]
            [ db.execute('insert_urls.sql', url_tup)
                    for url_tup in parsed_tweet.urls ]
            [ db.execute('insert_user_mentions.sql', user_mention_tup)
                    for user_mention_tup in parsed_tweet.user_mentions ]

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-t", "--twitter_handle",
        help="Twitter handle to pull tweets against.")
    args = parser.parse_args()

    if args.twitter_handle:
        dir = os.path.join(base_path, f'tweet_data/{args.twitter_handle}/')
        tweet_files = os.listdir(dir)
        for tweet_file in tweet_files:
            log.info(tweet_file)
            fp = f'{dir}{tweet_file}'
            Politopics(fp).load_db()

    dir = os.path.join(base_path, f'tweet_data/')
    handles = os.listdir(dir)
    n = len(handles)
    for i, handle in enumerate(handles):
        log.info(f'Processing tweets for {handle} ({i+1} of {n})')
        tweet_files = os.listdir(f'{dir}{handle}')
        for tweet_file in tweet_files:
            fp = f'{dir}{handle}/{tweet_file}'
            Politopics(fp).load_db()
