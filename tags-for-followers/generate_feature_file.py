#!/usr/bin/python
# -*- coding: utf-8 -*-
import json, datetime, time, re, csv
import ConfigParser
import urllib
import os
from termcolor import colored
import media_history_extractor
from media_feature_extractor import Media_feature_extractor

columns = ["userId", "usernameLength","followedBy", "follows", "mediaCount", "hasWebsite", "bioHasUrl", "fullNameLength"]
Media_feature_extractor_obj = None
category_ranges = None

def getHeaders():
    return columns

def diffInFollowerCount(userId, startDate, endDate, typeOfUser):
    inputDir = 'data/users/daily_user_info/'+ typeOfUser
    if userId in os.listdir(inputDir):
        try:
            with open(inputDir + "/" + str(userId)+"/"+str(startDate) + ".json" ) as inputFile:
                userData1 = json.load(inputFile)
            with open(inputDir + "/" + str(userId)+"/"+str(endDate) + ".json" ) as inputFile:
                userData2 = json.load(inputFile)
            return userData2["counts"]["followed_by"] - userData1["counts"]["followed_by"]
        except:
            print(colored("For DIFF: unable to open the file for user "+ str(userId), "yellow"))
            return None
    return None


def getFollowerCountCategory(followerCount): 
    global category_ranges
    for index in range(0, len(category_ranges)):
	cat_tuple = category_rages[index]
        if followerCount >= cat_tuple[0] and followerCount <= cat_tuple[1]:
   	    return index
    return None


def writeFeaturesToFile(userId, dataCollectionDate, typeOfUser, writer):
    global Media_feature_extractor_obj
    followerCountDiff = getFollowerCountCategory(diffInFollowerCount(userId, "11-09-15", "11-21-15", typeOfUser))
    if followerCountDiff != None:
        userFeatures = getRequiredUserData(userId, dataCollectionDate, typeOfUser)
        if userFeatures != None:
            oldMediaFeatures = media_history_extractor.create_csv_data(userId)
            currentMediaFeatures = Media_feature_extractor_obj.get_media_details_for_user(userId)
            if oldMediaFeatures != None and currentMediaFeatures != None:
                userFeatures.extend(currentMediaFeatures)
                userFeatures.extend(oldMediaFeatures)
                userFeatures.append(followerCountDiff)
                writer.writerow(userFeatures)

def generateCSV(usermap,dataCollectionDate, modeOfWriting):
    global Media_feature_extractor_obj
    inputFileName1 = "data/mappings/user_mapping/"+ usermap +".json"
    inputFileName2 = "data/mappings/user_mapping/"+usermap+".json"
    outputFileName = 'features.csv'
    outputDir = 'data/features/original_users'
    outputDirSimilarUsers = 'data/features/similar_users'
    with open(inputFileName1) as user_map:
        userMap = json.load(user_map)

    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
    if not os.path.exists(outputDirSimilarUsers):
        os.makedirs(outputDirSimilarUsers)
    with open(outputDir + "/" +outputFileName, modeOfWriting) as outputFile:
        with open(outputDirSimilarUsers + "/" +outputFileName, modeOfWriting) as outputFileSimilarUsers:
            writer = csv.writer(outputFile, delimiter=',')
            if modeOfWriting == "wb":
                userHeaders = getHeaders()
		userHeaders.extend(Media_feature_extractor_obj.get_headers())
                userHeaders.extend(media_history_extractor.get_headers())
                userHeaders.append("diffInFollowerCount")
                writer.writerow(userHeaders)
            for key in userMap:
                writeFeaturesToFile(key,dataCollectionDate, "original_users", writer)
                #writeFeaturesToFile(userMap[key], dataCollectionDate, "similar_users", outputFileSimilarUsers)
                
def getRequiredUserData(userId, dateOfDataCollection, typeOfUser):
    listOfData = None
    inputDir = 'data/users/daily_user_info/'+ typeOfUser
    if userId in os.listdir(inputDir):
        try:
            with open(inputDir + "/" + str(userId)+"/"+str(dateOfDataCollection) + ".json" ) as inputFile:
                userData = json.load(inputFile)
        except:
            print(colored("unable to open the file for user "+ str(userId), "yellow"))
            return None

        user_id = userData["id"]

        username = len(userData["username"])

        counts = userData["counts"]

        # hasProfilePicture = 1
        # if userData["profile_picture"] == None:
        #     print("found someone without profile picture!!! :)")
        #     hasProfilePicture = 0

        bioHasUrl = 0
        if "www." in userData["bio"] or "http:" in userData["bio"]:
            # print("Contains url" + user_id + " with bio " + userData["bio"])
            bioHasUrl = 1

        hasWebsite = 0
        if userData["website"] != None and userData["website"] != "":
            hasWebsite = 1

        fullNameLength = len(userData["full_name"].split(" "))


        listOfData = [str(user_id), str(username), str(counts["followed_by"]), str(counts["follows"]), str(counts["media"]), hasWebsite, bioHasUrl, str(fullNameLength)]
        
    else:
        print(colored("User info not found in db " + userId, "red"))
        return None

    return listOfData




if __name__ == "__main__":
    global Media_feature_extractor_obj
    global category_ranges
    category_ranges = [(-4440, 0),(1, 7),(8, 19), (20, 70), (71, 123657)]
    Media_feature_extractor_obj = Media_feature_extractor()
    generateCSV("users_map1", "11-08-15", "wb")
    generateCSV("users_map2","11-08-15", "ab+")
    print("DONE")



