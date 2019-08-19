import matplotlib.pyplot as plt 
import numpy as np 
import matplotlib
font = {'size': 24, 'weight': 'bold'}
matplotlib.rc('font', **font)

import json

fig = plt.figure()
ax = fig.add_axes([0.17, 0.2, 0.78, 0.7])
ax.ticklabel_format(axis='y', style='sci', scilimits=(-2, 2))

tmp_filename = 'data/result_cost_profit.json'

results = json.load(open(tmp_filename))


marker_vec = ['o', 'x', 'D']
marker_idx = 0
for cost in results['cost_vec']:
	result = results[str(cost)]
	ax.plot(result['reward_vec'], result['profit_vec'], color='black', label='cost='+str(cost), \
		linewidth=2, marker=marker_vec[marker_idx], markersize=10, fillstyle='none', markeredgewidth=2)
	marker_idx += 1

plt.legend(loc='lower left', fontsize=22, frameon=False)

plt.xlabel('the reward $r$', weight='bold')
plt.ylabel('profit', weight='bold')
plt.ylim(-20000, 33000)

plt.savefig('images/impact_cost.eps', dpi=1200)

plt.show()