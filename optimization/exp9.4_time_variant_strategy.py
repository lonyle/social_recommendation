''' comparing the optimal strategies at different time points
	for different parameter settings, e.g. delta
'''

import time_variant_mixed
import utils
import json

MAX_LEN = 50

N_iteration = 50
sum_improvement_vec = [0] * MAX_LEN
count_improvement_vec = [0] * MAX_LEN

delta = utils.true_delta
rec_prob_func = utils.true_rec_prob_func
adopt_prob_func = utils.true_adopt_prob_func

for ite in range(N_iteration):
	profit, improvement_vec = time_variant_mixed.run_epoches(200, \
		delta, rec_prob_func, adopt_prob_func)
	for idx in range(len(improvement_vec)):
		sum_improvement_vec[idx] += improvement_vec[idx]
		count_improvement_vec[idx] += 1

ave_improvement_vec = []
for i in range(MAX_LEN):
	if count_improvement_vec[i] == 0:
		break
	ave_improvement_vec.append(sum_improvement_vec[i] / count_improvement_vec[i])

with open('data/result_exp9.4.json', 'w') as output_file:
	json.dump(ave_improvement_vec, output_file, indent=4)