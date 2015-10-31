import ConfigParser
import urllib2, urllib
import re
import time
import os
from datetime import date
import json

config = None

def save_user(user_id, directory):
	directory = directory +'/'+ str(user_id)
	if not os.path.exists(directory):
    		os.makedirs(directory)

	next_url = 'https://api.instagram.com/v1/users/'+str(user_id)+'/followed-by?access_token='+config.get('UserDetails','access_token')
	count = 0
	while True:	
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


if __name__ == '__main__':
	config = ConfigParser.ConfigParser()
	config.read('defaults.cfg')

	date = date.today()
	directory = 'data/users_followed_by/'+str(date)
	if not os.path.exists(directory):
    		os.makedirs(directory)

	media_folders = ['data/recent_media/follow4follow', 'data/recent_media/followme', 'data/recent_media/followme', 'data/recent_media/spam4spam']
	for folder in media_folders:
		for input_file in os.listdir(folder):
			file_path = folder + '/' +input_file	
			with open(file_path) as data_file:
				data = json.load(data_file)
				for media in data['data']:
					try:
						user_id = media['user']['id']
						save_user(user_id, directory)
						print user_id
					except:
						print 'Error for user' +user_id

	
		
