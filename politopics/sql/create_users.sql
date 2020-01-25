DROP TABLE IF EXISTS constatuents.twitter_users;

CREATE TABLE constatuents.twitter_users(
    created_at TIMESTAMP,
    description VARCHAR(500),
    favourites_count INT,
    followers_count INT,
    friends_count INT,
    geo_enabled BOOLEAN,
    user_id BIGINT,
    listed_count INT,
    location VARCHAR(100),
    name VARCHAR(100),
    profile_background_image_url VARCHAR(500),
    profile_image_url_https VARCHAR(500),
    screen_name VARCHAR(100),
    statuses_count INT,
    url VARCHAR(500),
    verified BOOLEAN,
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY ( user_id )
);
