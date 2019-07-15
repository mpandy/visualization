from twitter import *

#-----------------------------------------------------------------------
# load our API credentials
#-----------------------------------------------------------------------
import sys
sys.path.append(".")

#-----------------------------------------------------------------------
# create twitter API object
#-----------------------------------------------------------------------
twitter = Twitter(auth = OAuth('1141354030192635904-8427nh8lXfuHNJb4ui1uwDk2gpijMK',
                  'kJ8R1m02DTN7J79Gu9ap8QQcncoyFlmBwwtGJBqflohro',
                  'M9fPJX1VbS6UDfQaUhl3wTO7H',
                  'YbY0T9Jb8QnaJj1tEl5TfO7stwxACHDomjvKWFzdlJOhBPrutC'))

#-----------------------------------------------------------------------
# retrieve global trends.
# other localised trends can be specified by looking up WOE IDs:
#   http://developer.yahoo.com/geo/geoplanet/
# twitter API docs: https://dev.twitter.com/rest/reference/get/trends/place
#-----------------------------------------------------------------------
results = twitter.trends.place(_id = 23424975)

print("UK Trends")

for location in results:
    for trend in location["trends"]:
        print(" - %s " % trend)
        # print(" - %s : %s" % (trend["name"], trend["tweet_volume"]))