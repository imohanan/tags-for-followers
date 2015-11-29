import math
import csv
import datetime
import json
import os 
from pylab import *
from scipy.stats.stats import pearsonr  
import matplotlib.pyplot

headers = [ 'media_id','user_id', '2015-11-10(likes, comments)', '2015-11-11', '2015-11-12', '2015-11-13', '2015-11-14', '2015-11-15', '2015-11-16', '2015-11-17', '2015-11-18', '2015-11-19' ]
date = None

def plot_scatter_graph(y,x,color_val, title_graph):
	matplotlib.pyplot.scatter(x,y, color =color_val)
	matplotlib.pyplot.title(title_graph)
	matplotlib.pyplot.xlabel('Difference Value')
	matplotlib.pyplot.ylabel('Number of Users') 
	matplotlib.pyplot.show()


def plot_bar_graph(follow_dict, similar_dict, title_graph, color_val1, color_val2):
	matplotlib.pyplot.plot(follow_dict.keys(),follow_dict.values(), color =color_val1)
	matplotlib.pyplot.plot(similar_dict.keys(),similar_dict.values(), color =color_val2)
	matplotlib.pyplot.title(title_graph)
	matplotlib.pyplot.xlabel('Day of Data Collection')
	matplotlib.pyplot.ylabel('Average Count') 
	matplotlib.pyplot.show()


def convert_to_log(dict_name):
	new_dict = {}
	for key, val in dict_name.items():
		if key <= 0: continue
		new_key = math.log(key)
		new_val = math.log(val)
		new_dict[new_key] = new_val
	return new_dict

def get_user_id(data):
	if 'data' not in data: return None
	return data['data']['user']['id']


def extract_features(data):
	if 'data' not in data: return None
	likes =  data['data']['likes']['count']
	comments = data['data']['comments']['count']
	return str(likes)+":"+str(comments)


