# the elasticity of the sales amount w.r.t. the occupation probability

# goal: q and sales amount, q and elasticity

import numpy as np 
#from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

import matplotlib
font = {'size'   : 24, 'weight': 'bold'}
matplotlib.rc('font', **font)
import json

from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

linestyle_dict = {
    'solid':              (0, ()),
    'densely dotted':      (0, (1, 1)),
    'dashed':             (0, (5, 5)),
    'dashdotted':          (0, (3, 5, 1, 5)),
    'loosely dashdotted':  (0, (3, 10, 1, 10)),
    'densely dashdotted':  (0, (3, 1, 1, 1)),
    'densely dashdotted':  (0, (3, 1, 1, 1))
}

########## other parameters #################
slope = 5
# suppose lambda(r) = 1 + slope*r

########## distribution settings ############
MAX_ORDER = 1000
prob = [0] * MAX_ORDER

alpha = 2.5 # power-law coef, default=2.5

for k in range(1, MAX_ORDER):
	prob[k] = k**(-alpha)

prob[1] = 0

Sum = sum(prob)
for k in range(MAX_ORDER):
	prob[k] = prob[k] / Sum

z = 0
for k in range(MAX_ORDER):
	z += k * prob[k]

print ('default mean degree:', z)

def G0(x):
	y = 0
	for k in range(MAX_ORDER):
		y += prob[k] * x**k
	return y

def G1(x):
	y = 0
	for k in range(1, MAX_ORDER):
		y += k * prob[k] * x**(k-1)
	return y / z

def G1_prime(x):
	y = 0
	for k in range(2, MAX_ORDER):
		y += k*(k-1) * prob[k] * x**(k-2)
	return y / z

def get_q(u, omega):
	return (1-u) / (1-(1-omega)*G1(u))

def get_S(u, omega):
	return 1 - (1-omega) * G0(u)

def get_derivative(u, omega):
	numerator = z * (1-omega) * (1-(1-omega)*G1(u))**2 * G1(u)
	denominator = 1 - (1-omega) * G1(u) - (1-u) * (1-omega) * G1_prime(u)
	return numerator / denominator

def get_profit(u, omega, q0, q0_R):
	q = get_q(u, omega)
	S = get_S(u, omega)
	Lambda = q / q0
	r = (Lambda - 1)/slope
	if Lambda < 1 or r > 1 or q0_R*Lambda > 1:
		return None, None
	profit = S * (1-r*q0_R*Lambda)
	return r, profit

def get_dPdr():
	return 0

def r_and_profit(q0, q0_R):
	omega_vec = [0.001, 0.01, 0.1]
	for omega in omega_vec:
		u_vec = list(np.linspace(0.000001, 0.01, 1000)) + list(np.linspace(0.01, 0.99, 1000)) + list(np.linspace(0.99, 0.9999999999, 1000))
		r_vec = []
		profit_vec = []
		for u in u_vec:
			r, profit = get_profit(u, omega, q0, q0_R)
			if r != None:
				r_vec.append(r)
				profit_vec.append(profit)
		plt.plot(r_vec, profit_vec, label='$\delta=$'+str(omega))
	plt.xlabel('reward $r$')
	plt.ylabel('profit $P$')
	plt.title('$q(0)=$' + str(q0) + ', $q_R(0)=$' + str(q0_R))
	plt.xlim(0, 1)
	plt.legend()
	plt.savefig('images/r_and_profit_'+str(q0)+'_'+str(q0_R)+'.eps', dpi=5000)
	plt.show()

def q_and_S():
	tmp_filename = 'data/result_q_and_S.json'
	results = dict()
	omega_vec = [0.0001, 0.001, 0.01, 0.1]
	for omega in omega_vec:
		u_vec = list(np.linspace(0.000001, 0.01, 1000)) + list(np.linspace(0.01, 0.99, 1000)) + list(np.linspace(0.99, 0.9999999999, 1000))
		q_plot_vec = []
		S_plot_vec = []
		for u in u_vec:
			q = get_q(u, omega)
			S = get_S(u, omega)
			dS_dq = get_derivative(u, omega)
			if q < 1:
				q_plot_vec.append(q)
				S_plot_vec.append(S)

		#plt.plot(u_vec, q_plot_vec)
		results[omega] = {'q_plot_vec': q_plot_vec, 'S_plot_vec': S_plot_vec}

	with open(tmp_filename, 'w') as output_file:
		json.dump(results, output_file)

		

