# the analysis on the inferred adoption prob.

import sys
sys.path.insert(0, 'inference')
import adoption_prob
import json

import matplotlib.pyplot as plt 
import numpy as np 
import matplotlib
font = {'size': 20}
matplotlib.rc('font', **font)

output_filename = 'data/result_adoption_prob.json'

def calculate():
	yelp = osn.OnlineSocialNetwork('data/user.json')

	f = open(sorted_review_filename)

	p_with_vec = []
	p_without_vec = []
	ratio_vec = []
	weight_vec = []
	reviewer_vec = []
	line = f.readline()
	first_review = json.loads(line)
	current_business_id = first_review['business_id']
	while line:
		review = json.loads(line)
		if review['business_id'] != current_business_id:
			p_with, p_without, p_with_type = adoption_prob(reviewer_vec, yelp)
			print ('p_with:', p_with, 'p_without:', p_without)
			p_with_vec.append(p_with)
			p_without_vec.append(p_without)
			if p_without != 0 and p_with != None:
				ratio_vec.append(p_with/p_without)
				weight_vec.append(len(reviewer_vec))
			reviewer_vec = []
			current_business_id = review['business_id']
		else:
			reviewer_vec.append(review['user_id'])
		line = f.readline()

	f.close()
	with open(output_filename, 'w') as output_file:
		json.dump({'ratio_vec': ratio_vec, 'weight_vec': weight_vec}, output_file)

def plot():
	data = json.load(open(output_filename))
	ratio_vec = data['ratio_vec']
	weight_vec = data['weight_vec']

	ratio_vec_new = []
	weight_vec_new = []
	for i in range(len(ratio_vec)):
		if ratio_vec[i] > 0:
			ratio_vec_new.append(ratio_vec[i])
			weight_vec_new.append(weight_vec[i])

	# the average
	print ('the average ratio:', np.average(ratio_vec)) #333.347197348
	print ('the weighted average ratio:', np.average(ratio_vec, weights=weight_vec)) #93.791749059

	# the histogram of the data
	fig = plt.figure()
	ax = fig.add_axes([0.19, 0.15, 0.74, 0.8])
	n, bins, patches = ax.hist(ratio_vec_new, 50, range=[0, 300], normed=1, facecolor='black', alpha=0.5, weights=weight_vec_new)
	plt.xlabel('improvement ratio of rec. prob. (receiver)')
	plt.ylabel('frequency density')
	#plt.title('the improvement of reviewing probability by recommendations')
	plt.savefig('images/improvement_ratio.eps', format='eps', dpi=1000)

	plt.show()

if __name__ == '__main__':
	#calculate()
	plot()