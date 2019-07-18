import twitter
import yaml

class ParseTweets():
    def __init__(self):
        '''
        Initialize object with a Twitter API key file -> keys.yaml
        TODO: Initialize an object for every Politician?
        '''
        #base_path = os.path.dirname(os.path.realpath(__file__))
        #key_file = os.path.join(base_path,'keys.yaml')
        key_file = 'keys.yaml'
        with open(key_file, 'r') as (f):
            keys = yaml.load(f)
        self.api = twitter.Api(
                consumer_key=keys['consumer_key'],
                consumer_secret=keys['consumer_secret'],
                access_token_key=keys['access_token_key'],
                access_token_secret=keys['access_token_secret'])
        print(self.api.VerifyCredentials())
    
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
        timeline = self.api.GetUserTimeline(screen_name=handle, count=n)
        tweets = [tweet.AsDict() for tweet in timeline]
        return(tweets)
    
    def preprocess_(self, text):
        '''
        Some preprocessing will most likely need to be done to 
        remove stop words, stemming, perhaps even by using synonyms
        TODO: NLTK library
        '''
    
    def construct_td_matrix(self, tweets):
        '''
        Construct a TD Matrix from inputted tweets data
        TODO: Implement term frequency - inverse document frequency 
              (tf-idf) statistic
        '''
    
    def main(self):
        '''
        Executes the program
        TODO: Explore efficiency of using loop vs. generator object
        '''
        self.politicians = get_politicians()
        for politician in self.politicians:
            tweets = get_tweets(politician)
            tweets_td = construct_td_matrix(tweets)