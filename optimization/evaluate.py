import matplotlib.pyplot as plt


def evaluate_once(graph, get_decision, is_node_feature):
	current_state_param = (0, 0, 0, graph.N_other_info)

	graph.reset()

	action_seq = []

	while True:
		# edited on 2019-01-08, the decision is based on state and the arrival node
		selected_user = graph.node_arrival()
		degree = len(graph.edges[selected_user]) if selected_user != None else None
		node_feature = {'degree': degree, 'id': selected_user}
		##################################################

		if is_node_feature: # enable the firm to use node feature
			action = get_decision(current_state_param, node_feature)
		else:
			action = get_decision(current_state_param)
		action_seq.append(action)

		# edited on 2019-01-08
		graph.do_action(selected_user, action)
		##################################################

		current_state_param = graph.current_state_param()
		m, delta_m, n, delta_n = current_state_param

		if delta_m + delta_n == 0: # no more potential users to be informed
			break

	total_profit = graph.gross_profit - graph.cost_on_reward

	return total_profit, action_seq

def evaluate_average(graph, get_decision, num_sims, is_node_feature=False):
	total_profit_vec = []
	for n in range(num_sims):
		total_profit, action_seq = evaluate_once(graph, get_decision, is_node_feature)
		total_profit_vec.append(total_profit)

		if n == num_sims//2:
			price_seq = [action['price'] for action in action_seq]
			reward_seq = [action['reward'] for action in action_seq]
			plt.plot(price_seq, color='blue')
			plt.plot(reward_seq, color='red')
			#plt.show()

	plt.hist(total_profit_vec)
	#plt.show()

	return sum(total_profit_vec)/len(total_profit_vec)