class Media_Plotter(object):

	def save_daily_media_info(self):
		if os.path.exists('data/plot_media_info') is False: os.makedirs('data/plot_media_info')
		output_file = open('data/plot_media_info/followusers_'+str(date)+'.txt', 'w+')
		output_file.close()
		output_file = open('data/plot_media_info/similarusers_'+str(date)+'.txt', 'w+')
		output_file.close()

		self.follow_media = set()
		self.similar_media = set()
		with open('data/mappings/media_mapping/media_map.json') as mapping_file:
			for line in mapping_file:
				data =  json.loads(line)
				for key, val in data.items():
					if val == None or (key in self.follow_media) or (val in self.similar_media): continue
					self.follow_media.add(key)
					self.similar_media.add(val)
			print len(self.follow_media)
			print len(self.similar_media)

		count = 0
		follow_output_file = open('data/plot_media_info/followusers_'+str(date)+'.txt', 'wb')
		spamwriter = csv.writer(follow_output_file, dialect = 'excel')
		spamwriter.writerow(headers)

		for media_id in self.follow_media:
			count += 1
			if count%1000 == 0: print count
			features = [media_id]

			for folder in ['data/media_info/2015-11-10', 'data/media_info/2015-11-11', 'data/media_info/2015-11-12', 'data/media_info/2015-11-13', 'data/media_info/2015-11-14', 'data/media_info/2015-11-15', 'data/media_info/2015-11-16', 'data/media_info/2015-11-17', 'data/media_info/2015-11-18', 'data/media_info/2015-11-19']:
				media_file_name = folder +'/' + media_id + '.json'
				if os.path.isfile(media_file_name):
					with open(media_file_name, 'r') as media_file:
						data = json.load(media_file)
						if len(features) == 1: features.append(get_user_id(data))
						features.append(extract_features(data))
				else:  
					features.append( None)
					print folder
					print media_id
					input('Enter')

			spamwriter.writerow(features)
		follow_output_file.close()
		print 'Follow Users Completed'
				
		count = 0
		similar_output_file = open('data/plot_media_info/similarusers_'+str(date)+'.txt', 'wb')
		spamwriter = csv.writer(similar_output_file, dialect = 'excel')
		spamwriter.writerow(headers)	
		for media_id in self.similar_media:
			count += 1
			if count%1000 == 0: print count
			features = [media_id]
			for folder in ['data/media_info/2015-11-09', 'data/media_info/2015-11-10', 'data/media_info/2015-11-11', 'data/media_info/2015-11-12', 'data/media_info/2015-11-13', 'data/media_info/2015-11-14', 'data/media_info/2015-11-15', 'data/media_info/2015-11-16', 'data/media_info/2015-11-17', 'data/media_info/2015-11-18', 'data/media_info/2015-11-19']:
				media_file_name = folder +'/' + media_id + '.json'
				if os.path.isfile(media_file_name):
					with open(media_file_name, 'r') as media_file:
						data = json.load(media_file)
						if len(features) == 1: features.append(get_user_id(data))
						features.append(extract_features(data))
				else:  
					features.append( None)
					print folder
					print media_id
					input('Enter')
			spamwriter.writerow(features)
		similar_output_file.close()
		print 'Similar Users Completed'

					
	def plot_media_avg_graph(self, file_name):
		daily_likes_sum = {}
		daily_likes_count = {}
		daily_comments_sum = {}
		daily_comments_count = {}
		
		daily_avg_comments = {}
		daily_avg_likes = {}

		#follow user
		with open(file_name, 'r') as follow_output_file:
			spamreader = csv.reader(follow_output_file, dialect = 'excel')
			for row in spamreader:
				if row[0]=='media_id': continue
				for index in range(2, 12):
					vals = row[index].split(":")	
					if len(vals) <2: continue
					if index not in daily_likes_sum:
						daily_likes_sum[index] = 0
						daily_likes_count[index] = 0
						daily_comments_sum[index] = 0
						daily_comments_count[index] = 0
					daily_likes_sum[index] += int(vals[0])
					daily_comments_sum[index] += int(vals[1])
					daily_likes_count[index] += 1
					daily_comments_count[index] += 1
			for key in daily_likes_sum.keys():
				daily_avg_comments[key] = float(daily_comments_sum[key])/ float(daily_comments_count[key])
				daily_avg_likes[key] = float(daily_likes_sum[key])/ float(daily_likes_count[key])
				
		return daily_avg_likes, daily_avg_comments
	

	def plot_media_total_change_graph(self, file_name):		
		comments_diff_count = {}
		likes_diff_count = {}

		with open(file_name, 'r') as follow_output_file:
			spamreader = csv.reader(follow_output_file, dialect = 'excel')
			for row in spamreader:
				if row[0]=='media_id': continue
				if row[2] =='' or row[11] == '': continue
				user_id = row[1]
				first_vals = row[2].split(':')
				last_vals = row[11].split(':')
				likes_diff = int(last_vals[0]) - int(first_vals[0])
				if likes_diff not in likes_diff_count: likes_diff_count[likes_diff] = 0
				likes_diff_count[likes_diff] += 1
				comments_diff = int(last_vals[1]) - int(first_vals[1])
				if comments_diff not in comments_diff_count: comments_diff_count[comments_diff] = 0
				comments_diff_count[comments_diff] += 1
		return likes_diff_count, comments_diff_count


	def calculate_follower_media_correlation(self, media_file, follower_file):
		# 1. save media information		
		user_likes_dict = {}
		user_comments_dict = {}
		with open(media_file, 'r') as follow_output_file:
			spamreader = csv.reader(follow_output_file, dialect = 'excel')
			for row in spamreader:
				if row[0]=='media_id': continue
				user_id = row[1]
				if user_id is '': continue
				likes = []
				comments = []
				for index in range(2, 12):
					vals = row[index].split(":")	
					if len(vals) <2: break
					likes.append(int(vals[0]))
					comments.append(int(vals[1]))
				if len(likes) == 10:
					user_likes_dict[user_id] = likes
					user_comments_dict[user_id] = comments
		
		# 2. save follower information
		user_follower_dict = {}
		with open(follower_file, 'r') as follower_file:
			data = json.load(follower_file)
			for key, val in data.items():
				user_id = key
				if user_id == 517642152: print 'FOUND!!!!'
				followers = []
				followers_count = val['0']
				for index in range(9, 19):
					index = str(index)
					difference = val[index]
					followers_count += difference
					followers.append(followers_count)
				user_follower_dict[str(user_id)] = followers
	
		#3. LIKES & COMMENTS CORRELATION AVERAGE
		likes_correlation_sum = 0
		comments_correlation_sum = 0
		likes_count = 0
		comments_count = 0
		skipped_count = 0
		for user in user_likes_dict.keys():
			if user not in user_follower_dict: 
				#print 'skipped' + str(skipped_count)
				skipped_count += 1
				continue
			likes = user_likes_dict[user]
			comments = user_comments_dict[user]
			followers =   user_follower_dict[user]
			likes_correlation = pearsonr(likes, followers)
			comments_correlation = pearsonr(comments, followers)
			if math.isnan(likes_correlation[0]) is False:
				likes_correlation_sum += likes_correlation[0]
				likes_count += 1
			if math.isnan(comments_correlation[0]) is False:
				comments_correlation_sum += comments_correlation[0]
				comments_count += 1
		avg_likes_correlation = float(likes_correlation_sum)/ float(likes_count)
		avg_comments_correlation = float(comments_correlation_sum)/ float(comments_count)
		print 'Average likes Correlation : '+ str(avg_likes_correlation )
		print 'Average comments Correlation : '+ str(avg_comments_correlation )




