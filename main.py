from random import randint
import praw
import re
import config

CITATIONS = [
    "That's it, end of the story", 
    "Bless you", 
    "Wendy's triple bacon...", 
    "Crincio",
    "UIC - University of Indians and Chineses",
    "Thanks for playing with us... but no",
    "Join our coult... Join NECSTLab",
    "Can we do better?",
    "Shut",
    "We're going to do science",
    "Have a nice weekend even though it's wednedsay",
    "Awesome"
]

TRIGGERS = [
    "santambrogio",
    "santa",
    "jenna"
]

def get_citation():
    return CITATIONS[randint(0, len(CITATIONS) - 1)]

def santa_egg(sentence) -> bool:
    return re.search("s.*a.*n.*t.*a", sentence)


def handle_post(post):
    for trigger in TRIGGERS:
        if trigger in post.title.lower():
            post.reply(f"{get_citation()}")


def handle_comment(comment):
    body = comment.body.lower()

    for trigger in TRIGGERS:
        if trigger in body:
            comment.reply(f"{get_citation()}")
            return 

    nominated = santa_egg(body)

    if nominated: 
        comment.reply(f"Non lo sapevi ma mi hai nominato `{nominated.group()}`, eccoti una citazione `{get_citation()}`")


def main():
    reddit = praw.Reddit(
        client_id=config.client_id,
        client_secret=config.client_secret,
        user_agent=config.user_agent,
        password=config.password,
        username=config.username,
    )

    print("Listening for comments and posts on POLIMIxUIC")

    subreddit = reddit.subreddit("POLIMIxUIC")

    posts = subreddit.stream.submissions(pause_after=-1, skip_existing=True)
    cmts = subreddit.stream.comments(pause_after=-1, skip_existing=True)

    while True:
        for post in posts:
            if post is None:
                break
            
            handle_post(post)

        for cmt in cmts:
            if cmt is None:
                break
            
            if cmt.author.name != "santa_bot_1":
                handle_comment(cmt)


if __name__ == "__main__":
    main()

# obtain the token 
# curl -X POST -d 'grant_type=password&username=santa_bot_1&password=Rizjob-qampaz-1bynbo' --user 'hjx9zv-_IgH9PJuUiDFcIg:KWjjGe9sMgg_UOPP_UPKxUMxzP3PEg' https://www.reddit.com/api/v1/access_token