def plot_q_and_S(critical_value):
	tmp_filename = 'data/result_q_and_S.json'	
	results = json.load(open(tmp_filename))
	linestyle_vec = ['solid', 'densely dotted', 'dashed', 'dashdotted']

	fig = plt.figure()
	ax = fig.add_axes([0.2, 0.2, 0.75, 0.7])
	axins = zoomed_inset_axes(ax, 8, loc=4)

	marker_idx = 0
	for delta in [0.001, 0.01, 0.1]:
		q_plot_vec = results[str(delta)]['q_plot_vec']
		S_plot_vec = results[str(delta)]['S_plot_vec']
		ax.plot(q_plot_vec, S_plot_vec, color='black', label='$\delta=$'+str(delta),\
			linestyle=linestyle_dict[linestyle_vec[marker_idx]], linewidth=3)
		axins.plot(q_plot_vec, S_plot_vec, color='black', \
			linestyle=linestyle_dict[linestyle_vec[marker_idx]], linewidth=3)
		marker_idx += 1

	mark_inset(ax, axins, loc1=2, loc2=3, fc="none", ec="0.5")

	axins.axvline(x=critical_value, color='k', linestyle='--')#label='critical value')
	ax.set_xlabel('recommendation prob. $q_i$', weight='bold')
	ax.set_ylabel('normed demand $D_i$', weight='bold')
	plt.yticks(visible=False)
	plt.xticks(visible=False)

	axins.set_xlim(-0.015, 0.06)
	axins.set_ylim(0, 0.06)

	ax.set_ylim(-0.05, 1.3)
	axins.text(0.45, 0.32, 'critical \nvalue$\\rightarrow$', transform=ax.transAxes, fontsize=20, verticalalignment='top')
	ax.legend(loc = 'upper left', fontsize=20, frameon=False)
	plt.savefig('images/q_and_S.eps', dpi=1200)
	plt.show()


def q_and_elasticity():
	tmp_filename = 'data/result_q_and_elasticity.json'
	results = dict()
	omega_vec = [0.0001, 0.001, 0.01, 0.1]
	#omega_vec = [0.001, 0.01]
	for omega in omega_vec:
		u_vec = list(np.linspace(0.000001, 0.01, 1000)) + list(np.linspace(0.01, 0.99, 1000)) + list(np.linspace(0.99, 0.9999999999, 1000))
		q_plot_vec = []
		elasticity_plot_vec = []
		for u in u_vec:
			q = get_q(u, omega)
			S = get_S(u, omega)
			dS_dq = get_derivative(u, omega)
			elasticity = q / S * dS_dq
			if q < 1:
				q_plot_vec.append(q)
				elasticity_plot_vec.append(elasticity)
		results[omega] = {'q_plot_vec': q_plot_vec, 'elasticity_plot_vec': elasticity_plot_vec}
		
	with open(tmp_filename, 'w') as output_file:
		json.dump(results, output_file)

def plot_q_and_elasticity(critical_value):
	tmp_filename = 'data/result_q_and_elasticity.json'	
	results = json.load(open(tmp_filename))

	linestyle_vec = ['solid', 'densely dotted', 'dashed', 'dashdotted']

	fig = plt.figure()
	ax = fig.add_axes([0.18, 0.18, 0.75, 0.7])

	marker_idx = 0
	for delta in [0.001, 0.01, 0.1]:
		q_plot_vec = results[str(delta)]['q_plot_vec']
		elasticity_plot_vec = results[str(delta)]['elasticity_plot_vec']
		ax.plot(q_plot_vec, elasticity_plot_vec, color='black', label='$\delta=$'+str(delta),\
			linestyle=linestyle_dict[linestyle_vec[marker_idx]], linewidth=3)
		marker_idx += 1

	ax.axvline(x=critical_value, color='k', linestyle='--')
	plt.xlabel('recommendation prob. $q_i$', weight='bold')
	plt.ylabel('elasticity $\\frac{q_idD_i}{D_idq_i}$', weight='bold')
	ax.text(0.14, 0.9, '   critical\n$\\leftarrow$value', transform=ax.transAxes, fontsize=20, verticalalignment='top')
	plt.xlim(0, 0.22)
	plt.legend(loc = 'upper right', frameon=False, fontsize=21)
	plt.savefig('images/q_and_elasticity.eps', dpi=1200)
	plt.show()

def run_r_and_profit():
	q0 = 0.02 # 1. q0 near the threshold
	#q0 = 0.004 # 2. q0 below the threshold
	#q0 = 0.04 # 3. q0 above the threshold
	for q0_R in [q0*4]:#[q0*2, q0*4, q0*8]:
		r_and_profit(q0, q0_R) 

def alter_degree_dist(alpha):
	for k in range(1, MAX_ORDER):
		prob[k] = k**(-alpha)

	prob[1] = 0

	Sum = sum(prob)
	for k in range(MAX_ORDER):
		prob[k] = prob[k] / Sum

	z = 0
	for k in range(MAX_ORDER):
		z += k * prob[k]

	print ('altered mean degree:', z)

def degree_and_elasticity():
	alpha_vec = [2]
	for alpha in alpha_vec:
		alter_degree_dist(alpha)	


if __name__ == '__main__':
	print ('critical value:', 1/G1_prime(1))
	# q_and_S()
	#plot_q_and_S( 1/G1_prime(1) )

	#q_and_elasticity()
	plot_q_and_elasticity( 1/G1_prime(1) )

	#run_r_and_profit()
	


