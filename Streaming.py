from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import MySQLdb
import time
import json


conn = MySQLdb.connect("mysql.server", "beginneraccount", "cookies", "beginneraccount$tutorial")

c = conn.cursor()

# consumer key, consumer secret, access token, access secret.
ckey = "********"
csecret = "*********"
atoken = "***********"
asecret = "**********"


class listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)

        tweet = all_data["text"]

        username = all_data["user"]["screen_name"]

        c.execute("INSERT INTO taula (time, username, tweet) VALUES (%s,%s,%s)",
                  (time.time(), username, tweet))

        conn.commit()

        print((username, tweet))

        return True

    def on_error(self, status):
        print
        status


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["car"])