import os
import json
import pickle

class tag:
	id_count = 0

	def __init__ (self, tag_name):
		self.id = tag.id_count
		tag.id_count += 1
		self.tag = tag_name
		self.linked_tag = {}
	
	def link(self, tag_id):
		if tag_id not in self.linked_tag:
			self.linked_tag[tag_id] = 1
		else:
			self.linked_tag[tag_id] += 1


if __name__ == '__main__':
	
	media_folders = ['data/recent_media/follow4follow', 'data/recent_media/followme', 'data/recent_media/followme', 'data/recent_media/spam4spam']
	tag_map = {}
	for folder in media_folders:
		for input_file in os.listdir(folder):
			file_path = folder + '/' +input_file	
			with open(file_path) as data_file:
				data = json.load(data_file)
				for media in data['data']:
					try:
						for tag1 in media['tags']:
							if tag1 in tag_map:	
								tag_node = tag_map[tag1]
							else:
								tag_node = tag(tag1)
								tag_map[tag1] = tag_node

							for tag2 in media['tags']:
								if tag1 == tag2:	continue
								if tag2 not in tag_map:
									tag_map[tag2] = tag(tag2)
								tag2_node = tag_map[tag2]
								tag_node.link(tag2_node.id)
						#print 'Read media ' + media['id']
							
					except Exception,e:
						print 'Error in reading media ' + media['id']
						print str(e)
		print 'read folder '+ folder
	
	pickle.dump( tag_map, open( "data/co-occur.txt", "wb" ) )
