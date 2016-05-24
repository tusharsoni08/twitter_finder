import tweepy
import plotly.plotly as py
from tweepy import OAuthHandler
from datetime import datetime as dt
from collections import OrderedDict

#OAuth
# Get the following keys and sccret from https://apps.twitter.com using your twitter account
consumer_key = '####################'
consumer_secret = '#####################'
access_token = '###############'
access_secret = '##################'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

#Plot.ly API Graph
#HASHTAG
hash_graph_data = {
"data": [{
    "x": [],
    "y": [],
    "type": "bar"
}],
"layout": {
    "xaxis": {"title": "topics"},
    "yaxis": {"title": "frequencies"},
    "title": "Trends with #hashtag"
}
}
hash_data = hash_graph_data.get("data")

X_val_hash = hash_data[0]['x']
Y_val_hash = hash_data[0]['y']

#MENTION
mention_graph_data = {
"data": [{
    "x": [],
    "y": [],
    "type": "bar"
}],
"layout": {
    "xaxis": {"title": "topics"},
    "yaxis": {"title": "frequencies"},
    "title": "popularity with @mention"
}
}
mention_data = mention_graph_data.get("data")

X_val_men = mention_data[0]['x']
Y_val_men = mention_data[0]['y']


#print "from which year: "
from_year = "2016"#raw_input()
#print "from which month: "
from_month = "04"#raw_input()
#print "from which date"
from_date = "20"#raw_input()

#print "to which year: "
to_year = "2016"#raw_input()
#print "to which month: "
to_month = "05"#raw_input()
#print "to which date"
to_date = "15"#raw_input()

start = dt.strptime((from_year + '-' + from_month + '-' + from_date), "%Y-%m-%d")
end = dt.strptime((to_year + '-' + to_month + '-' + to_date), "%Y-%m-%d")

tweets = 0
total_tweets = 0

cross_group_tag = {}
cross_group_mention = {}

# Loop over all input files
for i in xrange(4):

    #one group intersection map with it's all profiles
    tag_result = {}
    mention_result = {}

    file_name = "input" + str(i) + ".txt"
    with open(file_name) as f:
        name_list = f.read().splitlines()

    for username in name_list:
        tag_map = {}
        mention_map = {}
        for tweet in tweepy.Cursor(api.user_timeline, screen_name = username, lang="en").items():
            if((dt.strptime(str(tweet.created_at)[:10], "%Y-%m-%d") >= start) and (dt.strptime(str(tweet.created_at)[:10], "%Y-%m-%d") <= end)):
                tweets += 1
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

#        print "\nTrends (via #HashTag) in that period for " + username + " timeline"
#        for key in  OrderedDict(sorted(tag_map.items(), key=lambda kv: kv[1], reverse=True)):
#            if(tag_map[key] > 1):
#                print '#' + key + ": " + str(tag_map[key])
                #X_val_hash.append(key)
                #Y_val_hash.append(tag_map[key])
#            else:
#                break
#        print "\nMost popular person/company (via @Mention) in that period for " + username + " timeline"
#        for key in  OrderedDict(sorted(mention_map.items(), key=lambda kv: kv[1], reverse=True)):
#            if(mention_map[key] > 1):
#                print '@' + key + ": " + str(mention_map[key])
                #X_val_men.append(key)
                #Y_val_men.append(mention_map[key])
#            else:
#                break

        #Intra-group cross key matching for #hashtag within group
        if(len(tag_result) == 0):
            for each_key in tag_map.keys():
                tag_result[each_key] = 1
        else:
            for cross_key in set(tag_map).intersection(tag_result):
                if cross_key in tag_result:
                    tag_result[cross_key] += 1
                else:
                    tag_result[cross_key] = 1

        #Intra-group cross key matching for @mention within group
        if (len(mention_result) == 0):
            for each_key in mention_map.keys():
                mention_result[each_key] = 1
        else:
            for cross_key in set(mention_map).intersection(mention_result):
                if cross_key in mention_result:
                    mention_result[cross_key] += 1
                else:
                    mention_result[cross_key] = 1

    #    py.plot(hash_graph_data, filename='#' + username, sharing='public')
    #    del X_val_hash[:]
    #    del Y_val_hash[:]

    #    py.plot(mention_graph_data, filename='@' + username, sharing='public')
    #    del X_val_men[:]
    #    del Y_val_men[:]

        tag_map.clear()
        mention_map.clear()

    del name_list[:]


    print "\nNumber of tweets in group " + file_name + ": " + str(tweets)
    total_tweets += tweets
    tweets = 0

    print "\n\nTRENDS (via #HashTag) in that period for this group: " + file_name
    for key in OrderedDict(sorted(tag_result.items(), key=lambda kv: kv[1], reverse=True)):
        if (tag_result[key] > 1):
            print '#' + key + ": " + str(tag_result[key])
            X_val_hash.append(key)
            Y_val_hash.append(tag_result[key])
        else:
            break

    print "\n\nMost popular person/company (via @Mention) in that period for this group: " + file_name
    for key in OrderedDict(sorted(mention_result.items(), key=lambda kv: kv[1], reverse=True)):
        if (mention_result[key] > 1):
            print '@' + key + ": " + str(mention_result[key])
            X_val_men.append(key)
            Y_val_men.append(mention_result[key])
        else:
            break

    py.plot(hash_graph_data, filename='#group: ' + file_name, sharing='public')
    del X_val_hash[:]
    del Y_val_hash[:]

    py.plot(mention_graph_data, filename='@group: ' + file_name, sharing='public')
    del X_val_men[:]
    del Y_val_men[:]

    #Inter-group cross key matching of #hashtag
    if (len(cross_group_tag) == 0):
        for each_key in tag_result.keys():
            cross_group_tag[each_key] = 1
    else:
        for cross_key in set(tag_result).intersection(cross_group_tag):
            if cross_key in cross_group_tag:
                cross_group_tag[cross_key] += 1
            else:
                cross_group_tag[cross_key] = 1

    #Inter-group cross key matching of @mention
    if (len(cross_group_mention) == 0):
        for each_key in mention_result.keys():
            cross_group_mention[each_key] = 1
    else:
        for cross_key in set(mention_result).intersection(cross_group_mention):
            if cross_key in cross_group_mention:
                cross_group_mention[cross_key] += 1
            else:
                cross_group_mention[cross_key] = 1


    tag_result.clear()
    mention_result.clear()


print "\nTotal number of tweets in all groups: " + str(total_tweets)

print "\n\nOVERALL TRENDS (via #HashTag) in that period"
for key in OrderedDict(sorted(cross_group_tag.items(), key=lambda kv: kv[1], reverse=True)):
    if (cross_group_tag[key] > 1):
        print '#' + key + ": " + str(cross_group_tag[key])
        X_val_hash.append(key)
        Y_val_hash.append(cross_group_tag[key])
    else:
        break

print "\n\nOVERALL Most popular person/company (via @Mention) in that period"
for key in OrderedDict(sorted(cross_group_mention.items(), key=lambda kv: kv[1], reverse=True)):
    if (cross_group_mention[key] > 1):
        print '@' + key + ": " + str(cross_group_mention[key])
        X_val_men.append(key)
        Y_val_men.append(cross_group_mention[key])
    else:
        break

py.plot(hash_graph_data, filename='#Overall_cross-group', sharing='public')
del X_val_hash[:]
del Y_val_hash[:]

py.plot(mention_graph_data, filename='@Overall_cross-group', sharing='public')
del X_val_men[:]
del Y_val_men[:]

cross_group_tag.clear()
cross_group_mention.clear()
