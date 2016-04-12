import tweepy
from tweepy import OAuthHandler
from datetime import datetime as dt
from collections import OrderedDict

#Twitter OAuth
consumer_key = '#############'
consumer_secret = '##################'
access_token = '#######################'
access_secret = '#################'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

print "from which year: "
from_year = raw_input()
print "from which month: "
from_month = raw_input()
print "from which date"
from_date = raw_input()

print "to which year: "
to_year = raw_input()
print "to which month: "
to_month = raw_input()
print "to which date: "
to_date = raw_input()

start = dt.strptime((from_year + '-' + from_month + '-' + from_date), "%Y-%m-%d")
end = dt.strptime((to_year + '-' + to_month + '-' + to_date), "%Y-%m-%d")

tag_result = {}
mention_result = {}

#input file to read screen names line by line
file_name = "input.txt"
with open(file_name) as f:
    name_list = f.read().splitlines()

for username in name_list:
    tag_map = {}
    mention_map = {}
    for tweet in tweepy.Cursor(api.user_timeline, screen_name = username, lang="en").items():
        if((dt.strptime(str(tweet.created_at)[:10], "%Y-%m-%d") >= start) and (dt.strptime(str(tweet.created_at)[:10], "%Y-%m-%d") <= end)):
            for tag in tweet.entities['hashtags']:
                if tag['text'] in tag_map:
                    tag_map[tag['text']] += 1
                else:
                    tag_map[tag['text']] = 1
            for mention in tweet.entities['user_mentions']:
                if mention['screen_name'] in mention_map:
                    mention_map[mention['screen_name']] += 1
                else:
                    mention_map[mention['screen_name']] = 1
        elif (dt.strptime(str(tweet.created_at)[:10], "%Y-%m-%d") < start):
            break

    print "\nTrends (via #HashTag) in that period for " + username + " timeline"
    for key in  OrderedDict(sorted(tag_map.items(), key=lambda kv: kv[1], reverse=True)):
        if(tag_map[key] > 2):
            print '#' + key + ": " + str(tag_map[key])
        else:
            break
    print "\nMost popular person/company (via @Mention) in that period for " + username + " timeline"
    for key in  OrderedDict(sorted(mention_map.items(), key=lambda kv: kv[1], reverse=True)):
        if(mention_map[key] > 2):
            print '@' + key + ": " + str(mention_map[key])
        else:
            break

    # for cross key matching for #hashtag
    if(len(tag_result) == 0):
        for each_key in tag_map.keys():
            tag_result[each_key] = 1
    else:
        for cross_key in set(tag_map).intersection(tag_result):
            if cross_key in tag_result:
                tag_result[cross_key] += 1
            else:
                tag_result[cross_key] = 1

    # for cross key matching for @mention
    if (len(mention_result) == 0):
        for each_key in tag_map.keys():
            mention_result[each_key] = 1
    else:
        for cross_key in set(tag_map).intersection(mention_result):
            if cross_key in tag_result:
                mention_result[cross_key] += 1
            else:
                mention_result[cross_key] = 1

    tag_map.clear()
    mention_map.clear()


print "\n\nTRENDS (via #HashTag) in that period for this group:"
for key in OrderedDict(sorted(tag_result.items(), key=lambda kv: kv[1], reverse=True)):
    if (tag_result[key] > 2):
        print '#' + key + ": " + str(tag_result[key])
    else:
        break

print "\n\nMost popular person/company (via @Mention) in that period for this group:"
for key in OrderedDict(sorted(mention_result.items(), key=lambda kv: kv[1], reverse=True)):
    if (mention_result[key] > 2):
        print '@' + key + ": " + str(mention_result[key])
    else:
        break