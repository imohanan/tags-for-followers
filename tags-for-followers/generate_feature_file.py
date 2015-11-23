#!/usr/bin/python
# -*- coding: utf-8 -*-
import json, datetime, time, re, csv
import ConfigParser
import urllib
import os
from termcolor import colored
import media_info_extractor


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


def writeFeaturesToFile(userId, dataCollectionDate, typeOfUser, writer):

    followerCountDiff = diffInFollowerCount(userId, "11-09-15", "11-21-15", typeOfUser)
    if followerCountDiff != None:
        userFeatures = getRequiredUserData(userId, dataCollectionDate, typeOfUser)
        if userFeatures != None:
            mediaFeatures = media_info_extractor.create_csv_data(userId)
            if mediaFeatures != None:
                userFeatures.extend(mediaFeatures)
                userFeatures.append(followerCountDiff)
                writer.writerow(userFeatures)

def generateCSV(usermap,dataCollectionDate, modeOfWriting):

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

        hasProfilePicture = "True"
        if userData["profile_picture"] == None:
            print("found someone without profile picture!!! :)")
            hasProfilePicture = "False"

        bioHasUrl = "False"
        if "www." in userData["bio"] or "http:" in userData["bio"]:
            # print("Contains url" + user_id + " with bio " + userData["bio"])
            bioHasUrl = "True"

        hasWebsite = "False"
        if userData["website"] != None:
            hasWebsite = "True"

        fullNameLength = len(userData["full_name"].split(" "))


        listOfData = [str(user_id), str(username), str(counts["followed_by"]), str(counts["follows"]), str(counts["media"]), hasProfilePicture, hasWebsite, bioHasUrl, str(fullNameLength)]
        
    else:
        print(colored("User info not found in db " + userId, "red"))
        return None

    return listOfData




if __name__ == "__main__":
    generateCSV("users_map1", "11-09-15", "wb")
    generateCSV("users_map2","11-09-15", "ab+")
    print("DONE")



