import matplotlib.pyplot as plt 
import numpy as np 
import matplotlib
font = {'size': 24, 'weight':'bold'}
matplotlib.rc('font', **font)

import json

def plot_min_average_max():
	filename = 'data/result_exp9.7_compare_influence.json'
	data = json.load(open(filename))
	param_vec = data['param_vec']
	k_vec = data['k_vec']
	profit_vec_vec = data['profit_vec_vec']

	min_vec = []
	max_vec = []
	average_vec = []
	for profit_vec in profit_vec_vec:
		min_vec.append( min(profit_vec) )
		max_vec.append( max(profit_vec) )
		average_vec.append( np.average(profit_vec) )

	plt.axes([0.13, 0.2, 0.83, 0.7])

	plt.plot(param_vec, max_vec, color='black', label='optimal $k$', \
		linewidth=2, marker='o', markersize=10, fillstyle='none', markeredgewidth=2)
	max_ratio_vec = np.asarray(max_vec) / np.asarray(average_vec)
	i = 0
	print (param_vec, max_vec)
	#[0.01, 0.05, 0.1, 0.2, 0.3, 0.4] 
	#[279.0675, 416.9825, 461.48, 502.075, 539.4825, 579.23]
	for xy in zip([-0.02, 0.02, 0.08, 0.18, 0.28, 0.38], 
				  [330.0675, 440.9825, 490.48, 532.075, 569.4825, 609.23]):
		plt.annotate('%.0f'%(max_ratio_vec[i]*100-100)+'%', xy=xy, fontsize=20)
		i += 1

	plt.plot(param_vec, average_vec, color='black', label='random $k$', \
		linewidth=2)

	plt.plot(param_vec, min_vec, color='black', label='worst $k$', \
		linewidth=2, marker='x', markersize=10, fillstyle='none', markeredgewidth=2)
	min_ratio_vec = np.asarray(min_vec) / np.asarray(average_vec)
	i = 0
	print (param_vec, min_vec) 
	# [0.01, 0.05, 0.1, 0.2, 0.3, 0.4] 
	# [48.6625, 197.4425, 304.215, 415.3525, 461.1575, 475.01]
	for xy in zip([-0.01, 0.048, 0.09, 0.165, 0.26, 0.355],
				  [-20, 145.4425, 240.215, 340.3525, 390.1575, 405.01]):
		plt.annotate('%.0f'%(min_ratio_vec[i]*100-100)+'%', xy=xy, fontsize=20)
		i += 1

	plt.ticklabel_format(style='sci', axis='y', scilimits=(2,2))
	plt.xlabel('informed prob. $\\delta$', weight='bold')
	plt.ylabel('profit', weight='bold')
	plt.legend(loc='lower right', fontsize=20, frameon=False)

	plt.text(0.02, 680, '\"71%\": improvement ratio\n compared to random $k$', fontsize=20)#transform=ax.transAxes)

	plt.ylim(-30, 850)
	plt.xlim(-0.02, 0.42)

	plt.savefig('images/plot_9.7_compare_influence_k.eps', dpi=1200)
	plt.show()

if __name__ == '__main__':
	plot_min_average_max()