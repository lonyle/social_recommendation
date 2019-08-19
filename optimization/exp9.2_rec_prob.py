''' not only need to decide the initial rec_prob without reward
	also need to decide the shape of the function to represent the effect the reward
'''
import math
from scipy.stats import norm
import exp_utils
import utils
import argparse

# is_TS = True
# utils.graph_name = 'Facebook'
# utils.graph_name = 'Yelp'
# is_TS = False

parser = argparse.ArgumentParser(description = 'experiments on optimization')
parser.add_argument('--graph_name', action = 'store', required = True, type = str, \
	help = 'the name of the graph: Facebook or Yelp')
parser.add_argument('--enable_PSRL', dest='is_PSRL', action='store_true')

args = parser.parse_args()
utils.graph_name = args.graph_name
is_TS = args.is_PSRL # posterior sampling is also known as thompson sampling


def linear_rec_prob_func_gen(scalar):
	def rec_prob_func(price, reward):
		rec_prob = (0.02 + 0.36 * reward) * scalar
		return rec_prob
	return rec_prob_func

if __name__ == '__main__':
	''' first step: only consider two possible actions
		and set the scale of rec_prob, and the scale of adopt_prob
	'''
	exp_runner = exp_utils.Exp()

	if utils.graph_name == 'Facebook':
		scalar_vec = [0.2, 0.5, 1, 2]
	elif utils.graph_name == 'Yelp':
		scalar_vec = [0.2, 0.5, 1]

	if is_TS:
		scalar_vec = [0.2, 0.5, 1]

	delta = 0.1
	adopt_prob_func = utils.true_adopt_prob_func
	for scalar in scalar_vec:
		print ('scalar:', scalar)
		rec_prob_func = linear_rec_prob_func_gen(scalar)
		if is_TS:
			exp_runner.run_experiments_TS(delta, rec_prob_func, adopt_prob_func)
		else:
			exp_runner.run_experiments(delta, rec_prob_func, adopt_prob_func)
			exp_runner.run_extra_experiments(delta, rec_prob_func, adopt_prob_func)
			
		exp_runner.param_vec.append(scalar)

	if is_TS:
		exp_runner.dump_to_file_TS('data/result_exp9.2_TS.json')
	else:
		if utils.graph_name == 'Yelp':
			exp_runner.dump_to_file('data/result_exp9.2_Yelp.json')
		else:
			exp_runner.dump_to_file('data/result_exp9.2.json')
