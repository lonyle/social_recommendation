import matplotlib.pyplot as plt 
import numpy as np 
import matplotlib
font = {'size': 20}
matplotlib.rc('font', **font)

import json

tmp_filename = 'data/result_effectiveness_reward_profit.json'

results = json.load(open(tmp_filename))

for scale in results['scale_vec']:
	result = results[str(scale)]
	plt.plot(result['reward_vec'], result['profit_vec'], label='scale='+str(scale))

plt.legend()

plt.xlabel('reward $r$')
plt.ylabel('profit')

plt.savefig('images/impact_effectiveness_reward.eps', dpi=1200)

plt.show()