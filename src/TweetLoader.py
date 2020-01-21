import os, time, json, yaml
import mysql.connector
from argparse import ArgumentParser
import logging as log

log.basicConfig(
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=log.INFO
)
base_path = os.path.dirname(os.path.realpath(__file__))

class TweetLoader():
    def __init__(self, filepath):
        self.filepath = filepath
        with open(self.filepath) as f:
            self.tweet = json.load(f)
        self.connect()

    def connect(self):
        config_file = os.path.join(base_path,'config.yaml')
        with open(config_file, 'r') as f:
            db_config = yaml.load(f, Loader=yaml.FullLoader)['mysql_creds']

        self.db = mysql.connector.connect(
            host = db_config['host'],
            user = db_config['user'],
            passwd = db_config['password'],
            database = db_config['database'],
            charset="utf8",
            use_unicode=True
        )

    def sql_exec(self, sql_file, vars):
        with open(f'sql/{sql_file}', 'r') as f:
            sql = f.read()
        cursor = self.db.cursor()
        cursor.execute(sql, vars)
        self.db.commit()

    def parse_tweet(self, tweet, retweet_id=None, quoted_tweet_id=None):
        created_at = time.strftime('%Y-%m-%d %H:%M:%S',
            time.strptime(
                tweet['created_at'],
                '%a %b %d %H:%M:%S +0000 %Y'
            )
        )

        retweet = tweet.get('retweeted_status', None)
        quoted_tweet = tweet.get('quoted_status', None)

        if retweet:
            tweet['favorite_count'] = None

        tweet_text = tweet.get('text', tweet['full_text'].encode())

        vars = (
            created_at,
            tweet['user']['id'],
            tweet['id'],
            retweet_id,
            quoted_tweet_id,
            tweet['lang'],
            tweet['source'],
            tweet_text,
            tweet['retweet_count'],
            tweet['favorite_count']
        )
        return(vars)

    def facts(self):
        if self.tweet.get('retweeted_status', None):
            log.info("loading tweet")
            tweet_vars = self.parse_tweet(
                self.tweet,
                retweet_id = self.tweet['retweeted_status']['id']
            )
            self.sql_exec('insert_facts.sql', tweet_vars)

            log.info("loading retweet")
            retweet_vars = self.parse_tweet(
                self.tweet['retweeted_status'],
            )
            self.sql_exec('insert_facts.sql', retweet_vars)

        elif self.tweet.get('quoted_status', None):
            log.info("loading tweet")
            tweet_vars = self.parse_tweet(
                self.tweet,
                quoted_tweet_id = self.tweet['quoted_status']['id']
            )
            self.sql_exec('insert_facts.sql', tweet_vars)

            log.info("loading quoted tweet")
            quoted_tweet_vars = self.parse_tweet(
                self.tweet['quoted_status'],
            )
            self.sql_exec('insert_facts.sql', quoted_tweet_vars)

        else:
            log.info("loading tweet")
            tweet_vars = self.parse_tweet(self.tweet)
            self.sql_exec('insert_facts.sql', tweet_vars)


    def hashtags(self):
        with open('sql/insert_hashtags.sql', 'r') as f:
            sql = f.read()
        for hashtag in self.tweet['hashtags']:
            vars = (
                self.tweet['user']['id'],
                self.tweet['id'],
                hashtag['text']
            )
            self.sql_exec(sql, vars)

    def urls(self):
        with open('sql/insert_urls.sql', 'r') as f:
            sql = f.read()
        for url in self.tweet['urls']:
            vars = (
                self.tweet['user']['id'],
                self.tweet['id'],
                url['expanded_url']
            )
            self.sql_exec(sql, vars)

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
            self.sql_exec(sql, vars)

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
