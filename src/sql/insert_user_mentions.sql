REPLACE INTO constatuents.twitter_facts
(
      created_at
    , user_id
    , tweet_id
    , retweet_id
    , lang
    , source
    , full_text
    , retweet_count
    , favorite_count
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
;
