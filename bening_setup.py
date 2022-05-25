import tweepy, os, logging

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger()

def create_env():
    api_key = "API_KEY"
    api_key_secret = "API_KEY_SECRET"
    access_token = "ACCESS_TOKEN"
    access_token_secret = "ACCESS_TOKEN_SECRET"

    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    since_id = 1
    data = []

    try:
        with open("data\\bening_data.csv") as bening_data:
            data = bening_data.readlines()
    except:
        logger.error("Error reading data!")

    for index, cell in enumerate(data):
        if index == 0:
            since_id = int(cell.strip())

    return api, since_id