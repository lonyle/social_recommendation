# compare the diffusion size in the original data and the diffusion size predicted by the percolation model

# the key: uniform diffusion probability

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import sampling_size
import sampling
import adoption_prob
import osn
import json
import numpy as np
import simulation_setting

sorted_review_filename = 'data/sorted_review.json'

#possibly duplicated
N_node_type = {'medium': 349188, 'small': 843456, 'large': 133457}
occupation_scale = simulation_setting.occupation_scale

def get_est_size(p_with, p_without):
	initial_prob = p_without/p_with
	occupation_prob = p_with
	awared_prob = sampling_size.get_expected_size(initial_prob, occupation_prob)
	# TODO: problem needed to be fixed
	estimated_fraction = awared_prob * p_with #+ (1-awared_prob) * p_without
	return estimated_fraction

def businesses_traverse():
	yelp = osn.OnlineSocialNetwork('data/user.json')

	estimated_size_vec = []
	true_size_vec = []

	f = open(sorted_review_filename)

	reviewer_vec = []
	line = f.readline()
	first_review = json.loads(line)
	current_business_id = first_review['business_id']
	while line:
		review = json.loads(line)
		if review['business_id'] != current_business_id:
			p_with, p_without, p_with_type = adoption_prob.adoption_prob(reviewer_vec, yelp)

			if p_with != None and p_with != 0 and np.random.random()>0.8: # process the business
				# estimated_fraction_uniform = get_est_size(p_with, p_without)
				# estimated_size_uniform = estimated_fraction_uniform * yelp.N_node
				# print ('estimated_size_uniform:', estimated_size_uniform)

				# reconstruct the occupation prob
				x = p_with * yelp.N_node / (occupation_scale['small']*N_node_type['small'] \
						+ occupation_scale['medium']*N_node_type['medium'] \
						+ occupation_scale['large']*N_node_type['large'])
				occupation_prob_type = dict()
				for Type in simulation_setting.Types:
					occupation_prob_type[Type] = x * occupation_scale[Type]
				estimated_fraction = sampling.get_est_recommend_prob(yelp, p_without/p_with, occupation_prob_type)
				estimated_size = estimated_fraction * yelp.N_node				
				estimated_size_vec.append(estimated_size)
				print ('p_with_type:', p_with_type)
				print ('occupation_prob_type', occupation_prob_type)		
				print ('estimated_size:', estimated_size)
				
				true_size = len(reviewer_vec)
				true_size_vec.append(true_size)
				print ('true_size:', true_size)

			reviewer_vec = []
			current_business_id = review['business_id']
		else:
			reviewer_vec.append(review['user_id'])
		line = f.readline()

	f.close()
	return estimated_size_vec, true_size_vec

def compare(estimated_size_vec, true_size_vec):
	# the first measure: compare the sum of estimated size and true size
	print ('the ratio between two sums is:', sum(estimated_size_vec)/sum(true_size_vec))

if __name__ == '__main__':
	estimated_size_vec, true_size_vec = businesses_traverse()
	compare(estimated_size_vec, true_size_vec)
