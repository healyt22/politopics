DROP TABLE IF EXISTS constatuents.twitter_facts;

CREATE TABLE constatuents.twitter_facts(
    created_at TIMESTAMP,
    user_id BIGINT,
    tweet_id BIGINT,
    retweet_id BIGINT,
    quoted_tweet_id BIGINT,
    lang VARCHAR(2),
    source VARCHAR(500),
    full_text VARCHAR(280),
    retweet_count INT,
    favorite_count INT,
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY ( tweet_id, user_id )
)
;
