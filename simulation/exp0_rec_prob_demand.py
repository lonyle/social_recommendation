# Exp 0: rec prob and demand

import estimation
import estimation_uniform
import setting
import numpy as np
import json

from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

import matplotlib.pyplot as plt
import matplotlib
font = {'size'   : 24, 'weight': 'bold'}
matplotlib.rc('font', **font)

linestyle_dict = {
    'solid':              (0, ()),
    'densely dotted':      (0, (1, 1)),
    'dashed':             (0, (5, 5)),
    'dashdotted':          (0, (3, 5, 1, 5)),
    'loosely dashdotted':  (0, (3, 10, 1, 10)),
    'densely dashdotted':  (0, (3, 1, 1, 1)),
    'densely dashdotted':  (0, (3, 1, 1, 1))
}


Types = setting.Types
N_node_type = setting.N_node_type
scale_rec_prob = setting.occupation_scale['large']/setting.occupation_scale['small']

tmp_filename = 'data/result_rec_prob_and_demand.json'

def get_demand(other_info_prob, recommend_prob_OthInf, recommend_prob_FriRec):
	if setting.UNIFORM == True:
		prob_FriRec, prob_OthInf = estimation_uniform.estimate_informed_prob(other_info_prob, recommend_prob_OthInf, recommend_prob_FriRec)
	else: # mongodb version, slower
		prob_FriRec, prob_OthInf = estimation.estimate_informed_prob(other_info_prob, recommend_prob_OthInf, recommend_prob_FriRec)

	adopt_prob_OthInf = {'zero': 1, 'small': 1, 'large': 1}
	adopt_prob_FriRec = {'zero': 1, 'small': 1, 'large': 1}

	N_adoption = 0
	for Type in Types:
		N_adoption += (prob_OthInf[Type] * adopt_prob_OthInf[Type] + prob_FriRec[Type] * adopt_prob_FriRec[Type]) \
			* N_node_type[Type]

	# consider the users with degree zero
	N_adoption += adopt_prob_OthInf['zero'] * N_node_type['zero']

	return N_adoption

def rec_prob_and_demand():
	other_info_prob_vec = [0.0001, 0.001, 0.01, 0.1]
	rec_prob_vec = list( np.linspace(0.001, 0.04, 15) ) + list( np.linspace(0.05, 0.9, 21) )

	results = {}

	for other_info_prob in other_info_prob_vec:
		########################
		# !!!!! reset the global variable when changing other_info_prob
		setting.informed_prob_average = None
		########################

		demand_vec = []
		for rec_prob in rec_prob_vec:
			recommend_prob_FriRec = {'zero':0, 'small':rec_prob, 'large':rec_prob*scale_rec_prob}
			recommend_prob_OthInf = recommend_prob_FriRec
			demand = get_demand(other_info_prob, recommend_prob_OthInf, recommend_prob_FriRec)
			print ('the demand is:', demand)
			demand_vec.append(demand)

		results[other_info_prob] = {'rec_prob_vec': rec_prob_vec, 'demand_vec': demand_vec}

	with open(tmp_filename, 'w') as output_file:
		json.dump(results, output_file, indent=4)

def plot():
	results = json.load(open(tmp_filename))

	other_info_prob_vec = [0.0001, 0.001, 0.01, 0.1]
	markers = ['o', 'x', 'D', '^']
	linestyle_vec = ['solid', 'densely dotted', 'dashed', 'dashdotted']
	marker_idx = 0

	fig = plt.figure()#plt.subplots()
	ax = fig.add_axes([0.17, 0.2, 0.78, 0.7])

	axins = zoomed_inset_axes(ax, 7, loc=4,\
		bbox_to_anchor=(0.68,0.07,.3,.3), bbox_transform=ax.transAxes) # zoom-factor: 2.5, location: upper-left
	
	for other_info_prob in other_info_prob_vec:
		data = results[str(other_info_prob)]

		rec_prob_vec = data['rec_prob_vec']
		demand_vec = data['demand_vec']

		ax.plot(rec_prob_vec, demand_vec, color='black', label='$\\delta=$'+str(other_info_prob),\
			linestyle=linestyle_dict[linestyle_vec[marker_idx]], linewidth=3)
			#marker=markers[marker_idx],\
			#markersize=10, fillstyle='none', markeredgewidth=3)

		axins.plot(rec_prob_vec, demand_vec, color='black', \
			linestyle=linestyle_dict[linestyle_vec[marker_idx]], linewidth=3)
			#marker=markers[marker_idx],\
			#markersize=10, fillstyle='none', markeredgewidth=3)

		marker_idx += 1

	ax.legend(loc='upper left', fontsize=20, frameon=False)

	axins.set_xlim(-0.01, 0.06) # apply the x-limits
	axins.set_ylim(560000, 600000) # apply the y-limits

	mark_inset(ax, axins, loc1=2, loc2=3, fc="none", ec="0.5")

	plt.yticks(visible=False)
	#plt.xticks(visible=False)
	ax.set_ylim(550000, 1500000)

	ax.ticklabel_format(axis='y',style='sci',scilimits=(0,3))
	ax.set_xlabel('rec. prob. $q_i$ (for degree<500)', weight='bold')
	ax.set_ylabel('demand $D_i$', weight='bold')
	#plt.draw()

	plt.savefig('images/rec_prob_and_demand.eps', dpi=1200)

	plt.show()

if __name__ == '__main__':
	#rec_prob_and_demand()
	plot()