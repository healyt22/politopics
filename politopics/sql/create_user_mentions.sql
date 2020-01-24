DROP TABLE IF EXISTS constatuents.twitter_user_mentions;

CREATE TABLE constatuents.twitter_user_mentions(
    user_id BIGINT,
    tweet_id BIGINT,
    name VARCHAR(100),
    screen_name VARCHAR(100),
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY ( user_id, tweet_id )
);
