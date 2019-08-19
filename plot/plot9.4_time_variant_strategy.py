import matplotlib.pyplot as plt
import numpy as np
import json
import matplotlib
font = {'size': 24, 'weight':'bold'}
matplotlib.rc('font', **font)

#improvement_vec = [0, 1.5924999999999727, 0.0, 0.0, 1.1924999999999955, 2.1724999999999994, 0.14999999999999947]
improvement_vec = json.load(open('data/result_exp9.4.json'))

profit_opt_mixed = 435.7

improvement_vec = [x/profit_opt_mixed for x in improvement_vec]

x_vec = np.arange(len(improvement_vec)) * 500

fig = plt.figure()
ax = fig.add_axes([0.2, 0.2, 0.75, 0.75])

ax.bar(x_vec, improvement_vec, width=200, fill=False, hatch='//', color='black')
plt.xlabel('num. of arrived users', weight = 'bold')
plt.xticks(fontsize=20)
plt.ylabel('Improvement ratio', weight = 'bold')
plt.yticks(fontsize=20)

# manipulate
vals = ax.get_yticks()
ax.set_yticklabels(['{:,.1%}'.format(x) for x in vals])

plt.savefig('images/plot9.4_time_variant_strategy.eps', dpi=1200)
plt.show()