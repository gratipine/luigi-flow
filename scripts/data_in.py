# %%
import sys
sys.path.append("../")
import requests
import json
import tweepy as tw
import src.data_in as dt_in
import pandas as pd
from setup import token
# %%
tweet_fields = "tweet.fields=text,author_id,created_at"
since = "start_time=2022-06-26T19:16:12.000Z"
query="from: ECONdailycharts"
# %%
out = dt_in.search_twitter(query, tweet_fields, since, token)
# %%
out["data"]
# %%