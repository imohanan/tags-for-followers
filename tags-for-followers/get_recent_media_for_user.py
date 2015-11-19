
import ConfigParser
import urllib2, urllib
import re, os, sys
import time, datetime
import json

NO_OF_DAYS = 20

def get_user_media(user_id, config, directory):
    count = 0
    today = datetime.datetime.today()
    next_url = 'https://api.instagram.com/v1/users/'+user_id+'/media/recent?access_token='+config.get('UserDetails','access_token')
    media_list = [];
    media_count = 0
    while( media_count < 20):
        count += 1
        url = next_url

        result = urllib.urlopen(url).read()
        json_data = json.loads(result)
        if json_data["meta"]["code"] == 429:
            print "Rate Limit exceeded"
            exit()
        if json_data["meta"]["code"] != 200:
            print "USER INFO NOT available"
            return
        done = False
        print(json_data)
        for data_item in json_data["data"]:
            created_date = datetime.datetime.fromtimestamp(int(data_item["created_time"]))
            media_list.append(data_item)
            media_count+=1
            if media_count > 20:
                break
        if media_count > 20:
            break
        else:
            if "next_url" in json_data["pagination"]:
                next_url = json_data["pagination"]["next_url"]
            else:
                break
        time.sleep(0.1)

    #print len(media_list)
    file_name = open(directory+"/"+user_id+'.json', 'w')
    json.dump(media_list, file_name)
    return 1

if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.read('defaults.cfg')

    today = datetime.date.today()
    directory = 'data/user_recent_media/'+str(today)
    if not os.path.exists(directory):
        os.makedirs(directory)

    already_collected_id_list = set()
    already_collected_file = open('data/user_recent_media/'+str(today)+'/collected_list.txt', 'a+')
    for line in already_collected_file:
        already_collected_id_list.add(line.strip())

    user_mapping_file = open('data/mappings/user_mapping/users_map1.json', 'r')
    data = json.loads(user_mapping_file.readline())
    user_ids = data.keys()
    user_ids.extend(data.values())
    for user_id in user_ids:
        if user_id not in already_collected_id_list:
            status = get_user_media(user_id, config, directory)
            print("collected::   " + user_id)
            if status == 1:
                already_collected_file.write(user_id + "\n")
                already_collected_id_list.add(user_id)

