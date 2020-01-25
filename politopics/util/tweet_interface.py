import os, time, json
import logging as log

log.basicConfig(
    format='util.tweet_cleaner | %(asctime)s | %(levelname)s | %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=log.INFO
)
base_path = os.path.dirname(os.path.realpath(__file__))

class TweetInterface():
    def __init__(self, tweet_dict):
        self.tweet_dict = tweet_dict
        self.retweet_id = self.tweet_dict.get('retweeted_status', {}).get('id')
        self.quoted_tweet_id = self.tweet_dict.get('quoted_status', {}).get('id')

        self.parse_data()

    def string_to_date(self, created_at):
        dt = time.strftime('%Y-%m-%d %H:%M:%S',
            time.strptime(
                created_at,
                '%a %b %d %H:%M:%S +0000 %Y'
            )
        )
        return(dt)

    def fact_vars(self):
        try:
            tweet_text = self.tweet_dict['full_text']
        except:
            tweet_text = self.tweet_dict['text']

        self.facts = (
            self.string_to_date(self.tweet_dict['created_at']),
            self.tweet_dict['user']['id'],
            self.tweet_dict['id'],
            self.retweet_id ,
            self.quoted_tweet_id,
            self.tweet_dict['lang'],
            self.tweet_dict['source'],
            tweet_text,
            self.tweet_dict.get('retweet_count', None),
            self.tweet_dict.get('favorite_count', None)
        )

    def hashtag_vars(self):
        self.hashtags = []
        for hashtag in self.tweet_dict['hashtags']:
            self.hashtags.append((
                self.tweet_dict['user']['id'],
                self.tweet_dict['id'],
                hashtag['text']
            ))

    def url_vars(self):
        self.urls = []
        for url in self.tweet_dict['urls']:
            self.urls.append((
                self.tweet_dict['user']['id'],
                self.tweet_dict['id'],
                url['expanded_url']
            ))

    def user_mention_vars(self):
        self.user_mentions = []
        for user_mention in self.tweet_dict['user_mentions']:
            self.user_mentions.append((
                self.tweet_dict['user']['id'],
                self.tweet_dict['id'],
                user_mention['name'],
                user_mention['screen_name']
            ))

    def parse_data(self):
        self.fact_vars()
        self.hashtag_vars()
        self.url_vars()
        self.user_mention_vars()

    def print_data(self):
        print('-------------------------- FACTS ------------------------------')
        print(self.facts)
        print('-------------------------- HASHTAGS ---------------------------')
        print(self.hashtags)
        print('-------------------------- URLS -------------------------------')
        print(self.urls)
        print('-------------------------- USER MENTIONS ----------------------')
        print(self.user_mentions)
        print('\n')

if __name__ == '__main__':
    twt_fp = os.path.join(base_path, '../tweet_data/aguilarpete/482267226238484481.json')
    with open(twt_fp, 'r') as f:
        tweet_dict = json.load(f)
    ti = TweetInterface(tweet_dict)
    ti.print_data()

    twt_fp = os.path.join(base_path, '../tweet_data/LindseyGrahamSC/1205508523486011397.json')
    with open(twt_fp, 'r') as f:
        tweet_dict = json.load(f)
    ti = TweetInterface(tweet_dict)
    ti.print_data()
