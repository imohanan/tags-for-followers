#!/usr/bin/python
import json, datetime, time, re
import ConfigParser
import urllib
from termcolor import colored

def saveUserInfo(data, fileName, originalUserId):
    try:
        with open(fileName,"rb") as dataFile:
            userInfo = json.load(dataFile)
    except IOError:
        userInfo = dict()
    if data["id"] in userInfo.keys():
        #if userdata is already present skip it
        print(colored(data["id"] + " user is already present in the file","red"))
        print("fileData>>>>>" + str(userInfo[data["id"]]))
        print("newData<<<<<" + str(data))
    else:
        #add data in the dict
        userInfo[data["id"]] = data
        userInfo[data["id"]]["timestamp"] = datetime.datetime.now().isoformat()
        userInfo[data["id"]]["originalUserId"] = originalUserId
        #write the new/modified data in the file (overwrite)
        print("USER INFO>>>>>>>>>>>>>>>" +str(userInfo))
        with open(fileName, 'w') as outputFile:
            json.dump(userInfo,outputFile)


def getUserInfo(userId):
    config = ConfigParser.ConfigParser()
    config.read('defaults.cfg')
    url = "https://api.instagram.com/v1/users/"+ userId + "?access_token="+config.get('UserDetails','access_token')
    userInfo = json.loads(urllib.urlopen(url).read())

    if userInfo["meta"]["code"] == 200:
        return userInfo["data"]
    else:
        return "error"


if __name__ == "__main__":

    config = ConfigParser.ConfigParser()
    config.read('defaults.cfg')
    inputFileName = "data/mappings/user_mapping/users_map.json"
    with open(inputFileName) as user_map:
        userMap = json.load(user_map)
    userInfoFileName = "data/users/original_users/users_"+ re.sub(r"\/",r"-", str(time.strftime("%x")))+".json"
    similarUserInfoFileName = "data/users/similar_users/users_"+ re.sub(r"\/",r"-", str(time.strftime("%x")))+".json"
    for key, value in userMap.iteritems():
        originalUserInfo = getUserInfo(key)
        if originalUserInfo == "error":
            print("ERROR:::: UserInfo not available for user Id ::: " + key,"red")
        else:
            saveUserInfo(originalUserInfo,userInfoFileName, None)

        similarUserInfo = getUserInfo(value)
        if similarUserInfo == "error":
            print("ERROR:::: UserInfo not available for similar user Id ::: " + key,"red")
        else:
            saveUserInfo(similarUserInfo,similarUserInfoFileName, key)