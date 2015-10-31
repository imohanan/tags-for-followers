from instagram.client import InstagramAPI
import ConfigParser
import urllib2, urllib
import re
import time, datetime
import json

NO_OF_DAYS = 20

def get_user_media(user_id, configz):
    count = 0
    today = datetime.datetime.today()
    next_url = 'https://api.instagram.com/v1/users/'+user_id+'/media/recent?access_token='+config.get('UserDetails','access_token')
    media_list = [];
    while( count < 150):
        count += 1
        url = next_url

        result = urllib2.urlopen(url).read()
        json_data = json.loads(result)

        done = False
        for data_item in json_data["data"]:
            created_date = datetime.datetime.fromtimestamp(int(data_item["created_time"]))
            delta = today - created_date;
            if delta.days < NO_OF_DAYS:
                media_list.append(data_item)
            else:
                done = True
                break

        if done == True:
            break
        else:
            if "next_url" in json_data["pagination"]:
                next_url = json_data["pagination"]["next_url"]
            else:
                break
        time.sleep(1)

    print len(media_list)
    file_name = open('data/user_recent_media/'+user_id+"_"+str(today.month)+"."+str(today.day)+'.json', 'w')
    json.dump(media_list, file_name)
    return

if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.read('defaults.cfg')
    get_user_media('528817151', config);
