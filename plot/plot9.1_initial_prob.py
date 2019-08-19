import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import json

import sys
sys.path.insert(1, 'optimization')
import utils

font = {'size': 24, 'weight': 'bold'}
matplotlib.rc('font', **font)
#matplotlib.rcParams['hatch.linewidth'] = 2 

is_ImpRatio = False

def ImpRatio(vec1, vec2):
	if is_ImpRatio:
		ratio_vec = []
		for i in range(len(vec1)):
			ratio = max(0, vec1[i]/vec2[i] - 1)
			ratio_vec.append(ratio)
	else:
		ratio_vec = vec1
	return ratio_vec

result = json.load(open('data/result_exp9.1.json'))

delta_vec = result['param_vec']

# 4 bars, for 4 different algorithms
N_delta = len(delta_vec)
N_algorithm = len(result) - 2

ind = np.arange(N_delta)
width = 1/(N_algorithm+2)

fig = plt.figure(figsize=(8,4))
ax = fig.add_axes([0.13, 0.2, 0.83, 0.7])

if is_ImpRatio == False:
	rects0 = ax.bar(ind, result['baseline_profit_vec'], width, label='baseline', color='black',\
		fill=False, hatch='*')

ImpRatio_opt_fixed = ImpRatio(result['opt_fixed_vec'], result['baseline_profit_vec'])
rects1 = ax.bar(ind+width, ImpRatio_opt_fixed, width, label='opt. fixed', color='black',\
	fill=True)

ImpRatio_opt_mixed = ImpRatio(result['opt_mixed_vec'], result['baseline_profit_vec'])
rects2 = ax.bar(ind+2*width, ImpRatio_opt_mixed, width, label='opt. mixed', color='black',\
	fill=False)

ImpRatio_q_learning = ImpRatio(result['q_learning_vec'], result['baseline_profit_vec'])
rects3 = ax.bar(ind+3*width, ImpRatio_q_learning, width, label='q-learning', color='gray',\
	fill=True)

rect4 = ax.bar(ind+4*width, result['time_cutoff_vec'], width, label='reward then stop', color='gray', \
	fill=True, hatch='x', edgecolor='black')

ImpRatio_degree_cutoff = ImpRatio(result['degree_cutoff_vec'], result['baseline_profit_vec'])
rects5 = ax.bar(ind+5*width, ImpRatio_degree_cutoff, width, label='degree', color='black',\
	fill=False, hatch='//')

# rects6 = ax.bar(ind+6*width, result['boosted_cutoff_vec'], width, label='boosted', color='black',\
# 	fill=False, hatch='-')

rects7 = ax.bar(ind+6*width, result['influence_cutoff_vec'], width, label='influence', color='black',\
	fill=False, hatch='\\\\')

#plt.legend(loc='upper left', frameon=False, fontsize=16,  ncol=2, mode="expand")

plt.xlabel('informed prob. $\\delta$ from other sources', weight='bold')
plt.ylabel('profit', weight='bold')

ax.set_xticks(ind + 3.5*width)
ax.set_xticklabels(delta_vec, fontsize=22)

plt.ticklabel_format(style='sci', axis='y', scilimits=(1,0))
if utils.graph_name == 'Yelp':
	plt.ylim(0, 80000)
else:
	plt.ylim(0, 600)

output_filename = 'images/plot_bar9.1_initial_prob_' + utils.graph_name + '.eps'
plt.savefig(output_filename, dpi=1200)
plt.show()