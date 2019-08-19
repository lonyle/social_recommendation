''' change the amount of reward, to see the improvement
'''

import logging
import utils

import exp_utils
import argparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('exp9.0-reward')

parser = argparse.ArgumentParser(description = 'experiments on optimization')
parser.add_argument('--graph_name', action = 'store', required = True, type = str, \
	help = 'the name of the graph: Facebook or Yelp')
parser.add_argument('--enable_PSRL', dest='is_PSRL', action='store_true')
args = parser.parse_args()
utils.graph_name = args.graph_name
is_TS = args.is_PSRL # posterior sampling is also known as thompson sampling

reward_vec = [0.9]

delta = utils.true_delta
adopt_prob_func = utils.true_adopt_prob_func
def rec_prob_func(price, reward):
	if reward > 0:
		return 0.2
	else:
		return 0.02


if __name__ == '__main__':
	exp_runner = exp_utils.Exp()
	for reward in reward_vec:
		logger.info('reward: %f'%(reward))

		actions = [{'reward': 0, 'price': 1}, {'reward': reward, 'price': 1}]
		utils.possible_reward = [0, reward]
		utils.possible_actions = actions[:]
		utils.mixed_actions = actions[:]

		if is_TS:
			exp_runner.run_experiments_TS(delta, rec_prob_func, adopt_prob_func)

		else:
			exp_runner.run_experiments(delta, rec_prob_func, adopt_prob_func)
			exp_runner.run_extra_experiments(delta, rec_prob_func, adopt_prob_func)

		exp_runner.param_vec.append(reward)

	if is_TS:
		exp_runner.dump_to_file_TS('data/result_exp9.0_TS.json')		
	else: # not thompson sampling
		if utils.graph_name == 'Yelp':
			exp_runner.dump_to_file('data/result_exp9.0_Yelp.json')
		else:
			exp_runner.dump_to_file('data/result_exp9.0.json')
