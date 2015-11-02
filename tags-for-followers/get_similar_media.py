#!/usr/bin/python
import sys, json, pprint, os, datetime, time, re
import ConfigParser
import urllib2, urllib
from termcolor import colored

def hasSimilarFollowerCount(similarUserInfo, orgininalMediaFollowerCount):
    config = ConfigParser.ConfigParser()
    config.read('defaults.cfg')
    percentDiff = float(config.get("SimilarFollowerCount", "percent_difference"))*orgininalMediaFollowerCount/100
    similarUserFollowerCount = getFollowerCount(similarUserInfo)
    return (similarUserFollowerCount >= (orgininalMediaFollowerCount-percentDiff)) and (similarUserFollowerCount <= orgininalMediaFollowerCount+percentDiff) 

def getRecentMediaForTag(hashtag,orgininalMediaFollowerCount, userInfoFileName, similarMediaFileName, originalMediaId, originalUserId):

    config = ConfigParser.ConfigParser()
    config.read('defaults.cfg')
    count = 0

    next_url = 'https://api.instagram.com/v1/tags/'+hashtag+'/media/recent?access_token='+config.get('UserDetails','access_token')
    print(colored("Recent media URL::::::::::"+ next_url,"blue"))
    # found = False
    similarMedia = None
    dataForMapping = list()
    noOfCalls =0
    while(True):
        url = next_url
        resultStr =urllib2.urlopen(url).read()
        result = json.loads(resultStr)
        #first 20 recent media having that tag
        data = result["data"]
        for eachMedia in data:
            # print("$$$$$$$$$$$$$$$$$similar tag media%%%%%%%%%%%%%%%%%%" + str(eachMedia["tags"]))
            mediaTags = eachMedia["tags"]
            if int(time.time()) - int(eachMedia["created_time"]) > 3600:
                raise Exception("Data too old!!!")
            if not hasFollowTags(mediaTags,getFilterList(config.get('FilterFile','file_name'))):
                similarUserInfo = getUserInfo(eachMedia)
                print(colored("%%%%%%%%%%%%%%%%%%found similar tag media%%%%%%%%%%%%%%%%%%","yellow"))
                if hasSimilarFollowerCount(similarUserInfo, orgininalMediaFollowerCount):
                    print(colored("**********************************found a similar media*****************************",'green'))
                    similarMedia = eachMedia
                    #save similar Media
                    dataForMapping.append(similarMedia)
                    saveSimilarMedia(similarMedia,similarMediaFileName,hashtag,originalMediaId)
                    #save the similar media and its userDetails
                    saveUserInfo(similarUserInfo,userInfoFileName, hashtag,originalUserId)
                    dataForMapping.append(similarUserInfo)
                    break
                
        if similarMedia == None:
            noOfCalls+=1
            resultStr = urllib2.unquote(resultStr).decode('unicode_escape')
            resultStr = resultStr.replace('\/','/')
            reg_exp = r'"next_url":"(.*)"},"meta":'
            url_result = re.search(reg_exp, resultStr)
            if url_result == None or noOfCalls > 50:
                raise Exception("No more pagination!!!")
            next_url =  url_result.group(1)
            print(next_url)
        else:
            return dataForMapping

    #print result


def saveSimilarMedia(similarMedia, fileName, hashtag, originalMediaId):
    similarMedia["hashtag"] = hashtag
    similarMedia["originalMediaId"] = originalMediaId
    similarMedia["timestamp"] = int(time.time())
    with open(fileName, 'a') as outputFile:
        json.dump(similarMedia,outputFile)
        outputFile.write("\n")

def hasFollowTags(tagsList, filterList):
    fixed_list = ["like", "follo", "spam", "shoutout", "comment", "recent"]
    for tag in tagsList:
        if tag in filterList or any(s in tag for s in fixed_list):
            return True
    return False

def filterTags(tagsList, filterList):
    fixed_list = ["like", "follo", "spam", "shoutout", "comment", "recent"]
    filteredTags = set()
    for tag in tagsList:
        if not any(s in tag for s in fixed_list):
            if tag not in filterList:
                filteredTags.add(tag)
    return filteredTags

def getFilterList(filterFileName):
    filterListFile = open(filterFileName, "r")
    filterList = list()
    for line in filterListFile:
        filterList.append(line.strip())
    return filterList

def readJsonFile(inputDirName, inputFileName):
    inputFile = os.path.join(inputDirName,inputFileName)
    with open(inputFile) as data_file:    
        data = json.load(data_file)
    return data["data"]

def getUserInfo(media):
    config = ConfigParser.ConfigParser()
    config.read('defaults.cfg')
    userId = media["user"]["id"]
    url = "https://api.instagram.com/v1/users/"+ userId + "?access_token="+config.get('UserDetails','access_token')
    userInfo = json.loads(urllib.urlopen(url).read())
    print(str(userInfo))
    if userInfo and userInfo["meta"]["code"] == 200:
        return userInfo["data"]
    else:
        return "error"

    # print(userInfo)
    # return userInfo["data"] if userInfo["data"] else "error"
    # return userInfo["data"]["counts"]["followed_by"]

