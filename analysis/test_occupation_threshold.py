import sampling_size
import matplotlib.pyplot as plt
import numpy as np

import matplotlib
font = {'size'   : 18}
matplotlib.rc('font', **font)

if __name__ == '__main__':
	initial_prob = 0.0001
	occupation_prob_vec = np.linspace(0, 0.1, 201)
	informed_prob_vec = []
	for occupation_prob in occupation_prob_vec:
		informed_prob = sampling_size.get_expected_size(initial_prob, occupation_prob)
		informed_prob_vec.append(informed_prob)

	plt.plot(occupation_prob_vec, informed_prob_vec, color='black')
	plt.xlabel('recommendation probability')
	plt.ylabel('probability of being informed')
	plt.savefig('images/yelp_threshold_00001_part.eps', dpi=5000)
	plt.show()