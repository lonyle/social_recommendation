# Exp: the profit (price/reward, not necessarily optimal) of the firm, for different kinds of osn
import firm
import sys
sys.path.insert(0, 'preprocess')
import osn
import json

import numpy as np
import matplotlib.pyplot as plt

import matplotlib
font = {'size'   : 18}
matplotlib.rc('font', **font)



def degree_distribution():
	pass

def generate_new_graph(weight):
	''' 
	need to run the simulation again, because the graph is changed 
	weight is the probability to retain current edges
	'''
	# randomly add new edges, and randomly remove edges
	# generate new files of social network graphs
	OSN = osn.OnlineSocialNetwork('yelp')

	# convert the lists to sets
	for user_id in OSN.edges:
		OSN.edges[user_id] = set(OSN.edges[user_id])

	for user_id in OSN.edges:
		friends = list(OSN.edges[user_id])
		for friend_id in friends:
			# randomly remove
			if np.random.random() < weight:
				OSN.edges[user_id].remove(friend_id)
				# remove the symmetry edge
				if friend_id in OSN.edges:
					if user_id in OSN.edges[friend_id]:
						OSN.edges[friend_id].remove(user_id)

	# dump the new osn to file
	with open('data/user_'+str(weight)+'.json', 'w') as output_file:
		for user_id in OSN.edges:
			data = {'user_id': user_id, 'friends': list(OSN.edges[user_id])}
			output_file.write(json.dumps(data) + '\n')	

def clustering_coefficient():
	pass


if __name__ == '__main__':
	#generate_new_graph(0.7) # 'zero': 0.5326705884393421
	generate_new_graph(0.3)