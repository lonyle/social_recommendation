import matplotlib.pyplot as plt 
import numpy as np 
import matplotlib
font = {'size': 20}
matplotlib.rc('font', **font)

stars_vec = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
checkin_count_noreward = [2.725628584,16.35011136,24.45824591,50.18925234,100.2736295,119.0688066,152.4455154,85.13050548,11.65770863]
checkin_count_reward = [4.023809524,13.67307692,49.112,68.02734375,167.8842975,217.7891832,327.8926282,187.98941,31.72911392]

fig = plt.figure()
ax = fig.add_axes([0.16, 0.15, 0.81, 0.8])

ind = np.asarray(stars_vec)
width = 0.15

rects1 = ax.bar(ind, checkin_count_noreward, width, color='black', fill=False, hatch='/')
rects2 = ax.bar(ind+width, checkin_count_reward, width, color='black')


ax.legend( (rects1[0], rects2[0]), ('no check-in offer', 'with check-in offer'), loc='upper left', fontsize=20, frameon=False)

ax.set_xticks(ind + width)
ax.set_xticklabels( stars_vec )

plt.ylabel('average number of check-in')
plt.xlabel('rating score')
plt.savefig('images/checkin_offer_and_count.eps', dpi=1200)

plt.show()

