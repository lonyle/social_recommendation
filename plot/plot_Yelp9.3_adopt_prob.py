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

result = json.load(open('data/result_exp9.3_Yelp.json'))

adopt_prob_vec = [0.08, 0.2, 0.4]#[str(x*0.2) for x in result['param_vec']]

# 4 bars, for 4 different algorithms
N_delta = len(adopt_prob_vec)
N_algorithm = 5

ind = np.arange(N_delta)
width = 1/(N_algorithm+2)

# fig = plt.figure(figsize=(6.5,5))
# ax = fig.add_axes([0.13, 0.2, 0.83, 0.7])
fig = plt.figure(figsize=(4,3))
ax = fig.add_axes([0.18, 0.26, 0.8, 0.64])

if is_ImpRatio == False:
	rects0 = ax.bar(ind, result['baseline_profit_vec'], width, label='baseline', color='black',\
		fill=False, hatch='*')

ImpRatio_opt_fixed = ImpRatio(result['opt_fixed_vec'], result['baseline_profit_vec'])
rects1 = ax.bar(ind+width, ImpRatio_opt_fixed, width, label='opt. fixed', color='black',\
	fill=True)

ImpRatio_opt_mixed = ImpRatio(result['opt_mixed_vec'], result['baseline_profit_vec'])
rects2 = ax.bar(ind+2*width, ImpRatio_opt_mixed, width, label='opt. mixed', color='black',\
	fill=False)

# ImpRatio_q_learning = ImpRatio(result['q_learning_vec'], result['baseline_profit_vec'])
# rects3 = ax.bar(ind+3*width, ImpRatio_q_learning, width, label='q-learning', color='gray',\
# 	fill=True)

rect4 = ax.bar(ind+3*width, result['time_cutoff_vec'], width, label='reward \nthen stop', color='gray', \
	fill=True, hatch='x')

ImpRatio_degree_cutoff = ImpRatio(result['degree_cutoff_vec'], result['baseline_profit_vec'])
rects5 = ax.bar(ind+4*width, ImpRatio_degree_cutoff, width, label='degree', color='black',\
	fill=False, hatch='//')

# rects6 = ax.bar(ind+6*width, result['boosted_cutoff_vec'], width, label='boosted', color='black',\
# 	fill=False, hatch='-')

# rects7 = ax.bar(ind+7*width, result['influence_cutoff_vec'], width, label='influence', color='black',\
# 	fill=False, hatch='\\\\')

# plt.legend(loc='upper left', frameon=False, fontsize=18,  ncol=1, mode="expand")

plt.xlabel('adopt. prob. $a$', weight='bold')
plt.ylabel('profit', weight='bold')

ax.set_xticks(ind + 3.5*width)
ax.set_xticklabels(adopt_prob_vec, fontsize=22)

plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
# plt.ylim(0, 95000)
# plt.yticks([40000, 90000])

plt.savefig('images/plot_bar9.3_adopt_prob_Yelp.eps', dpi=1200)
plt.show()