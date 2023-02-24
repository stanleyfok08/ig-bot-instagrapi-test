# ig-bot-instagrapi-test

1. Login (credentials must be typed)
2. Fetch recent post of hashtag
3. Like the fetched posts
	like a post if all condition satisfied
    1. is photo (media type = 1)
    2. within a week (today - post date <= 7)
    3. is not liked before (database have no record of this post)
    4. user not in banned list (is not post by selected users)
    5. not exceed max like count (prevent bot not work)
4. Logoff (otherwise will cause client error)
