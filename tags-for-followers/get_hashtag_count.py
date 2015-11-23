import ConfigParser
import sys, json, os
import urllib2, urllib

def get_hashtag_media_count(hashtag):
    url = 'https://api.instagram.com/v1/tags/'+hashtag+'?access_token='+config.get('UserDetails','access_token')
    result = urllib.urlopen(url.encode('utf-8')).read()
    data = json.loads(result)
    #print media_info
    if data["meta"]["code"] == 429:
        print "Rate Limit exceeded"
        return None
    return data["data"]["media_count"]

if __name__ == "__main__":
    config = ConfigParser.ConfigParser()
    config.read('defaults.cfg')

    all_hashtags_file = open('data/all_hashtags.json', 'r')
    hashtags = json.loads(all_hashtags_file.readline())
    hashtag_count = {}
    if 'hashtag_count_map.json' in os.listdir('data'):
        count_map_file = open('data/hashtag_count_map.json', 'r')
        hashtag_count = json.loads(count_map_file)
    counter = 1
    for tag in hashtags:
        if tag not in hashtag_count:
            print "Processed: " + str(counter)
            counter += 1
            val = get_hashtag_media_count(tag)
            if val == None:
                json.dump(hashtag_count, open('data/hashtag_count_map.json', 'w'))
            else:
                hashtag_count[tag] = val
