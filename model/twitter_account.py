
import tweepy


class TwitterAccount:

    def __init__(self, record):

        # recordの順序が、以下順序である前提
        # アカウントID	API_KEY	API_SECRET_KEY	ACCESS_TOKEN	ACCESS_SECRET_TOKEN
        self.id = record[0]
        auth = tweepy.OAuthHandler(record[1], record[2])
        auth.set_access_token(record[3], record[4])
        self.tweetApi = tweepy.API(auth)

    def __str__(self):
        return self.id

    def tweet(self,text) -> bool:

        self.tweetApi.update_status(text)
        return True
