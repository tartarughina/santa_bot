from random import randint, random
import praw
import re
import config
import bisect

class Config:
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
        "Awesome",
        "Super awesome"
    ]

    TRIGGERS = [
        "santambrogio",
        "santa",
        "jenna",
        "uic",
        "chicago",
        "letterman",
        "ds160",
        "uslenghi",
        "piergiorgio",
        "visa",
    ]

    NAMES = [
        {"name": "Andrea", "probability": 3},
        {"name": "Pietro", "probability": 1},
        {"name": "Riccardo", "probability": 1},
        {"name": "Simone", "probability": 1},
        {"name": "Marco", "probability": 1},
        {"name": "Alessandro", "probability": 1},
        {"name": "Filippo", "probability": 2},
        {"name": "Claudio", "probability": 1},
        {"name": "Gabriele", "probability": 1},
        {"name": "Calliope", "probability": 1},
        {"name": "Matteo", "probability": 1}
    ]

    TOT_PROBABILITY = 0
    DISTRIBUTION = []

def get_citation():
    return Config.CITATIONS[randint(0, len(Config.CITATIONS) - 1)]

def santa_egg(sentence) -> bool:
    return re.search("s.*a.*n.*t.*a", sentence)

def cdf():
    cumsum = 0
    for w in Config.NAMES:
        cumsum += w.get("probability")
        Config.DISTRIBUTION.append(cumsum / Config.TOT_PROBABILITY)

def get_rand_name():    
    return Config.NAMES[bisect.bisect(Config.DISTRIBUTION, random())].get("name")

def prep_reply():
    return f"{get_citation()} mh... {get_rand_name()}"


def handle_post(post):
    for trigger in Config.TRIGGERS:
        if trigger in post.title.lower():
            post.reply(prep_reply())


def handle_comment(comment):
    body = comment.body.lower()

    for trigger in Config.TRIGGERS:
        if trigger in body:
            comment.reply(prep_reply())
            return 

    nominated = santa_egg(body)

    if nominated: 
        comment.reply(f"Non lo sapevi ma mi hai nominato `{nominated.group()}`, eccoti una citazione `{get_citation()}`")


def main():
    # update the total probability at startup
    for x in Config.NAMES:
        Config.TOT_PROBABILITY += x.get("probability")

    # set the distribution of the available names
    cdf()

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