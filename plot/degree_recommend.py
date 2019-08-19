# investigate the impact of degree on recommendation probability

import json
import sys
sys.path.insert(0, 'simulation')
import setting
sys.path.insert(0, 'preprocess')
import osn
import numpy as np 
import matplotlib.pyplot as plt

business_filename = 'data/business_checkin_review.json'
degree_analysis_filename = 'result_degree_recommend.json'

def degree_recommend(is_type, osn):
	'''
	need to prepare 
	1. the dict of the degrees for each user (or the osn network)
	2. the senders and receivers for each item
	'''
	
	count_re_senders_dict = dict()
	count_receivers_dict = dict()
	for line in open(business_filename):
		item = json.loads(line)
		if 'reviewer_vec' not in item:
			continue
		reviewer_set = set(item['reviewer_vec'])
		recommendation_receivers = set()
		# get the receivers
		for reviewer in reviewer_set:
			friends = osn.edges[reviewer]
			for friend in friends:
				recommendation_receivers.add(friend)

		for receiver in recommendation_receivers:
			if receiver not in osn.edges:
				continue
			degree = len(osn.edges[receiver])
			degree_type = setting.type_of_node(degree)
			if is_type == False:
				key = key_of_degree(degree)
			else:
				key = degree_type
			if key not in count_receivers_dict:
				count_receivers_dict[key] = 0
				count_re_senders_dict[key] = 0

			count_receivers_dict[key] += 1
			if receiver in reviewer_set:
				count_re_senders_dict[key] += 1

	rate_dict = dict()
	for key in count_re_senders_dict:
		re_send_rate = count_re_senders_dict[key]/count_receivers_dict[key]
		rate_dict[key] = re_send_rate

	if is_type == False:
		with open(degree_analysis_filename, 'w') as output_file:
			json.dump(rate_dict, output_file, indent=4)

	else:
		print ('rate_dict:', rate_dict)

def key_of_degree(degree):
	if degree < 100:
		return int(degree/10)*10 + 5
	elif degree < 500:
		return int(degree/50)*50 + 25
	else:
		return int( (degree-500)/200)*200 +500 + 100

def width_of_degree(degree):
	if degree < 100:
		return 5
	elif degree < 500:
		return 25
	else:
		return 100

def plot_degree_recommend():
	rate_dict = json.load(open(degree_analysis_filename))
	key_vec = []
	value_vec = []
	width_vec = []
	for key in rate_dict:
		key_vec.append(int(key))
		value_vec.append(rate_dict[key])
		width = width_of_degree(int(key))
		width_vec.append(width*2)

	import matplotlib
	font = {'size': 20}
	matplotlib.rc('font', **font)

	fig = plt.figure()
	ax = fig.add_axes([0.19, 0.15, 0.74, 0.8])
	
	ax.bar(key_vec, value_vec, width_vec, color='black', alpha=0.5) #fill=False, hatch='/'
	plt.xlim(0, 2500)
	plt.ylim(0, 0.01)
	plt.xlabel('number of friends of a user')
	plt.ylabel('recommendation probability')
	plt.savefig('images/yelp_degree_rec_prob.eps', dpi=1200)
	plt.savefig('images/yelp_degree_rec_prob.png', dpi=1200)
	plt.show()

if __name__ == '__main__':
    #yelp = osn.OnlineSocialNetwork('yelp') 
    #is_type = False
    #degree_recommend(is_type, yelp)
    plot_degree_recommend()




