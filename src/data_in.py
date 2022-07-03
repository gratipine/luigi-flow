import requests

def search_twitter(
        query: str, tweet_fields: str, since: str, 
        bearer_token: str):
    """Get tweets from Twitter.
    Only works for tweets from the past week, so since must be a week ago at most

    Taken from 
    https://towardsdatascience.com/searching-for-tweets-with-python-f659144b225f
    Slightly modified

    query: in the format of "from: user_name"
    tweet_fields: in the format of "tweet.fields=text,author_id,created_at"
    since: "start_time=2022-06-26T19:16:12.000Z"
    bearer_token: need to create a Twitter dev account for that. 

    Can read more about the fields here:
    https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-recent#tab1
    and in here
    https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query

    """
    headers = {"Authorization": "Bearer {}".format(bearer_token)}

    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}&{}".format(
        query, tweet_fields, since
    )
    print(url)
    response = requests.request("GET", url, headers=headers)

    print(response.status_code)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


