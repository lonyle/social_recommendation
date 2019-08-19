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

result = json.load(open('data/result_exp9.3.json'))

delta_vec = result['param_vec']

# 4 bars, for 4 different algorithms
N_delta = len(delta_vec)
N_algorithm = len(result) - 1

ind = np.arange(N_delta)
width = 1/(N_algorithm+2)

fig = plt.figure()
ax = fig.add_axes([0.13, 0.2, 0.83, 0.7])


rects3 = ax.bar(ind+1*width, result['influence_cutoff_vec'], width, \
	label='influence', color='black',\
	fill=False, hatch='-')

rects2 = ax.bar(ind+2*width, result['time_cutoff_vec'], width, \
	label='time cutoff', color='black',\
	fill=False, hatch='=')

rects3 = ax.bar(ind+3*width, result['boosted_cutoff_vec'], width, \
	label='boosted', color='black',\
	)



plt.legend(loc='upper left', frameon=False, fontsize=18,  ncol=1, mode="expand")

plt.xlabel('initial informed prob. $\\delta$', weight='bold')
plt.ylabel('profit', weight='bold')

ax.set_xticks(ind + 2*width)
ax.set_xticklabels(delta_vec, fontsize=22)

plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
plt.ylim(0, 3200)

plt.savefig('images/plot_extra_9.3_initial_prob.eps', dpi=1200)
#plt.show()