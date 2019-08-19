# the estimated profit of firms, the strategies of firms
import setting
import estimation
import estimation_uniform

Types = setting.Types
N_node_type = setting.N_node_type

'''
input: 
	1. price and reward
	2. the diffusion params given the reward and price
	3. the adoption params given the reward and price
output:
	1. the estimated profit
'''
def get_estimated_profit(price, reward,	cost, other_info_prob, recommend_prob_OthInf, recommend_prob_FriRec, adopt_prob_OthInf, adopt_prob_FriRec):
	# uniform, fast version
	if setting.UNIFORM == True:
		prob_FriRec, prob_OthInf = estimation_uniform.estimate_informed_prob(other_info_prob, recommend_prob_OthInf, recommend_prob_FriRec)
	else: # mongodb version, slower
		prob_FriRec, prob_OthInf = estimation.estimate_informed_prob(other_info_prob, recommend_prob_OthInf, recommend_prob_FriRec)

	N_adoption = 0
	for Type in Types:
		N_adoption += (prob_OthInf[Type] * adopt_prob_OthInf[Type] + prob_FriRec[Type] * adopt_prob_FriRec[Type]) \
			* N_node_type[Type]

	# consider the users with degree zero
	#N_adoption += adopt_prob_OthInf['zero'] * N_node_type['zero']

	N_recommendation = 0
	for Type in Types:
		N_recommendation += (prob_OthInf[Type] * recommend_prob_OthInf[Type] + prob_FriRec[Type] * recommend_prob_FriRec[Type]) \
			* N_node_type[Type]

	profit = N_adoption * (price - cost) - N_recommendation * reward
	return profit, N_recommendation, N_adoption


if __name__ == '__main__':
	opt_reward, opt_profit = opt_strategy(without_prob, with_prob, with_prob_type)
	print ('opt_reward:', opt_reward, 'opt_profit:', opt_profit)