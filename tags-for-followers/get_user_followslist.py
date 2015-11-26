import time
import ConfigParser
import urllib2, urllib
import re
import time
import os
from datetime import date
import json
import random

config = None
token = None
token_count = 0
token_names = ['UserDetails','UserDetails1','UserDetails2','UserDetails3','UserDetails4','UserDetails5']
last_seen_exception = None

def save_user_friends(user, directory):
	user_directory = directory +'/'+ str(user)
	for file_num in os.listdir(user_directory):
		with open(user_directory+'/'+file_num, 'r') as frnd_file:
			data = json.load(frnd_file)
			for user in data["data"]:
				user_id = user['id']
				save_user(user_id, directory)

	
def save_user(user_id, directory):
	global token
	global last_seen_exception
	global token_names
	global token_count
	if str(user_id) in os.listdir(directory): return

	directory = directory +'/'+ str(user_id)
	if not os.path.exists(directory):
    		os.makedirs(directory)

	next_url = 'https://api.instagram.com/v1/users/'+str(user_id)+'/follows?access_token='+token
	count = 0
	while True:
		try:	
			time.sleep(0.1)
			url = next_url
			result = urllib2.urlopen(url).read()

			file_name = directory + '/' + str(count) +".json"
			with open(file_name, 'w+') as op_file:
				op_file.write(result)

			result = urllib.unquote(result).decode('unicode_escape')
			result = result.replace('\/','/')
	
			reg_exp = r'"next_url":"(.*)","next_cursor":'
			url_result = re.search(reg_exp, result)
			if url_result == None: break		
			next_url =  url_result.group(1)	
	
			count += 1
			time.sleep(0.1)
		except urllib2.HTTPError, e:
			print url			
			print 'exception ' + str(e)
			if e.code == 429:
				if last_seen_exception == None	: last_seen_exception = time.time()
				elif time.time() - last_seen_exception < 1: raise Exception('API limit reached')
				else: last_seen_exception = time.time()
				print 'using next token'
				token_count = (token_count+1)%len(token_names)
				old_token = token
				token = config.get(token_names[token_count],'access_token')
				url = url.replace(old_token, token)
				next_url = url
			else: return
		except Exception, e:
			print 'exception ' + str(e)
			print '\t Error for user '+str(user_id)
			return			
	print '\t'+str(user_id)


if __name__ == '__main__':
	global token
	global token_names
	global token_count
	config = ConfigParser.ConfigParser()
	config.read('defaults.cfg')
	token = config.get(token_names[token_count],'access_token')
	date = date.today()
	directory = 'data/users_follows'
	if not os.path.exists(directory):
    		os.makedirs(directory)

	selected_users = {}
	# loading the previously selected users to avoid repeatition
	selected_users_file = directory+'/selected_users.txt'
	if os.path.isfile(selected_users_file):
		with open(selected_users_file, 'r') as mapped_users_file:
			for line in mapped_users_file:
				vals = line.split()
				if len(vals) < 2: continue
				selected_users[int(vals[0])] = int(vals[1])
	else: 
		mapped_users_file = open(selected_users_file, 'w+')
		mapped_users_file.close()
		
	users_map_file = 'data/mappings/user_mapping/users_map_followers_1.json'
	with open(users_map_file) as users_file:
		data = json.load(users_file)
		keys = data.keys()

		for key in keys:
			user, similar_user = key, int(data[str(key)])
			if user in selected_users: continue			
			print 'saving data of user '+ str(user)
			save_user(user, directory)
			#print 'saving friends of user '+ str(user)
			#save_user_friends(user, directory)
			print 'saving data of similar user '+ str(similar_user)
			save_user(similar_user, directory)
			#print 'saving friends of similar user '+ str(similar_user)
			#save_user_friends(similar_user, directory)
			selected_users[user] = similar_user
			with open(selected_users_file, 'a') as mapped_users_file:
				mapped_users_file.write('\n'+str(user) + ' ' + str(similar_user))
				print 'users found ' + str(len(selected_users))
