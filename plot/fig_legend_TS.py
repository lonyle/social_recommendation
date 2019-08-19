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

###########################################################
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
result_TS = json.load(open('data/result_exp9.1_TS.json'))

for key in result:
	result[key] = result[key][1:4]

delta_vec = result['param_vec']

# 4 bars, for 4 different algorithms
N_delta = len(delta_vec)
N_algorithm = 5

ind = np.arange(N_delta)
width = 1/(N_algorithm+2)

fig = plt.figure(figsize=(4,3))
ax = fig.add_axes([0.18, 0.26, 0.8, 0.64])


rects0 = ax.bar(ind, result['baseline_profit_vec'], width, label='baseline', color='black',\
	fill=False, hatch='*')

# ImpRatio_opt_fixed = ImpRatio(result['opt_fixed_vec'], result['baseline_profit_vec'])
# rects1 = ax.bar(ind+width, ImpRatio_opt_fixed, width, label='opt. fixed', color='black',\
# 	fill=False, hatch='//')

rects3 = ax.bar(ind+1*width, result['opt_mixed_vec'], width, label='opt. randomized', \
	fill=False)

rects2 = ax.bar(ind+2*width, result_TS['TS_mixed_vec'], width, label='randomized(PSRL)', color='black',\
	fill=False, hatch='/')

rects3 = ax.bar(ind+3*width, result_TS['TS_q_learning_vec'], width, label='q-learning(PSRL)',\
	color='gray', fill=True, hatch='/')

rects4 = ax.bar(ind+4*width, result_TS['TS_influence_vec'], width, label='           ',\
	fill=False, hatch='\\')
###########################################################



figLegend = pylab.figure(figsize=(9.8, 0.9))
pylab.figlegend(*ax.get_legend_handles_labels(), loc='upper left',\
frameon=False, fontsize=18, ncol=3, mode=None)

figLegend.text(0.84, 0.22, 'influence\n(PSRL)', fontsize=18)

output_filename = 'images/plot_legend_' + 'TS' + '.eps'
figLegend.savefig(output_filename, dpi=1200)
figLegend.show()