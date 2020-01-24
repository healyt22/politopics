DROP TABLE IF EXISTS constatuents.twitter_hashtags;

CREATE TABLE constatuents.twitter_hashtags(
    user_id BIGINT,
    tweet_id BIGINT,
    hashtag VARCHAR(100),
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY ( user_id, tweet_id )
)
;
