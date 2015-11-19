import ConfigParser
import urllib2, urllib
import re
import time
import os


def recent_media(tags):
	config = ConfigParser.ConfigParser()
	config.read('defaults.cfg')
	
	for tag in tags:
		if not os.path.exists('data/recent_media/'+tag):
    			os.makedirs('data/recent_media/'+tag)
		count = 0
		next_url = 'https://api.instagram.com/v1/tags/'+tag+'/media/recent?access_token='+config.get('UserDetails','access_token')
		while( count < 600):
			count += 1
			file_name = 'data/recent_media/'+tag+"/"+"10.23_"+str(count)+'.json'
			url = next_url

			result = urllib2.urlopen(url).read()
			with open(file_name, 'w+') as op_file:
				op_file.write(result)
			print file_name

			result = urllib.unquote(result).decode('unicode_escape')
			result = result.replace('\/','/')
			
			reg_exp = r'"next_url":"(.*)"},"meta":'
			url_result = re.search(reg_exp, result)
			next_url =  url_result.group(1)	

			time.sleep(0.1)
	#print result

if __name__ == '__main__':
	tags = ['followme']# 'follow4follow', 
	recent_media(tags)
