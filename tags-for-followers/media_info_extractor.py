import sys, json, csv, os, datetime

# TODO: Location, caption, avgTagPopularity, created_time
columns = ["mediaCount", "tagCount", "commentsCount", "likesCount", "usersInPhotoCount", "userhasLiked"]

initial_date = datetime.datetime(2015, 11, 9)

def get_headers():
    return columns

def create_csv_data(user_id):
    directory = 'data/user_recent_media/2015-11-22/'
    data = None
    if user_id+".json" in os.listdir(directory):
        file_obj = open(directory+user_id+".json", 'r')
        json_data = json.loads(file_obj.readline())
        if len(json_data)!=0:
            media_count = 0
            tag_count = 0
            comments_count = 0
            likes_count = 0
            users_in_photo_count = 0
            user_has_liked_count = 0
            for media in json_data:
                delta = initial_date - datetime.datetime.fromtimestamp(int(media["created_time"]))
                if delta.days>=0 and delta.days < 10:
                    media_count += 1
                    tag_count += len(media["tags"])
                    comments_count += media["comments"]["count"]
                    likes_count += media["likes"]["count"]
                    users_in_photo_count += len(media["users_in_photo"])
                    user_has_liked_count += media["user_has_liked"]
            if media_count != 0:
                data = [float(media_count), float(tag_count)/media_count, float(comments_count)/media_count, float(likes_count)/media_count, float(users_in_photo_count)/media_count, float(user_has_liked_count)/media_count]
            else:
                data = [0, 0, 0, 0, 0, 0] 
    return data

if __name__ == "__main__":
    user_mapping_file = open('data/mappings/user_mapping/users_map.json', 'r')
    data = json.loads(user_mapping_file.readline())
    user_ids = data.keys()
    data_list = []
    for user_id in user_ids:
        data_list.append(create_csv_data(user_id))

    with open('trial.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(columns)
        for data in data_list:
            writer.writerow(data)