def getFollowerCount(userInfo):
    return userInfo["counts"]["followed_by"]

def saveUserInfo(data, fileName, tag, originalUserId):
    try:
        with open(fileName,"rb") as dataFile:    
            userInfo = json.load(dataFile)
    except IOError:
        userInfo = dict()
    if data["id"] in userInfo.keys():
        #if userdata is already present add the hashtag in the list
        print(str(data["id"]) + " user is already present in the file")
        print("fileData>>>>>" + str(userInfo[data["id"]]))
        print("newData<<<<<" + str(data))
    else:
        #add data in the dict
        data["hashtags"] = list()
        userInfo[data["id"]] = data

    userInfo[data["id"]]["hashtags"].append(tag)
    userInfo[data["id"]]["timestamp"] = int(time.time())
    userInfo[data["id"]]["originalUserId"] = originalUserId

    #write the new/modified data in the file (overwrite)
    print("USER INFO>>>>>>>>>>>>>>>" +str(userInfo))
    with open(fileName, 'w') as outputFile:
        json.dump(userInfo,outputFile)


if __name__ == "__main__":

    config = ConfigParser.ConfigParser()
    config.read('defaults.cfg')
    baseDataPath = "data/recent_media/"
    inputDirName = baseDataPath + sys.argv[1]
    filterListFileName = config.get('FilterFile','file_name')#sys.argv[2]
    userInfoFileName = "data/users/original_users/users_"+ re.sub(r"\/",r"-", str(time.strftime("%x")))+".json"
    similarUserInfoFileName = "data/users/similar_users/users_"+ re.sub(r"\/",r"-", str(time.strftime("%x")))+".json"

    similarMediaFileName = "data/similar_media/similar_media_"+ re.sub(r"\/",r"-", str(time.strftime("%x")))+ "_"+ str(time.strftime("%X"))+".json"

    print(userInfoFileName)
    usersMapFileName = "data/mappings/user_mapping/users_map"+".json"
    mediaMapFileName = "data/mappings/media_mapping/media_map"+".json"
    try:
        with open(mediaMapFileName,"rb") as dataFile:
            mediaMap = json.load(dataFile)
    except IOError:
        mediaMap = dict()

    try:
        with open(usersMapFileName,"rb") as dataFile:
            userMap = json.load(dataFile)
    except IOError:
        userMap = dict()

    mediaCount =0
    validMediaCount = len(mediaMap.keys())
    for fileName in os.listdir(inputDirName):
        if fileName[-5:] == ".json":
            print(colored("PROCESSING FILE:::::::::::::::::::::::::::::::::::::::::::::::::" + fileName,"cyan"))
            data = readJsonFile(inputDirName, fileName)
            for eachMedia in data:
                mediaCount +=1
                count =0
                originalMediaId = eachMedia["id"]
                print(colored("????????????STARTED processing media " + str(mediaCount) + "  Media iD: " + str(originalMediaId),'magenta'))
                mediaTags = eachMedia["tags"]

                if originalMediaId in mediaMap.keys():
                    print(colored("Media already present...." + str(originalMediaId), "red"))
                    continue
                # print(mediaTags)
                coocurringTags = filterTags(mediaTags, getFilterList(filterListFileName))
                coocurringTagsList = list(coocurringTags)
                found=False
                while found == False:
                    if len(coocurringTagsList) <= count:
                        break
                    similarHashTag = coocurringTagsList[count]
                    userInfo = getUserInfo(eachMedia)
                    if userInfo == "error":
                        print(colored("User info not available","red"))
                        break
                    originalUserId = userInfo["id"]
                    if originalUserId in userMap.keys():
                        print(colored("User already present..."+str(originalUserId),"red"))
                        break
                    orgininalMediaFollowerCount = getFollowerCount(userInfo)
                    try:
                        dataForMapping = getRecentMediaForTag(similarHashTag, orgininalMediaFollowerCount,similarUserInfoFileName, similarMediaFileName, originalMediaId, originalUserId)
                        found = True
                        validMediaCount+=1
                    except Exception, msg:
                        print(colored(str(msg) + ":: " + similarHashTag,"red"))
                        count +=1
                        continue

                if found == False:
                    continue
                saveUserInfo(userInfo,userInfoFileName, sys.argv[1], None)
                mediaMap[eachMedia["id"]] =dataForMapping[0]["id"]
                userMap[userInfo["id"]] = dataForMapping[1]["id"]

                with open(usersMapFileName, 'wb') as outputFile:
                    json.dump(userMap,outputFile)
                with open(mediaMapFileName, 'wb') as outputFile:
                    json.dump(mediaMap,outputFile)
                print(colored("??????????????ENDED processing media  " + str(mediaCount) + "  Media ID: " + str(originalMediaId) + "  User Id: " + str(originalUserId),'magenta'))
                print(colored("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ValidMediaID Processed---->" + str(validMediaCount),"magenta"))
            if validMediaCount > 2000:
                break
        if validMediaCount > 2000:
            break
            # print(data)
            # break




#python get_similar_media.py follow4follow