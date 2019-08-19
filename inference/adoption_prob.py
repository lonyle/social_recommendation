# the effectiveness of recommendations on the prob. for users to recommend

import json

import sys
sys.path.insert(0, 'simulation')
sys.path.insert(0, 'preprocess')

import osn
import setting

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

sorted_review_filename = 'data/sorted_review.json'
output_filename = 'data/output_adoption_prob.json'

Types = setting.Types

'''
input:
	1. reviewer_vec: a list of users who make recommendations
	2. OSN: the osn graph
output:
	1. p_with: the overall prob. for a user to recommend when one of his friends recommend
	2. p_without: the overall prob. for a user to recommend when none of his friends recommend
	3. p_with_type: 
	4. len(all_recommendation_receivers)
'''
def recommend_prob(reviewer_vec, OSN): # occupation prob
	# for a specific business
	reviewer_set = set(reviewer_vec)
	
	N = OSN.N_node

	recommendation_receivers = {}
	# mark the users with recommendations
	for Type in simulation_setting.Types:
		recommendation_receivers[Type] = set()

	for reviewer in reviewer_set:
		friends = OSN.edges[reviewer]
		for friend in friends:
			if friend in OSN.edges:
				degree = len(OSN.edges[friend])
				Type = simulation_setting.type_of_node(degree)
				recommendation_receivers[Type].add(friend)
	if len(recommendation_receivers['small']) == 0 or len(recommendation_receivers['medium']) == 0 or len(recommendation_receivers['large']) == 0:
		return None, None, None, None

	all_recommendation_receivers = recommendation_receivers['small'] | recommendation_receivers['medium'] | recommendation_receivers['large']
	# maybe this should not be unified
	p_with = len( reviewer_set.intersection(all_recommendation_receivers) ) / len(all_recommendation_receivers)
	p_without = len( reviewer_set.difference(all_recommendation_receivers) ) / (N-len(all_recommendation_receivers))

	p_with_type = dict()
	for Type in simulation_setting.Types:
		p_with_type[Type] = len( reviewer_set.intersection(recommendation_receivers[Type]) ) / len(recommendation_receivers[Type])
	
	return p_with, p_without, p_with_type, len(all_recommendation_receivers)
	
def diffusion_params(p_with, p_without, p_with_type):
	initial_prob = p_without / p_with
	occupation_prob_type = p_with_type
	return initial_prob, occupation_prob_type

	
