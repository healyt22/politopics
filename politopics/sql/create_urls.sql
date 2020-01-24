DROP TABLE IF EXISTS constatuents.twitter_urls;

CREATE TABLE constatuents.twitter_urls(
    user_id BIGINT,
    tweet_id BIGINT,
    url VARCHAR(1000),
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY ( user_id, tweet_id )
);
