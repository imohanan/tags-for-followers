#!/usr/bin/python
import json, datetime, time, re
import ConfigParser
import urllib
from termcolor import colored

def saveUserInfo(data, fileName, originalUserId,userInfo, write):

    if data["id"] in userInfo.keys():
        #if userdata is already present skip it
        print(colored(str(data["id"]) + " user is already present in the file","red"))
        print("fileData>>>>>" + str(userInfo[data["id"]]))
        #print("newData<<<<<" + str(data))
    else:
        #add data in the dict
        userInfo[data["id"]] = data
        userInfo[data["id"]]["timestamp"] = int(time.time())
        userInfo[data["id"]]["originalUserId"] = originalUserId
        #write the new/modified data in the file (overwrite)
        #print("USER INFO>>>>>>>>>>>>>>>" +str(userInfo))
        if write:
            with open(fileName, 'w') as outputFile:
                json.dump(userInfo,outputFile)
            print(colored("WROTEEeeeeeeeeeeee","green"))


def getUserInfo(userId):
    config = ConfigParser.ConfigParser()
    config.read('defaults.cfg')
    url = "https://api.instagram.com/v1/users/"+ userId + "?access_token="+config.get('UserDetails','access_token')
    userInfo = json.loads(urllib.urlopen(url).read())

    if "meta" in userInfo.keys() and userInfo["meta"]["code"] == 200:
        return userInfo["data"]
    else:
        print(userInfo)

        return "error"


if __name__ == "__main__":

    config = ConfigParser.ConfigParser()
    config.read('defaults.cfg')
    inputFileName = "data/mappings/user_mapping/users_map2.json"
    with open(inputFileName) as user_map:
        userMap = json.load(user_map)
    userInfoFileName = "data/users/original_users/users2_"+ re.sub(r"\/",r"-", str(time.strftime("%x")))+".json"
    try:
        with open(userInfoFileName,"rb") as dataFile:
            userInfoMap = json.load(dataFile)
    except IOError:
        userInfoMap = dict()

    similarUserInfoFileName = "data/users/similar_users/users2_"+ re.sub(r"\/",r"-", str(time.strftime("%x")))+".json"

    try:
        with open(similarUserInfoFileName,"rb") as dataFile:
            similarUserInfoMap = json.load(dataFile)
    except IOError:
        similarUserInfoMap = dict()
    counter = 1
    count = 0
    for key, value in userMap.iteritems():
        count+=1
        if count % 100 == 0:
            print("HEREREREREREREREREREREREREREREREREREER")
            write = True
        else:
            write = False
        if key not in userInfoMap.keys():
            originalUserInfo = getUserInfo(key)
            if originalUserInfo == "error":
                print(colored("ERROR:::: UserInfo not available for user Id ::: " + str(key),"red"))
            else:
                saveUserInfo(originalUserInfo,userInfoFileName, None, userInfoMap,write)
                print "processed: " + str(counter)
                counter += 1
        else:
            print(colored("User already present","yellow"))
        if value not in similarUserInfoMap.keys() :
            similarUserInfo = getUserInfo(value)
            if similarUserInfo == "error":
                print(colored("ERROR:::: UserInfo not available for similar user Id ::: " + str(key),"red"))
            else:
                saveUserInfo(similarUserInfo,similarUserInfoFileName, key,similarUserInfoMap,write)
                print "processed: " + str(counter)
                counter += 1
        else:
            print(colored(" siimlar User already present","yellow"))