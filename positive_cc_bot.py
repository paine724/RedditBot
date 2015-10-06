#!/usr/bin/python
import praw
import pdb
import re
import os
import random
from config_bot import *

# Check that the file that contains our username exists
if not os.path.isfile("config_bot.py"):
    print "You must create a config file with your username and password."
    print "Please see config_skel.py"
    exit(1)

# Create the Reddit instance
user_agent = ("Positive CC Bot 1.0")
reddit = praw.Reddit(user_agent=user_agent)

positive_statements = ["You are a majestic unicorn. This is just the begining of what you can believe if you put your mind to it. I believe in you and we all do!", "You are special and you deserve to have a drake song written about you.", 
"Think about all the wonderful things you've felt since embarking on this adventure. You deserve that and more.", "Congratulations! You've made Ryan Gosling Proud"]
statement_index = random.randint(0,len(positive_statements)-1)

# and login
reddit.login(REDDIT_USERNAME, REDDIT_PASS)

# Have we run this code before? If not, create an empty list
if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []

# If we have run the code before, load the list of posts we have replied to
else:
    # Read the file into a list and remove any empty values
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = filter(None, posts_replied_to)

# Get the top 5 values from our subreddit
subreddit = reddit.get_subreddit('xxketo')
for submission in subreddit.get_hot(limit=5):
    # print submission.title

    # If we haven't replied to this post before
    if submission.id not in posts_replied_to:

        # Do a case insensitive search
        if (re.search("sv", submission.title, re.IGNORECASE)) or (re.search("nsv", submission.title, re.IGNORECASE)):
            # Reply to the post
            submission.add_comment("Positive encouragement bot here: " + positive_statements[statement_index])
            print "Bot replying to : ", submission.title

            # Store the current id into our list
            posts_replied_to.append(submission.id)

# Write our updated list back to the file
with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")