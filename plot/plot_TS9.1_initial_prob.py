import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import json

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

result = json.load(open('data/result_exp9.1.json'))
result_TS = json.load(open('data/result_exp9.1_TS.json'))

for key in result:
	result[key] = result[key][1:4]

# for key in result_TS:
# 	result_TS[key] = result_TS[key][1:4]

delta_vec = result_TS['param_vec']

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

rects3 = ax.bar(ind+1*width, result['opt_mixed_vec'], width, label='opt. \nrandom', \
	fill=False)

rects2 = ax.bar(ind+2*width, result_TS['TS_mixed_vec'], width, label='mixed(PSRL)', color='black',\
	fill=False, hatch='/')

rects3 = ax.bar(ind+3*width, result_TS['TS_q_learning_vec'], width, label='q-learning(PSRL)',\
	color='gray', fill=True, hatch='/')

rects4 = ax.bar(ind+4*width, result_TS['TS_influence_vec'], width, label='influence(PSRL)',\
	fill=False, hatch='\\')


#plt.legend(loc='upper left', frameon=False, fontsize=18,  ncol=2, mode="expand")

plt.xlabel('informed prob. $\\delta$', weight='bold')
plt.ylabel('profit', weight='bold')

ax.set_xticks(ind + 2*width)
ax.set_xticklabels(delta_vec, fontsize=22)

plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
#plt.ylim(0, 800)
plt.yticks([0, 200, 400])

plt.savefig('images/plot_TS_9.1_initial_prob.eps', dpi=1200)
plt.show()