if __name__ == '__main__':
	
	date = datetime.date.today()
	media_plotter = Media_Plotter()
	#media_plotter.save_daily_media_info()
	# 1. CORRELATION VALUES
	print 'Follow user Correlation'
	media_plotter.calculate_follower_media_correlation('data/plot_media_info/followusers_'+str(date)+'.txt', 'data/diff_in_followed_by _count.json')
	print 'Similar user Correlation'
	media_plotter.calculate_follower_media_correlation('data/plot_media_info/similarusers_'+str(date)+'.txt','data/similar_diff_in_followed_by _count.json')
	
	# 2. DAILY AVERAGE OF LIKES AND COMMENTS
	follow_avg_likes, follow_avg_comments = media_plotter.plot_media_avg_graph('data/plot_media_info/followusers_'+str(date)+'.txt')
	similar_avg_likes, similar_avg_comments = media_plotter.plot_media_avg_graph('data/plot_media_info/similarusers_'+str(date)+'.txt')
	print 'Follow vs Similar Users - Average Comments'
	plot_bar_graph(follow_avg_comments, similar_avg_comments, 'Average Comments per day', 'red', 'blue')
	print 'Follow vs Similar Users - Average Likes'
	plot_bar_graph(follow_avg_likes, similar_avg_likes, 'Average Likes per day', 'red', 'blue')

	# 3. Difference Graph
	follow_likes_diff, follow_comments_diff = media_plotter.plot_media_total_change_graph('data/plot_media_info/followusers_'+str(date)+'.txt')
	follow_likes_diff = convert_to_log(follow_likes_diff)
	follow_comments_diff = convert_to_log(follow_comments_diff)

	similar_likes_diff, similar_comments_diff = media_plotter.plot_media_total_change_graph('data/plot_media_info/similarusers_'+str(date)+'.txt')
	similar_likes_diff = convert_to_log(similar_likes_diff)
	similar_comments_diff = convert_to_log(similar_comments_diff)
	plot_scatter_graph(follow_likes_diff.values(), follow_likes_diff.keys(),'red','FollowUsers: Total Difference in likes')
	plot_scatter_graph(similar_likes_diff.values(), similar_likes_diff.keys(),'blue','SimilarUsers: Total Difference in likes')
	
	plot_scatter_graph(follow_comments_diff.values(), follow_comments_diff.keys(), 'red', 'Total Difference in Comments')
	plot_scatter_graph(similar_comments_diff.values(), similar_comments_diff.keys(), 'blue', 'Total Difference in Comments')
	
