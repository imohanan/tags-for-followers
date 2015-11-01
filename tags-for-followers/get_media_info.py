import ConfigParser
import urllib2, urllib
import re
import time
import os, sys
import datetime
import json

config = None

def get_media(media_id, config, directory):
    next_url = 'https://api.instagram.com/v1/media/'+media_id+'?access_token='+config.get('UserDetails','access_token')
    url = next_url
    try:
        result = urllib2.urlopen(url).read()
    except urllib2.HTTPError:
        print "Cannot fetch" + media_id
        return 0

    file_name = directory + '/' + str(media_id) +".json"
    with open(file_name, 'w+') as op_file:
        op_file.write(result)
    time.sleep(0.1)
    return 1


if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.read('defaults.cfg')
    
    today = datetime.date.today()
    directory = 'data/media_info/'+str(today) + "/" +str(datetime.datetime.today())
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    already_collected_id_list = set()
    already_collected_file = open('data/media_info/'+str(today)+'/collected_list.txt', 'a+')
    for line in already_collected_file:
        already_collected_id_list.add(line.strip())

    media_mapping_file = open(sys.argv[1])
    data = json.loads(media_mapping_file.readline())
    user_type = sys.argv[2]
    if user_type == "follow":
        media_ids = data.keys()
    else:
        media_ids = data.values()

    for media_id in media_ids:
        if media_id not in already_collected_id_list:
            status = get_media(media_id, config, directory);
            if status == 1:
                already_collected_file.write(media_id + "\n")
                already_collected_id_list.add(media_id)
