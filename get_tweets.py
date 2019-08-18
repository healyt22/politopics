import twitter
import os, yaml, json
from argparse import ArgumentParser
import logging as log
log.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p',
                level=log.INFO)

class GetTweets():
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

    def get_politicians(self, slug):
        '''
        This method will return a list of politicians
        returns list object
        '''
        crooks = self.api.GetListMembers(
                slug=slug,
                owner_screen_name='cspan')
        for crook in crooks:
            filepath = self.base_path + '/tweet_data/{0}'.format(crook.screen_name)
            if not os.path.exists(filepath):
                os.makedirs(filepath)
        return(crooks)

    def get_tweets(self, handle, n):
        '''
        Gets n tweets for inputted politician's handle
        TODO: figure out if date range should be implemented
        returns list object
        '''
        timeline = self.api.GetUserTimeline(screen_name=handle, count = n)
        for raw_tweet in timeline:
            tweet = raw_tweet.AsDict()
            msg = ' | '.join([tweet['id_str'], tweet['user']['name'], tweet['text']])
            log.info(msg)
            params = {
                'screen_name': tweet['user']['screen_name'],
                'id': tweet['id']
            }
            filename = self.base_path + '/tweet_data/{screen_name}/{id}.json'.format(**params)
            with open(filename, 'w') as outfile:
                json.dump(tweet, outfile, indent=4)

    def main(self, handle='', n=200):
        '''
        Executes the program
        TODO: Explore efficiency of using loop vs. generator object
        '''
        x = GetTweets()
        if handle is not None:
            x.get_tweets(handle, n)
        else:
            crooks = x.get_politicians('members-of-congress') #us-congress
            for crook in crooks:
                log.info('Pulling tweets for: ' + crook.name)
                x.get_tweets(crook.screen_name, n)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-t", "--twitter_handle",
        help="Twitter handle to pull tweets against.")
    args = parser.parse_args()
    GetTweets().main(args.twitter_handle)
