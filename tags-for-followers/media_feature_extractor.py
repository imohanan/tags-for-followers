import json
import os


class Media_feature_extractor:
	
	def __init__(self):
		self.follow_media_ids = None
		self.user_media_map = {}

		with open('data/mappings/media_mapping/media_map.json') as media_map:
			data = json.load(media_map)
			self.follow_media_ids = data.keys()

		for folder in os.listdir('data/recent_media'):
			folder = 'data/recent_media/' + folder
			for file_name in os.listdir(folder):
				with open(folder + '/' + file_name, 'r') as media_file:
					data = json.load(media_file)

					for media in data['data']:
						if media['id'] not in self.follow_media_ids: continue
						user_id = media['user']['id']
						self.user_media_map[user_id] = media

		self.similar_match_words = ["like", "follo", "spam", "shoutout", "comment", "recent"]
		self.exact_match_words = []
		for line in open('follow_tags_list.txt'):
			self.exact_match_words.append(line.strip())
		
	
	def get_headers(self):
		headers = ['NumberOfTags', 'LocationIncluded', 'NumberWordsInCaption', 'NumberOfUsersTagged']	
		return headers


	def get_media_details_for_user(self,userId):
		if userId not in self.user_media_map: return None
		features = []
		media = self.user_media_map[userId]

		# 1.Number of tags
		if 'tags' in media: 
			len_tags = len(media['tags'])
			features.append(len_tags)
		else: features.append(0)

		# 2. number of follow tags
		follow_tag_count = 0
		if 'tags' not in media: follow_tag_count = 0
		else:		
			for tag in media['tags']:
				is_follow_tag = False
				for follow_word in self.exact_match_words:
					if follow_word == tag:	is_follow_tag = True
				for follow_word in self.similar_match_words:
					if follow_word in tag:	is_follow_tag = True
				if is_follow_tag == True: follow_tag_count += 1
		features.append(follow_tag_count)

		# 3. percentage of follow tags
		if 'tags' not in media: features.append(0)
		else: features.append( float(follow_tag_count) / float( len(media['tags']) ) )

		# 4. location present
		if 'location' not in media == 0: features.append(0)
		else: features.append(1)

		# 5. number of words in caption
		if 'caption' not in media or 'text' not in media['caption']:features.append(0) 
		else:
			caption = media['caption']['text']
			words = caption.split()
			features.append(len(words))

		# 6. number of users
		if 'users_in _photo' not in media: features.append(0)
		else: features.append(len(media['users_in_photo']))

		# filter used for media? 
		# emoticons in caption
			
		# pos in caption
		# sentiment of caption
		# number of exclamation marks?
		# user has liked
		return features

if __name__ == '__main__':
	media_feature_extractor = Media_feature_extractor()
	feature = media_feature_extractor.get_media_details_for_user(str(1499631740))
	print feature
	print media_feature_extractor.get_headers()
