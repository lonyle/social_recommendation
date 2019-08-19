# propress merge the recommendations into the businesses

import sys
sys.path.insert(0, 'inference')

import checkin_preprocess
import osn
import json
import adoption_prob
import utils

sorted_review_filename = 'data/sorted_review.json'
business_input_filename = 'data/business_checkin.json' # this is the input file from the previous step
business_output_filename = 'data/business_checkin_review.json'

'''add the review_vec, also the recommendation probability, copied from adoption_prob'''
def add_review_vec(business_dict):
	yelp = osn.OnlineSocialNetwork('yelp')

	f = open(sorted_review_filename)

	reviewer_vec = []
	line = f.readline()
	first_review = json.loads(line)
	current_business_id = first_review['business_id']
	while line:
		review = json.loads(line)
		if review['business_id'] != current_business_id:
			# reviewer_vec contains all the reviewers of the current business id
			if current_business_id in business_dict:
				business_dict[current_business_id]['reviewer_vec'] = reviewer_vec
				# p_with, p_without, p_with_type, N_receivers = adoption_prob.adoption_prob(reviewer_vec, yelp)
				# business_dict[current_business_id]['p_with'] = p_with 
				# business_dict[current_business_id]['p_without'] = p_without
				# business_dict[current_business_id]['p_with_type'] = p_with_type
				# business_dict[current_business_id]['N_receivers'] = N_receivers

			reviewer_vec = []
			current_business_id = review['business_id']
		else:
			reviewer_vec.append(review['user_id'])
		line = f.readline()

	f.close()
	return business_dict

def add_receivers_vec(business_dict, OSN):
	for business_id in business_dict:
		if 'reviewer_vec' not in business_dict[business_id]:
			continue
		reviewer_vec = business_dict[business_id]['reviewer_vec']
		reviewer_set = set(reviewer_vec)
		recommendation_receivers = set()

		for reviewer in reviewer_set:
			friends = OSN.edges[reviewer]
			for friend in friends:
				recommendation_receivers.add(friend)

		business_dict[business_id]['review_receiver_vec'] = list(recommendation_receivers)
	return business_dict


if __name__ == '__main__':
	# add the review dict
	business_dict = utils.load_business_by_id(business_input_filename)
	business_dict = add_review_vec(business_dict)

	# add the receivers of the reviews (cannot add, too large)
	#business_dict = utils.load_business_by_id(business_output_filename)
	#yelp = osn.OnlineSocialNetwork('yelp')
	#business_dict = add_receivers_vec(business_dict, yelp)

	utils.dump_business(business_dict, business_output_filename)


