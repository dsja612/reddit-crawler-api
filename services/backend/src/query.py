"""
This script executes API calls and constructs data for the front-end.
"""

import time
from decouple import config
import asyncpraw
from . import api
from . import preprocess
from decouple import config
from fastapi import HTTPException

async def main(username: str) -> dict: 

    reddit = asyncpraw.Reddit(client_id = config('CLIENT_ID'),
                     client_secret = config('CLIENT_SECRET'),
                     user_agent = config('USER_AGENT'))

    payload = {}
    
    try:
        ### ASYNCPRAW
        start = time.time()
        print("Starting PRAW query for /u/{}".format(username))
        user = await reddit.redditor(username)
        comments = user.comments.new(limit=int(config('COMMENTS_LIMIT')))

        # Get body of comments
        comment_list = []
        top_subreddits = {}
        async for comment in comments:
            comment_list.append(comment.body)
            key = comment.subreddit.display_name
            top_subreddits[key] = top_subreddits[key] + 1 if key in top_subreddits else 1

        end = time.time()
        print("PRAW query finished in {} seconds".format(end - start))

        await reddit.close()
        # Get top subreddits commented on
        top_subreddits = {k: v for k, v in sorted(top_subreddits.items(), key=lambda x: x[1], reverse=True)}
        payload['top_subreddits'] = top_subreddits

        ### Other API
        # Get top words sorted in ascending order
        payload['top_words'] = await preprocess.preprocess_comments(comment_list)
        # Get general information
        payload['basic_data'] = await api.getBasicData(username)

        # Get no. of comments
        payload['num_comments'] = await api.getNumSubmissions(username, 'comment')

        # Get no. of submissions
        payload['num_submissions'] = await api.getNumSubmissions(username, 'submission')

        return payload

    except Exception as err:
        raise err
