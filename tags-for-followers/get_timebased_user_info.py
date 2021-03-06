#!/usr/bin/python
# -*- coding: utf-8 -*-
import json, datetime, time, re
import ConfigParser
import urllib
import os
from termcolor import colored


def createDirectoriesForEachUser(outputDir, userIds):
    for userId in userIds:
        if os.path.exists(outputDir + "/" + userId):
            print(colored("Directory already exist:::: " + str(userId), "red"))
        else:
            os.makedirs(outputDir+"/"+userId)


def createDirectories():

    outputDirOriginalUsers = 'data/users/daily_user_info/users/original_users'
    outputDirSimilarUsers = 'data/users/daily_user_info/users/similar_users'
    inputFileName1 = "data/mappings/user_mapping/users_map1.json"
    inputFileName2 = "data/mappings/user_mapping/users_map2.json"
    createDirs(inputFileName1,outputDirOriginalUsers,outputDirSimilarUsers)
    createDirs(inputFileName2,outputDirOriginalUsers,outputDirSimilarUsers)


def createDirs(inputFileName, outputDirOriginalUsers, outputDirSimilarUsers):
    with open(inputFileName) as user_map:
        userMap = json.load(user_map)
    createDirectoriesForEachUser(outputDirOriginalUsers, userMap.keys())
    createDirectoriesForEachUser(outputDirSimilarUsers, userMap.values())


def createFiles(dirName):
    dailyUsersInfoDir = 'data/users/daily_user_info'
    inputDir = "data/users/" + dirName
    for fileName in os.listdir(inputDir):
        if fileName[-5:] == ".json":

            # dir1 = fileName.split("_")[0]
            dir2 = dirName
            with open(inputDir + "/" + fileName) as inputFile:
                usersMap = json.load(inputFile)
            for key in usersMap.keys():
                dir3 = key
                path = dailyUsersInfoDir+"/" + dir2 + "/" + dir3
                outputFileName = fileName.split("_")[1]
                completePath = path + "/" + outputFileName
                if not os.path.exists(path):
                    os.makedirs(path)
                    print(colored("Directory DOESN'T exist:::: " + str(key) , "red"))
                with open(completePath, "wb") as eachUserFile:
                    json.dump(usersMap[key],eachUserFile)



if __name__ == "__main__":

    createDirectories()
    createFiles("original_users")
    createFiles("similar_users")


    print("DONE")



