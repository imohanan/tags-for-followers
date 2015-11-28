from sets import Set
import operator
import os
import json
from pylab import *
import numpy as np


def write_to_file(tag_Map, fileName, mediacount):
	cooccur_file = open( fileName, "w" )
	cooccur_file.close()
	sorted_map = sorted(tag_Map.items(), key=lambda x: x[1], reverse = True)
	for key in sorted_map:
		percent = float(key[1]) * 100 / float(mediacount) 
		try:
			line = str(key[0]).encode('utf-8') + ':' + str(percent)
			with open( fileName, "a" ) as cooccur_file:
				cooccur_file.write(line)
				cooccur_file.write('\n')
		except Exception , e:
			print key[0]
	

def plot_graph(fileName, count, titleOfgraph):
	y_vals= []
	x_vals = []
	with open(fileName, 'r') as result_file:
		for line in result_file:
			count = count - 1
			if count < 0: break
			vals = line.split(':')
			y_vals.append(vals[0])
			x_vals.append(float(vals[1].strip()))

	pos = arange(10) +0.5
	barh(pos, x_vals, align = 'center', color = '#000077')
	yticks(pos, y_vals)
	xlabel('Percentage of Hashtag')
	ylabel('Hashtag')
	title(titleOfgraph)
	show()

if __name__ == '__main__':
	# initialize

	with open('data/mappings/media_mapping/media_map.json', 'r') as media_file:
		media_data = json.load(media_file)
	follow_media = {}
	similar_media = {}
	for follow, similar in  media_data.items():
		follow_media[follow] = False
		similar_media[similar] = False

	similar_match_words = ["like", "follo", "spam", "shoutout", "comment", "recent"]
	exact_match_words = []
	for line in open('follow_tags_list.txt'):
		exact_match_words.append(line.strip())

	# follow tags	
	media_folders = ['data/recent_media/follow4follow','data/recent_media/followme']
	tag_Map = {}
	mediacount = 0

	for folder in media_folders:	
		for input_file in os.listdir(folder):
			file_path = folder + '/' +input_file	
			with open(file_path) as data_file:
				data = json.load(data_file)
				for media in data['data']:
					if media['id'] not in follow_media or follow_media[media['id']] == True: continue
					follow_media[media['id']] = True
					mediacount = mediacount + 1
					try:

						for tag2 in media['tags']:
							# check if follow tag, if true continue
							is_follow_tag = False
							for follow_word in exact_match_words:
								if follow_word == tag2:
									is_follow_tag = True
							for follow_word in similar_match_words:
								if follow_word in tag2:	
									is_follow_tag = True
							if is_follow_tag == True: continue
							
							if tag2 not in tag_Map: 
								tag_Map[tag2] = 0
							tag_Map[tag2] += 1
					#print 'Read media ' + media['id']
							
					except Exception,e:
						print 'Error in reading media ' + media['id']
						print str(e)
		print 'read folder '+ folder
	if os.path.isdir('data/co-occur_hashtags') == False:	os.makedir('data/co-occur_hashtags')
	write_to_file(tag_Map, "data/co-occur_hashtags/follow_co-occur.txt", mediacount)
	print mediacount
	print len(follow_media)

	#similar media tags
	similar_tag_Map = {}
	similar_mediacount = 0
	for input_file in os.listdir('data/similar_media'):
		file_path = 'data/similar_media/' +input_file	
		with open(file_path) as data_file:
			for line in data_file:
				media = json.loads(line)
				if media['id'] not in similar_media or similar_media[media['id']] == True: continue
				similar_media[media['id']] = True
				similar_mediacount = similar_mediacount + 1
				try:
					for tag2 in media['tags']:
						if tag2 not in similar_tag_Map: 
							similar_tag_Map[tag2] = 0
						similar_tag_Map[tag2] += 1
				#print 'Read media ' + media['id']
							
				except Exception,e:
					print 'Error in reading media ' + media['id']
					print str(e)
	print 'read folder '+ folder

	write_to_file(similar_tag_Map, "data/co-occur_hashtags/similar_co-occur.txt", similar_mediacount)
	print similar_mediacount
	print len(similar_media)

	plot_graph("data/co-occur_hashtags/similar_co-occur.txt", 10, 'Popular Hashtags in Similar Users')
	plot_graph("data/co-occur_hashtags/follow_co-occur.txt", 10, 'Popular Hashtags in Follow Users')
