import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import json

import sys
sys.path.insert(1, 'optimization')
import utils

font = {'size': 24, 'weight': 'bold'}
matplotlib.rc('font', **font)

result = json.load(open('data/result_exp9.0_all.json'))

import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import json

import sys
sys.path.insert(1, 'optimization')
import utils

font = {'size': 24, 'weight': 'bold'}
matplotlib.rc('font', **font)

# only select the results for 0.3, 0.5, and 0.7
for key in result:
	result[key] = result[key][1:4]

reward_vec = result['param_vec']

# 4 bars, for 4 different algorithms
N_delta = len(reward_vec)
N_algorithm = len(result) - 2

ind = np.arange(N_delta)
width = 1/(N_algorithm+2)
print (N_algorithm, width)

fig = plt.figure(figsize=(5,4))
ax = fig.add_axes([0.15, 0.2, 0.83, 0.7])

print (result['opt_fixed_vec'])

rects0 = ax.bar(ind, result['baseline_profit_vec'], width, label='baseline', color='black',\
	fill=False, hatch='*')

rects1 = ax.bar(ind+width, result['opt_fixed_vec'], width, label='opt. fixed', color='black',\
	fill=True)

rects2 = ax.bar(ind+2*width, result['opt_mixed_vec'], width, label='opt. mixed', color='black',\
	fill=False)

rects3 = ax.bar(ind+3*width, result['q_learning_vec'], width, label='q-learning', color='gray',\
	fill=True)

rect4 = ax.bar(ind+4*width, result['time_cutoff_vec'], width, label='reward then stop', color='gray', \
	fill=True, hatch='x', edgecolor='black')

rects5 = ax.bar(ind+5*width, result['degree_cutoff_vec'], width, label='degree', color='black',\
	fill=False, hatch='//')

# rects6 = ax.bar(ind+6*width, result['boosted_cutoff_vec'], width, label='boosted', color='black',\
# 	fill=False, hatch='-')

rects7 = ax.bar(ind+6*width, result['influence_cutoff_vec'], width, label='influence', color='black',\
	fill=False, hatch='\\\\')

plt.xlabel('preferred reward $r$', weight='bold')
plt.ylabel('profit', weight='bold')

ax.set_xticks(ind + 3.5*width)
ax.set_xticklabels(reward_vec, fontsize=22)

plt.ticklabel_format(style='sci', axis='y', scilimits=(1,0))
if utils.graph_name == 'Yelp':
	plt.ylim(0, 80000)
else:
	plt.ylim(0, 600)

output_filename = 'images/plot_bar9.0_reward_' + utils.graph_name + '.eps'
plt.savefig(output_filename, dpi=1200)
plt.show()
