import praw
import config
import traceback
import time

#Login process for the bot
def bot_login():
    r = praw.Reddit(username = config.username,
            password = config.password,
            client_id = config.client_id,
            client_secret = config.client_secret,
            user_agent = config.user_agent)
    
    return r

r = bot_login()
#Creating a variable to hold the bot's username
user = r.redditor(config.username)
hasCommented = False

#Opens a text file, and scans the specified subreddit for new submission. It checks if it has already
#commented on a submission, and if it hasn't it will comment. When the comment is voted below the specified
#threshold, the bot will remove the submission. This bot must be a moderator on the subreddit for this work.
while True:
    try:
        commented = open("commented.txt", "r+")

        for submission in r.subreddit(config.subreddit).new(limit=20):
            submissionID = submission.id
            for line in commented:
                if submissionID in line:
                    print ("Submission already commented on!")
                    hasCommented = True
            if hasCommented == False:
                submission.reply(config.reply)
                print ("Commented on a submission!")
                commented.write("\n" + submissionID)

        for comment in user.comments.new(limit=None):
            if comment.score < config.score:
                submission.mod.remove(spam=False)
                print ("Submission removed!")

        time.sleep(30)
    except:
        #Simply printing a trace and resuming the bot after 10 seconds
        traceback.print_exc()
        print("Resuming in 10 seconds...")
        time.sleep(10)        
    
