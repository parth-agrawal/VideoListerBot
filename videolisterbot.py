# A Reddit bot that collects YouTube links from comments and compiles them into a YouTube playlist.


import praw
import re
import os

reddit = praw.Reddit('bot1')

subreddit = reddit.subreddit("testingground4bots")


if not os.path.isfile("comment_IDs.txt"):
    comment_IDs = []
else:
    with open("comment_IDs.txt", "r") as f:
        comment_IDs = f.read()
        comment_IDs = comment_IDs.split(",")
        comment_IDs = list(filter(None, comment_IDs))

if not os.path.isfile("video_links.txt"):
    video_links = []
else:
    with open("video_links.txt", "r") as f:
        video_links = f.read()
        video_links = video_links.split(",")
        video_links = list(filter(None, video_links))

# Need to add funcitonality if there are multiple links in the same comment

for submission in subreddit.hot(limit=5):
    submission.comments.replace_more(limit=None)
    for comment in submission.comments:
        if comment.id not in comment_IDs:
            
            body = comment.body

            body_links = []
            while True:
                try:
                
                    # trims string at first link. Maybe should allow for you.tube links or m.youtube?
                    link_start = body.index("(https://www.youtube.com")
                    cut1 = body[link_start:]
                    # index of the next space after the link begins
                    endlink_ind = cut1.index(")")

                    # link string
                    link = cut1[1:endlink_ind] 
                    # creates new chunk after the first link to check for multiple links
                    new_body = cut1[endlink_ind + 1:]
                    
                    # if links not in links list, append
                    if link not in video_links:
                        body_links.append(link)
                        print(body)

                    # if new body is blank, exit loop

                    if new_body == "" or new_body == " ":
                        break
                    else:
                        body = new_body
                except ValueError as error:
                    break
            comment_IDs.append(comment.id)

            # adds all of the links in the body
            video_links = video_links + body_links

with open("comment_IDs.txt", "w") as f:
    for id in comment_IDs:
        f.write(id + ",")
with open ("video_links.txt", "w") as f:
    for link in video_links:
        f.write(link + ",")

             
        
