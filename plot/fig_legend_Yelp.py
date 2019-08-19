import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import json

import sys
sys.path.insert(1, 'optimization')
import utils
import pylab

font = {'size': 24, 'weight': 'bold'}
matplotlib.rc('font', **font)

###########################################################3
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

result = json.load(open('data/result_exp9.1_Yelp.json'))

rec_prob_vec = [0.04, 0.1, 0.2]#[str(x*0.2) for x in result['param_vec']]

# 4 bars, for 4 different algorithms
N_delta = len(rec_prob_vec)
N_algorithm = 5

ind = np.arange(N_delta)
width = 1/(N_algorithm+2)

fig = plt.figure(figsize=(4,3))
ax = fig.add_axes([0.18, 0.26, 0.8, 0.64])

if is_ImpRatio == False:
	rects0 = ax.bar(ind, result['baseline_profit_vec'], width, label='baseline', color='black',\
		fill=False, hatch='*')

ImpRatio_opt_fixed = ImpRatio(result['opt_fixed_vec'], result['baseline_profit_vec'])
rects1 = ax.bar(ind+width, ImpRatio_opt_fixed, width, label='opt. fixed', color='black',\
	fill=True)

ImpRatio_opt_mixed = ImpRatio(result['opt_mixed_vec'], result['baseline_profit_vec'])
rects2 = ax.bar(ind+2*width, ImpRatio_opt_mixed, width, label='opt. randomized', color='black',\
	fill=False)

# ImpRatio_q_learning = ImpRatio(result['q_learning_vec'], result['baseline_profit_vec'])
# rects3 = ax.bar(ind+3*width, ImpRatio_q_learning, width, label='q-learning', color='gray',\
# 	fill=True)

rect4 = ax.bar(ind+3*width, result['time_cutoff_vec'], width, label='reward then stop', color='gray', \
	fill=True, hatch='x')

ImpRatio_degree_cutoff = ImpRatio(result['degree_cutoff_vec'], result['baseline_profit_vec'])
rects5 = ax.bar(ind+4*width, ImpRatio_degree_cutoff, width, label='degree', color='black',\
	fill=False, hatch='//')
###########################################################


figLegend = pylab.figure(figsize=(8, 0.9))
pylab.figlegend(*ax.get_legend_handles_labels(), loc='upper left',\
frameon=False, fontsize=18, ncol=3, mode='expand')

output_filename = 'images/plot_legend_' + 'Yelp' + '.eps'
figLegend.savefig(output_filename, dpi=1200)
figLegend.show()