import time
import traceback
import config
import praw

#Login process for the bot
def bot_login():
    r = praw.Reddit(username = config.username, 
                    password = config.password, 
                    client_id = config.client_id,
                    client_secret = config.client_secret,
                    user_agent = config.user_agent)
    
    return r

r = bot_login()
#Opens a text file, and scans the specified subreddit for new submission. It checks if it has already
#commented on a submission, and if it hasn't it will comment. When the comment is voted below the specified
#threshold, the bot will remove the submission. This bot must be a moderator on the subreddit for this work.
while True:
    try:
        print "Beginning loop!"
        for submission in r.subreddit(config.subreddit).new(limit=20):
            if submission not in r.user.me().saved(limit=None):
                submission.reply(config.reply)
                print "Commented on a submission!"
                submission.save()
                print "Submission saved!"

        for comment in r.user.me().comments.new(limit=None):
            if comment.score < config.score:
                comment.submission.mod.remove(spam=False)
                print "Submission removed!"

        print "End of loop... sleep 30s"
        time.sleep(30)
    except:
        #Simply printing a trace and resuming the bot after 10 seconds
        traceback.print_exc()
        print "Resuming in 10 seconds..."
        time.sleep(10)
