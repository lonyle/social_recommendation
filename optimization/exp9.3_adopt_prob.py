''' 
	decide the scale of the adoption probability
'''
import math
import exp_utils
import utils

# is_TS = True
# utils.graph_name = 'Facebook'

parser = argparse.ArgumentParser(description = 'experiments on optimization')
parser.add_argument('--graph_name', action = 'store', required = True, type = str, \
	help = 'the name of the graph: Facebook or Yelp')
parser.add_argument('--enable_PSRL', dest='is_PSRL', action='store_true')
args = parser.parse_args()
utils.graph_name = args.graph_name
is_TS = args.is_PSRL # posterior sampling is also known as thompson sampling

def adopt_prob_func_gen(scalar):
	def adopt_prob_func(price, reward):
		return 0.2 * scalar
	return adopt_prob_func



if __name__ == '__main__':
	exp_runner = exp_utils.Exp()

	if utils.graph_name == 'Facebook':
		scalar_vec = [0.2, 0.5, 1, 2]
	else:
		scalar_vec = [0.5, 1, 2]

	if is_TS:
		scalar_vec = [0.5, 1, 2]

	delta = 0.1
	rec_prob_func = utils.true_rec_prob_func
	for scalar in scalar_vec:
		print ('scalar:', scalar)
		adopt_prob_func = adopt_prob_func_gen(scalar)
		if is_TS:
			exp_runner.run_experiments_TS(delta, rec_prob_func, adopt_prob_func)
		else:
			exp_runner.run_experiments(delta, rec_prob_func, adopt_prob_func)
			#exp_runner.run_extra_experiments(delta, rec_prob_func, adopt_prob_func)

		exp_runner.param_vec.append(scalar)

	if is_TS:
		exp_runner.dump_to_file_TS('data/result_exp9.3_TS.json')
	else:
		if utils.graph_name == 'Yelp':
			exp_runner.dump_to_file('data/result_exp9.3_Yelp.json')
		else:
			exp_runner.dump_to_file('data/result_exp9.3.json')