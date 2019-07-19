import twitter
import os, yaml, json
from argparse import ArgumentParser
import logging as log
log.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p',
                level=log.DEBUG)

class ParseTweets():
    def __init__(self):
        '''
        Initialize object with a Twitter API key file -> keys.yaml
        TODO: Initialize an object for every Politician?
        '''
        self.base_path = os.path.dirname(os.path.realpath(__file__))
        key_file = os.path.join(self.base_path,'keys.yaml')
        with open(key_file, 'r') as (f):
            keys = yaml.load(f)
        self.api = twitter.Api(
                consumer_key=keys['consumer_key'],
                consumer_secret=keys['consumer_secret'],
                access_token_key=keys['access_token_key'],
                access_token_secret=keys['access_token_secret'])

    def get_politicians(self):
        '''
        This method will return a list of politicians
        returns list object
        '''
        members = self.api.GetListMembers(
                slug='members-of-congress',
                owner_screen_name='cspan')
        return(members)

    def get_tweets(self, handle, n):
        '''
        Gets n tweets for inputted politician's handle
        TODO: figure out if date range should be implemented
        returns list object
        '''
        timeline = self.api.GetUserTimeline(screen_name=handle, count = 1000)
        tweets = [tweet.AsDict() for tweet in timeline]
        filename = self.base_path + '/data/{0}_tweets.json'.format(handle)
        with open(filename, 'w') as outfile:
            json.dump(tweets, outfile, indent=4)
        return(tweets)

    def main(self, handle=''):
        '''
        Executes the program
        TODO: Explore efficiency of using loop vs. generator object
        '''
        x = ParseTweets()
        if handle is not None:
            x.get_tweets(handle, 50)
        else:
            crooks = x.get_politicians()
            for crook in crooks:
                x.get_tweets(crook.screen_name, 50)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-t", "--twitter_handle",
        help="Twitter handle to pull tweets against.")
    args = parser.parse_args()
    ParseTweets().main(args.twitter_handle)
