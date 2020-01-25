REPLACE INTO constatuents.twitter_users
(
	  created_at
	, description
	, favourites_count
	, followers_count
	, friends_count
	, geo_enabled
	, user_id
	, listed_count
	, location
	, name
	, profile_background_image_url
	, profile_image_url_https
	, screen_name
	, statuses_count
	, url
	, verified
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
;
