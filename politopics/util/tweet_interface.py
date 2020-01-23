import time
import logging as log

log.basicConfig(
    format='util.tweet_cleaner | %(asctime)s | %(levelname)s | %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=log.INFO
)

class TweetInterface():
    def __init__(self, raw_tweet):
        self.tweet = tweet
        self.retweet = self.tweet.get('retweeted_status', None)
        self.quoted_tweet = self.tweet.get('quoted_status', None)

        if self.retweet:
            self.tweet['favorite_count'] = None

    def string_to_date(self, created_at):
        dt = time.strftime('%Y-%m-%d %H:%M:%S',
            time.strptime(
                created_at,
                '%a %b %d %H:%M:%S +0000 %Y'
            )
        )
        return(dt)

    def fact_vars(self, tweet_dict, retweet_id=None, quoted_tweet_id=None):
        vars = (
            self.string_to_date(tweet_dict['created_at']),
            tweet_dict['user']['id'],
            tweet_dict['id'],
            retweet_id,
            quoted_tweet_id,
            tweet_dict['lang'],
            tweet_dict['source'],
            tweet_dict['full_text']
            tweet_dict['retweet_count'],
            tweet_dict['favorite_count']
        )
        return(vars)

    def parse_facts(self):
        tweets = [ self.parse(self.tweet) ]
        if self.retweet:
            retweet_facts = self.fact_vars(
                self.retweet,
                retweet_id = self.retweet['id']
            )
            tweets.append(retweet_facts)
        if self.quoted_tweet:
            quoted_tweet_facts = self.fact_vars(
                self.quoted_tweet,
                quoted_tweet_id = self.quoted_tweet['id']
            )
            tweets.append(quoted_tweet_facts)
        return(tweets)
