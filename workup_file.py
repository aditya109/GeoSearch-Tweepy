# Tweepy module written by Josh Roselin, documentation at https://github.com/tweepy/tweepy
# MySQLdb module written by Andy Dustman, documentation at http://mysql-python.sourceforge.net/MySQLdb.html
# GeoSearch crawler written by Chris Cantey, MS GIS/Cartography, University of Wisconsin, https://geo-odyssey.com
# MwSQLdb schema written with great assistance from Steve Hemmy, UW-Madison DoIT

import json
import os
import time
import csv
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import mysql.connector
import random

consumer_key="insert your key"
consumer_secret="insert your secret"

access_token="insert your token"
access_token_secret="insert your secret"
# Create your MySQL schema and connect to database, ex: mysql> SET PASSWORD FOR 'root'@'localhost' = PASSWORD('newpwd');
db = mysql.connector.connect(
    host='localhost', user='root', passwd='newpwd', db='twitter')
# db.set_character_set('utf8')
cursor = db.cursor()

coords = dict()
XY = []

#per request, write output to csv, rather than mysql. Be aware of limited rows to csv. The streaming API will return millions of rows per day.
csvfile = open('geopy_results.csv', 'w', newline='')
csvwriter = csv.writer(csvfile)
csvwriter.writerow(['UserID', 'Date', 'Lat', 'Long', 'Text'])


class NoDirectCoordinatesError(Exception):
    pass


class StdOutListener(StreamListener):
    def on_data(self, status):
        #  using json loader
        all_data = json.loads(status)

        # getting text
        text = all_data["text"]
        # print("text => ", text)

        # getting id of user
        user_id_str = all_data["user"]["id_str"]
        # print("user_id => ", user_id_str)

        # getting date
        __date = all_data["created_at"]
        # __date = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(__date,'%a %b %d %H:%M:%S +0000 %Y'))
        # print("date => ", __date)

        try:
            # coordinates
            coord = all_data["coordinates"]

            if coord is None:
                raise NoDirectCoordinatesError
            else:
                coord = coord["coordinates"]
                XY = coord
                # print("X => ", XY[0])
                # print("Y => ", XY[1])

        except NoDirectCoordinatesError:
            Box = all_data["place"]["bounding_box"]["coordinates"][0]
            XY = [(Box[0][0] + Box[2][0])/2, (Box[0][1] + Box[2][1])/2]
            print("X => ", XY[0])
            print("Y => ", XY[1])

        # DB write
        cursor.execute("""INSERT INTO twitterfeed2 (UserID, Date, Lat, Lng, Text) VALUES
                                    (%s, %s, %s, %s, %s);""",())

        db.commit()

        # CSV write
        """ Use this line for storing the strings in 'utf-8' encoding
        """
        csvwriter.writerow([user_id_str.encode("utf-8"), __date.encode("utf-8"), XY[1], XY[0], text.encode("utf-8")])
        """ Use this line for storing the strings in non - 'utf-8' encoding
        """
        # csvwriter.writerow([user_id_str, __date, XY[0], XY[1], text])
        return True

    def on_error(self, status):
        print(status)


def main():
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, StdOutListener(), timeout=30.0, is_async=True)

    # Only records 'locations' OR 'tracks', NOT 'tracks (keywords) with locations'
    while True:
        try:
            stream.filter(locations=[-125, 25, -65, 48])
            break
        except Exception:
            nsecs = random.randint(60, 63)
            time.sleep(nsecs)

if __name__ == '__main__':
    # clearing screen
    if os.name == "nt":
        _ = os.system('cls')

    main()
    input("\n\n\nPress enter to exit 🚀...")

    # clearing screen
    if os.name == "nt":
        _ = os.system('cls')
