# %%
import sys
sys.path.append("../")
import requests
import json
import tweepy as tw
import src.data_in as dt_in
import pandas as pd
import src.data_prep as prep
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
out_df, flat = prep.transform_data(out) 
# %%
from importlib import reload
reload(prep)
# %%
flat_series = pd.Series(flat)
# %%
filler_words = [
    "the", "to", "of", "have", "in", "a", "is", 
    "and", "for", "as"]

flat_series = flat_series.str.replace("“", "")
flat_series = flat_series.str.replace("”", "")
flat_series = flat_series.str.replace(",", "")
flat_series = flat_series.str.replace("’s", "")

flat_series = flat_series[
    ~(flat_series.isin(filler_words))]

flat_series = flat_series[
    ~(flat_series.str.contains("http"))]

# %%
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
# %%
# Generate the word cloud from frequencies
wc = WordCloud().generate_from_text(" ".join(flat_series.values.astype(str)))

plt.imshow(wc)
plt.axis('off')
plt.show()
