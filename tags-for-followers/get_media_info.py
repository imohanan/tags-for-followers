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
    result = urllib.urlopen(url).read()
    media_info = json.loads(result)
    if media_info["meta"]["code"] == 429:
        print "Rate Limit exceeded"
        exit()
    file_name = directory + '/' + str(media_id) +".json"
    with open(file_name, 'w+') as op_file:
        op_file.write(result)
    time.sleep(0.1)
    return


if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.read('defaults.cfg')
    
    today = datetime.date.today()
    directory = 'data/media_info/'+str(today) + "/" + str(datetime.datetime.today().hour)
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    already_collected_id_list = set()
    already_collected_file = open(directory+'/collected_list.txt', 'a+')
    for line in already_collected_file:
        already_collected_id_list.add(line.strip())

    media_mapping_file = open('data/mappings/media_mapping/media_map1.json', 'r')
    data = json.loads(media_mapping_file.readline())
    media_ids = data.keys()
    media_ids.extend(data.values())
    counter = 1
    for media_id in media_ids:
        if media_id not in already_collected_id_list:
            get_media(media_id, config, directory);
            already_collected_file.write(media_id + "\n")
            already_collected_id_list.add(media_id)
            print "Processed: " + str(counter)
            counter = counter + 1

