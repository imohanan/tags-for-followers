
import ConfigParser
import urllib2, urllib
import re
import time

if __name__ == '__main__':
	config = ConfigParser.ConfigParser()
	config.read('defaults.cfg')
	
	tags = ['follow4follow']#,'like4like', 'spam4spam', 'followme']
	for tag in tags:
		count = 0
		next_url = 'https://api.instagram.com/v1/tags/'+tag+'/media/recent?access_token='+config.get('UserDetails','access_token')
		while( count < 150):
			count += 1
			file_name = 'data/recent_media/'+tag"/"+"10.23_"+str(count)+'.json'
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

			time.sleep(1)
	#print result
