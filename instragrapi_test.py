# %%
# instagrapi 1.16.30
from instagrapi import Client
from instagrapi import MediaMixin
from datetime import date, timedelta
import csv, time, pandas as pd
import schedule, time

"""
task procedure:
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
"""

# change the schedule time, hashtag and post fetching and liking limit
SET_TIME = "15:09"              # set a time to start the schedule
USER_HASHTAG = "trainspotting"  # set to any other hashtag
USER_MAX_SEARCH = 20            # recommend max 20, otherwise the api throws cilent error
USER_MAX_LIKE_NUMBER = 20       # should not be larger than USER_MAX_LIKE_NUMBER


def task(entered_hashtag,entered_max_number,entered_like_number):

    cl = Client()
    insta_username = # Fill in your username
    insta_password = # Fill in your password

    cl.login(insta_username, insta_password)
	
    print("Task step 1: Login complete")

    # some returned results of the hashtag    
    medias = cl.hashtag_medias_top(entered_hashtag, amount=entered_max_number)
	
    print("Task step 2: Fetch post complete. Fetched",len(medias),"posts")
    
    with open("liked_list.csv", "r") as liked, open("banned_list.csv", "r") as banned:
        liked_df = pd.DataFrame(pd.read_csv(liked))
        banned_df = pd.DataFrame(pd.read_csv(banned))

        liked_list = liked_df['list of liked post'].to_list()
        banned_list = banned_df['banned user'].to_list()
    
    like_count = 0


    print("Task step 3: Ready to like posts")
	
    for post in medias:
        # convert to python dict
        current_post = post.dict()
        url = "https://www.instagram.com/p/" + current_post['code'] + "/"

        # conditions to like a post
        if ((int(current_post['media_type']) == 1) and                                      #rule 1
            (date.today() - post.dict()['taken_at'].date() <= timedelta(days = 7)) and      #rule 2
            (int(current_post['pk']) not in liked_list) and                                 #rule 3
            (int(current_post['user']['pk']) not in banned_list) and                        #rule 4
            like_count < entered_like_number):                                              #rule 5       

            # like current post
            is_liked = MediaMixin.media_like(self=cl,media_id=current_post['pk'])           # like the current post using the post id
            
            if is_liked:                
                print("\tLiked post",url)
                
            # save the id to the database for this post
            with open("liked_list.csv", "a", newline='') as liked:
                writer = csv.writer(liked)
                writer.writerow([current_post['pk'],url]) 

            like_count += 1                                        
        else:                                                                               #if don't match any rules, skip the post
            print("\tSkipped post",url)                                                  

    print("Task step 3: Like posts complete. Liked",like_count,"posts")

    cl.logout()
    print("Task step 4: Logout complete")

schedule.every().day.at(SET_TIME).do(task, USER_HASHTAG, USER_MAX_SEARCH, USER_MAX_LIKE_NUMBER)

print("Schedule is set to", SET_TIME, "to search", USER_MAX_SEARCH, "posts of #" + USER_HASHTAG + ". Aiming to like", USER_MAX_LIKE_NUMBER, "posts.")

# autorun
while (True):
    schedule.run_pending()
    time.sleep(3)
