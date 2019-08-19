import matplotlib.pyplot as plt 
import numpy as np 
import matplotlib
font = {'size': 24, 'weight': 'bold'}
matplotlib.rc('font', **font)


category_vec = ['Arts & Crafts', 'Hair Salon', 'Massage Therapy', 'Education', 'Battery Stores', 'Men\'s Hair Salons', 'Casinos', 'Eyewear']
ratio_vec = [2489, 1002, 1233, 1039,  36, 200, 192, 173]

fig = plt.figure()
ax = fig.add_axes([0.22, 0.32, 0.74, 0.63])

ind = np.arange(8)
width = 0.5

rects1 = ax.bar(ind[:4], ratio_vec[:4], color='black', fill=False, hatch='/')
rects2 = ax.bar(ind[4:], ratio_vec[4:], color='black')

ax.legend( (rects1[0], rects2[0]), ('low perceivability', 'high perceivablity'), loc='upper right', fontsize=20, frameon=False)

ax.set_xticks([-1.3, 0, 0.1, 2, 2.6, 3.2, 5.2, 6.2])
ax.set_xticklabels(category_vec, rotation=30, fontsize=18)
plt.xlim(-1, 8)
plt.ylabel('improvement ratio', weight='bold')
plt.savefig('images/category_improvement_ratio.eps', dpi=1200)
plt.show()