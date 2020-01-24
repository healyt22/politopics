REPLACE INTO constatuents.twitter_user_mentions
(
    user_id,
    tweet_id,
    name,
    screen_name
)
VALUES (%s, %s, %s, %s)
;
