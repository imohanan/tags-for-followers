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
    dataForMapping = list()
    config = ConfigParser.ConfigParser()
    config.read('defaults.cfg')
    count = 0
    next_url = 'https://api.instagram.com/v1/tags/'+hashtag+'/media/recent?access_token='+config.get('UserDetails','access_token')

    # found = False
    similarMedia = None
    dataForMapping = list()
    while(True):
        url = next_url
        resultStr =urllib2.urlopen(url).read()
        result = json.loads(resultStr)
        #first 20 recent media having that tag
        data = result["data"]
        for eachMedia in data:
            # print("$$$$$$$$$$$$$$$$$similar tag media%%%%%%%%%%%%%%%%%%" + str(eachMedia["tags"]))
            mediaTags = eachMedia["tags"]
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
            resultStr = urllib2.unquote(resultStr).decode('unicode_escape')
            resultStr = resultStr.replace('\/','/')
            reg_exp = r'"next_url":"(.*)"},"meta":'
            url_result = re.search(reg_exp, resultStr)
            next_url =  url_result.group(1) 
            print(next_url)
            time.sleep(1)
        else:
            return dataForMapping

    #print result


def saveSimilarMedia(similarMedia, fileName, hashtag, originalMediaId):
    similarMedia["hashtag"] = hashtag
    similarMedia["originalMediaId"] = originalMediaId
    similarMedia["timestamp"] = datetime.datetime.now().isoformat()
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
    if userInfo["meta"]["code"] == 200:
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
        print(data["id"] + " user is already present in the file")
        print("fileData>>>>>" + userInfo[data["id"]])
        print("newData<<<<<" + data)
    else:
        #add data in the dict
        data["hashtags"] = list()
        userInfo[data["id"]] = data

    userInfo[data["id"]]["hashtags"].append(tag)
    userInfo[data["id"]]["timestamp"] = datetime.datetime.now().isoformat()
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
    userInfoFileName = "data/users/users_"+ re.sub(r"\/",r"-", str(time.strftime("%x")))+ "_"+ str(time.strftime("%X"))+".json"
    similarMediaFileName = "data/similar_media/similar_media_"+ re.sub(r"\/",r"-", str(time.strftime("%x")))+ "_"+ str(time.strftime("%X"))+".json"

    print(userInfoFileName)
    usersMapFileName = "data/mappings/users_map_"+re.sub(r"\/",r"-", str(time.strftime("%x")))+ "_"+ str(time.strftime("%X"))+".json"
    usersMap = dict()
    mediaMap = dict()
    mediaMapFileName = "data/mappings/media_map_"+re.sub(r"\/",r"-", str(time.strftime("%x")))+ "_"+ str(time.strftime("%X"))+".json"
    mediaCount =0
    for fileName in os.listdir(inputDirName):
        if fileName[-5:] == ".json":
            data = readJsonFile(inputDirName, fileName)
            for eachMedia in data:
                mediaCount +=1
                originalMediaId = eachMedia["id"]
                print(colored("????????????STARTED processing media " + str(mediaCount) + "  Media iD: " + str(originalMediaId),'magenta'))
                mediaTags = eachMedia["tags"]

                # print(mediaTags)
                coocurringTags = filterTags(mediaTags, getFilterList(filterListFileName))
                coocurringTagsList = list(coocurringTags)
                if len(coocurringTagsList) <= 0:
                    continue
                similarHashTag = coocurringTagsList[0]
                userInfo = getUserInfo(eachMedia)
                if userInfo == "error":
                    print(colored("User info not available","red"))
                    continue
                originalUserId = userInfo["id"]
                saveUserInfo(userInfo,userInfoFileName, sys.argv[1], None)
                orgininalMediaFollowerCount = getFollowerCount(userInfo)
                dataForMapping = getRecentMediaForTag(similarHashTag, orgininalMediaFollowerCount,userInfoFileName, similarMediaFileName, originalMediaId, originalUserId)
                mediaMap[eachMedia["id"]] =dataForMapping[0]["id"]
                usersMap[userInfo["id"]] = dataForMapping[1]["id"]

                with open(usersMapFileName, 'wb') as outputFile:
                    json.dump(usersMap,outputFile)
                with open(mediaMapFileName, 'wb') as outputFile:
                    json.dump(mediaMap,outputFile)
                print(colored("??????????????ENDED processing media  " + str(mediaCount) + "  Media ID: " + str(originalMediaId) + "  User Id: " + str(originalUserId),'magenta'))
            # print(data)
            # break




#python get_similar_media.py follow4follow