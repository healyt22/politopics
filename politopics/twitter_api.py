import twitter
import os, yaml, json, time
from argparse import ArgumentParser
import logging as log
log.basicConfig(format='%(asctime)s | twitter_api | %(levelname)s | %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p',
                level=log.INFO)

class TwitterAPI():
    def __init__(self):
        self.base_path = os.path.dirname(os.path.realpath(__file__))
        self.data_dir = '/media/montebello/tweet_data'

        self.config_fp = os.path.join(self.base_path,'conf/config.yaml')
        with open(self.config_fp, 'r') as (f):
            self.config = yaml.load(f, Loader=yaml.FullLoader)
        keys = self.config['twitter_api']

        self.api = twitter.Api(
            consumer_key        = keys['consumer_key'],
            consumer_secret     = keys['consumer_secret'],
            access_token_key    = keys['access_token_key'],
            access_token_secret = keys['access_token_secret'],
            tweet_mode          = 'extended'
        )

    def string_to_date(self, created_at):
        dt = time.strftime('%Y-%m-%d',
            time.strptime(
                created_at,
                '%a %b %d %H:%M:%S +0000 %Y'
            )
        )
        return(dt)

    def get_tweets(self):
        timeline = self.api.GetListTimeline(
            list_id = 34179516, #CSPAN Members of Congress https://twitter.com/i/lists/34179516?lang=en
            #since_id = self.config['latest_tweet_id'],
            count = 200
        )

        for raw_tweet in timeline:
            tweet = raw_tweet.AsDict()

            handle = tweet['user']['screen_name']
            tweet_id = tweet['id']
            tweet_txt = tweet['full_text']
            tweet_dt = self.string_to_date(tweet['created_at'])
            tweet_ts = tweet['created_at']

            tweet_dir = os.path.join(self.data_dir, handle, tweet_dt)
            if not os.path.exists(tweet_dir):
                os.makedirs(tweet_dir)
            filename = os.path.join(tweet_dir, str(tweet_id) + '.json')

            log.info(f'Processing | {handle} | {tweet_ts} | {tweet_id} | {tweet_txt}')
            with open(filename, 'w') as outfile:
                json.dump(tweet, outfile, indent=4)

        self.config['latest_tweet_id'] = tweet_id
        with open(self.config_fp, 'w') as outfile:
            yaml.dump(self.config, outfile, indent=4)

if __name__ == '__main__':
    TwitterAPI().get_tweets()
