import tweepy, time, logging
from bening_setup import create_env
from bening_watercolor import create_picture

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger()

def send_picture(api, since_id):
    logger.info("Checking mentions...")
    pictures_sent = 0
    new_since_id = since_id
    media = [1]
    media[0] = "pictures\\watercolor.png"

    for tweet in tweepy.Cursor(api.mentions_timeline, since_id = since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is None:
            # tweet is not a reply to somebody, so we should send a picture
            try:
                logger.info(f"Attempting to send a picture...")
                create_picture()
                api.update_status_with_media(
                    status = f"@{tweet.user.screen_name}",
                    filename = media[0]
                )
                logger.info("Picture sent!")
                pictures_sent += 1
            except:
                logger.info("Error sending picture.")
    
    with open("data\\bening_data.csv") as bening_data:
        data = bening_data.readlines()
    data[0] = str(new_since_id) + '\n'
    with open("data\\bening_data.csv", "w") as bening_data:
        bening_data.writelines(data)

    logger.info(f"Done sending pictures for now, {pictures_sent} picture(s) sent!")
    return new_since_id

def main():
    api, since_id = create_env()

    while True:
        since_id = send_picture(api, since_id)
        time.sleep(60)

if __name__ == "__main__":
    main()
