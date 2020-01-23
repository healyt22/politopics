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
        self.db = MySQLInterface()
        self.tweet_if = TweetInterface(tweet)

    def facts(self):
        tweets = tweet_if.parse_facts()
        for tweet in tweets:
            self.db.exec('insert_facts.sql', vars)

    def hashtags(self):
        with open('sql/insert_hashtags.sql', 'r') as f:
            sql = f.read()
        for hashtag in self.tweet['hashtags']:
            vars = (
                self.tweet['user']['id'],
                self.tweet['id'],
                hashtag['text']
            )
            self.db.execute(sql, vars)

    def urls(self):
        with open('sql/insert_urls.sql', 'r') as f:
            sql = f.read()
        for url in self.tweet['urls']:
            vars = (
                self.tweet['user']['id'],
                self.tweet['id'],
                url['expanded_url']
            )
            self.db.execute(sql, vars)

    def user_mentions(self):
        with open('sql/insert_user_mentions.sql', 'r') as f:
            sql = f.read()
        for url in self.tweet['user_mentions']:
            vars = (
                self.tweet['user']['id'],
                self.tweet['id'],
                url['id'],
                url['name'],
                url['screen_name']
            )
            self.db.execute(sql, vars)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-t", "--twitter_handle",
        help="Twitter handle to pull tweets against.")
    args = parser.parse_args()

    tweet_files = os.listdir(
        os.path.join(
            base_path,
            f'tweet_data/{args.twitter_handle}/'
        )
    )

    for tweet_file in tweet_files:
        log.info(tweet_file)
        fp = f'tweet_data/{args.twitter_handle}/{tweet_file}'
        TL = TweetLoader(fp)
        TL.facts()
