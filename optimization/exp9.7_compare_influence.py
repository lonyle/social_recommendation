''' this experiment is to compare the performance of influence algorithms under different values of k
'''

import logging
import utils
import exp_utils
import json

output_filename = 'data/result_exp9.7_compare_influence.json'

utils.graph_name = 'Facebook'
is_TS = False

if utils.graph_name == 'Yelp':
	delta_vec = [0.01, 0.05, 0.1] 
elif utils.graph_name == 'Facebook':
	delta_vec = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4]

rec_prob_func = utils.true_rec_prob_func
adopt_prob_func = utils.true_adopt_prob_func

logger = logging.getLogger('exp9.7-compare-influence')

if __name__ == '__main__':
	exp_runner = exp_utils.Exp()
	profit_vec_vec = []
	for delta in delta_vec:
		logger.info('delta: %f'%(delta))
		profit_vec, k_vec = exp_runner.influence_different_k(delta, rec_prob_func, adopt_prob_func)
		print (profit_vec, k_vec)
		profit_vec_vec.append(profit_vec)

	result = {
		'profit_vec_vec': profit_vec_vec,
		'k_vec': list(k_vec),
		'param_vec': delta_vec
	}
	with open(output_filename, 'w') as output_file:
		json.dump(result, output_file, indent=4)

