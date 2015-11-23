import sys, json, os, datetime

initial_date = datetime.datetime(2015, 11, 8)

def find_hashtags(user_id, hashtag_set):
    directory = 'data/user_recent_media/2015-11-22/'
    data = []
    if user_id+".json" in os.listdir(directory):
        file_obj = open(directory+user_id+".json", 'r')
        data = json.loads(file_obj.readline())
        if len(data)!=0:
            for media in data:
                delta = initial_date - datetime.datetime.fromtimestamp(int(media["created_time"]))
                if delta.days>=0 and delta.days < 10:
                    for tag in media["tags"]:
                        hashtag_set.add(tag)
    

if __name__ == "__main__":
    user_mapping_file = open('data/mappings/user_mapping/users_map.json', 'r')
    data = json.loads(user_mapping_file.readline())
    user_ids = data.keys()
    hashtag_set = set()
    for user_id in user_ids:
        find_hashtags(user_id, hashtag_set)

    hashtag_list = list(hashtag_set)
    json.dump(hashtag_list, open('data/all_hashtags.json', 'w'))
