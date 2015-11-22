#!/usr/bin/python
# -*- coding: utf-8 -*-
import json, datetime, time, re
import ConfigParser
import urllib
import os
from termcolor import colored

def writeFeaturesToFile(userId, dataCollectionDate, typeOfUser, outputFile):

    SEPARATOR = " , "
    userFeatures = getRequiredUserData(userId, dataCollectionDate, typeOfUser)
    if userFeatures != None:
        mediaFeatures = list()#TODO : add call to the media features function here
        if mediaFeatures != None:
            userFeatures.extend(mediaFeatures)
            print(userFeatures)
            featuresStr = SEPARATOR.join(userFeatures)
            print(featuresStr)
            outputFile.write(featuresStr + "\n")

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
            for key in userMap:
                writeFeaturesToFile(key,dataCollectionDate, "original_users", outputFile)
                writeFeaturesToFile(userMap[key], dataCollectionDate, "similar_users", outputFileSimilarUsers)
                


    



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
            print("Contains url" + user_id + " with bio " + userData["bio"])
            bioHasUrl = "True"

        hasWebsite = "False"
        if userData["website"] != None:
            hasWebsite = "True"

        fullNameLength = len(userData["full_name"].split(" "))


        listOfData = [str(user_id), str(username), str(counts["followed_by"]), str(counts["follows"]), str(counts["media"]), hasProfilePicture, hasWebsite, bioHasUrl, str(fullNameLength)]
        print(userData)
        print("&&&&")
        print(listOfData)
    else:
        print(colored("User info not found in db " + userId, "red"))
        return None

    return listOfData




if __name__ == "__main__":
    generateCSV("users_map1", "11-09-15", "w")
    generateCSV("users_map2","11-09-15", "a+")
    print("DONE")



