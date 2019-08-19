''' the experiment is to test the performance of thompson sampling under different delta
	this is to test whether the TS algorithm can do dynamic decisions based on the status of diffusion.
'''
import logging
import utils

import argparse
import exp_utils

# utils.graph_name = 'Facebook'
# is_TS = True
# utils.graph_name = 'Yelp'
# is_TS = False
parser = argparse.ArgumentParser(description = 'experiments on optimization')
parser.add_argument('--graph_name', action = 'store', required = True, type = str, \
	help = 'the name of the graph: Facebook or Yelp')
parser.add_argument('--enable_PSRL', dest='is_PSRL', action='store_true')
args = parser.parse_args()
utils.graph_name = args.graph_name
is_TS = args.is_PSRL # posterior sampling is also known as thompson sampling

if utils.graph_name == 'Yelp':
	delta_vec = [0.01, 0.05, 0.1] 
elif utils.graph_name == 'Facebook':
	delta_vec = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4]

rec_prob_func = utils.true_rec_prob_func
adopt_prob_func = utils.true_adopt_prob_func

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('exp9.1-initial-prob')


if is_TS == True:
	delta_vec = [0.05, 0.1, 0.2]

if __name__ == '__main__':
	exp_runner = exp_utils.Exp()

	for delta in delta_vec:
		logger.info('delta: %f'%(delta))
		if is_TS:
			exp_runner.run_experiments_TS(delta, rec_prob_func, adopt_prob_func)

		else:
			exp_runner.run_experiments(delta, rec_prob_func, adopt_prob_func)
			#exp_runner.run_extra_experiments(delta, rec_prob_func, adopt_prob_func)

		exp_runner.param_vec.append(delta)

	if is_TS:
		exp_runner.dump_to_file_TS('data/result_exp9.1_TS.json')		
	else: # not thompson sampling
		if utils.graph_name == 'Yelp':
			exp_runner.dump_to_file('data/result_exp9.1_Yelp.json')
		else:
			exp_runner.dump_to_file('data/result_exp9.1.json')




