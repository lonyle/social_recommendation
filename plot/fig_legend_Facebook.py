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

result = json.load(open('data_share/result_exp9.1.json'))

delta_vec = result['param_vec']

# 4 bars, for 4 different algorithms
N_delta = len(delta_vec)
N_algorithm = len(result) - 1

ind = np.arange(N_delta)
width = 1/(N_algorithm+2)

fig = pylab.figure(figsize=(16,0.5))
ax = pylab.gca()

if is_ImpRatio == False:
	rects0 = ax.bar(ind, result['baseline_profit_vec'], width, label='baseline', color='black',\
		fill=False, hatch='*')

ImpRatio_opt_fixed = ImpRatio(result['opt_fixed_vec'], result['baseline_profit_vec'])
rects1 = ax.bar(ind+width, ImpRatio_opt_fixed, width, label='opt. fixed', color='black',\
	fill=True)

ImpRatio_opt_mixed = ImpRatio(result['opt_mixed_vec'], result['baseline_profit_vec'])
rects2 = ax.bar(ind+2*width, ImpRatio_opt_mixed, width, label='opt. randomized', color='black',\
	fill=False)

ImpRatio_q_learning = ImpRatio(result['q_learning_vec'], result['baseline_profit_vec'])
rects3 = ax.bar(ind+3*width, ImpRatio_q_learning, width, label='q-learning', color='gray',\
	fill=True)

rect4 = ax.bar(ind+4*width, result['time_cutoff_vec'], width, label='reward then stop', color='gray', \
	fill=True, hatch='x')

ImpRatio_degree_cutoff = ImpRatio(result['degree_cutoff_vec'], result['baseline_profit_vec'])
rects5 = ax.bar(ind+5*width, ImpRatio_degree_cutoff, width, label='degree', color='black',\
	fill=False, hatch='//')

# rects6 = ax.bar(ind+6*width, result['boosted_cutoff_vec'], width, label='boosted', color='black',\
# 	fill=False, hatch='-')

rects7 = ax.bar(ind+7*width, result['influence_cutoff_vec'], width, label='influence', color='black',\
	fill=False, hatch='\\\\')

#plt.legend(loc='upper left', frameon=False, fontsize=16,  ncol=2, mode="expand")
figLegend = pylab.figure(figsize=(18, 0.5))
pylab.figlegend(*ax.get_legend_handles_labels(), loc='upper left',\
frameon=False, fontsize=18, ncol=7, mode='expand')

output_filename = 'images/plot_legend_' + 'Facebook' + '.eps'
figLegend.savefig(output_filename, dpi=1200)
figLegend.show()


