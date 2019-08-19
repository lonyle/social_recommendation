p_receivers_vec = [
0.060315,
0.069167,
0.067703,
0.06562,
0.033508,
0.091738,
0.027809,
0.105702,
0.094402,
0.040576,
0.112817,
0.064785,
0.054602,
0.073965
]
click_rate_vec = [
0.24223,
0.196308,
0.130357,
0.112669,
0.032275,
0.142826,
0.089581,
0.088305,
0.087673,
0.069682,
0.054664,
0.052959,
0.041617,
0.052826
]
reward_vec = [
0,
0,
0,
0,
0.5,
0,
0,
0.2,
0,
0.2,
0.9,
0.2,
0.5,
0.2
]
# click_then_resend_ratio = [
# ]

from sklearn import linear_model
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib
font = {'size': 24, 'weight':'bold'}
matplotlib.rc('font', **font)
from matplotlib.lines import Line2D

regr = linear_model.LinearRegression()
X = np.c_[p_receivers_vec, reward_vec]
y = np.asarray(click_rate_vec)
regr.fit(X, y)
print ('>>> evaluating the model')
y_pred = regr.predict(X)
# The coefficients
print ('Coefficients: \n', regr.coef_)
print ('Intercept:', regr.intercept_)
print ('Parameters:', regr.get_params())
# The mean squared error
print("Mean squared error:", mean_squared_error(y, y_pred))
print ('The score is:', regr.score(X, y))

# >>> evaluating the model
# Coefficients: 
#  [ 0.45678101 -0.14502802]
# Intercept: 0.09612860515864824
# Parameters: {'copy_X': True, 'fit_intercept': True, 'n_jobs': None, 'normalize': False}
# Mean squared error: 0.002051440119013479
# The score is: 0.40443559350388314

#####################################################################
plt.axes([0.2, 0.2, 0.75, 0.75])

def linear_func(x):
	return 2.2*x

# plt.plot(x1_vec, x2_vec)
x_vec = np.linspace(0.02, 0.11, 3)
plt.plot(x_vec, linear_func(x_vec), color='black')

#####################################################################
threshold = 0.08
marker_vec = ['o' if a < threshold else 'x' for a in click_rate_vec]

for x, y, m, s in zip(p_receivers_vec, reward_vec, marker_vec, np.asarray(click_rate_vec)*1000):
	plt.scatter(x, y, marker=m, s=s, color='black')

x1_vec = [(threshold-regr.intercept_) / regr.coef_[0], 0]
x2_vec = [0, (threshold-regr.intercept_) / regr.coef_[1]]


plt.xlabel('recommendation prob. $q$', weight='bold')
plt.ylabel('reward $r$', weight='bold')

legend_elements = [
	Line2D([0], [0], marker='o', color='w', label='CTR<0.08', markerfacecolor='black', markersize=13),
	Line2D([0], [0], marker='x', color='w', label='CTR>0.08', markeredgecolor='black', markersize=13)
]
plt.legend(handles=legend_elements, frameon=True, loc='upper left', fontsize=18)

plt.savefig('images/predict_click_rate.eps', dpi=1200)
plt.show()
