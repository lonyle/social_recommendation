import matplotlib.pyplot as plt 
import numpy as np 
import matplotlib
font = {'size': 20}
matplotlib.rc('font', **font)

import json

def find_high_occupation_prob(business_filename):
	recommend_prob_vec = []
	review_count_vec = []
	f = open(business_filename)
	line = f.readline()
	while line:
		business = json.loads(line)
		line = f.readline()
		if 'p_with' not in business or business['p_with'] == None:
			continue
		if business['review_count'] > 500: #and business['p_with'] > 0.02:
			recommend_prob_vec.append(business['p_with'])
			review_count_vec.append(business['review_count'])
			#print (business['name'], business['p_with'], business['review_count'])

	fig = plt.figure()
	ax = fig.add_axes([0.19, 0.15, 0.74, 0.8])
	ax.scatter(recommend_prob_vec, review_count_vec, alpha=0.2, color='black')
	plt.xlabel('recommendation probability')
	plt.ylabel('number of reviews')
	plt.savefig('images/p_and_reviewcount.eps', dpi=1200)
	plt.savefig('images/p_and_reviewcount.png', dpi=1200)
	plt.show()
	f.close()

if __name__ == '__main__':
	find_high_occupation_prob('data/business_checkin_review.json')