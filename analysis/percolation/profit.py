import numpy as np 
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

omega = 0.4 # original fraction of purchases, default=0.4
eta = 0.5 # concern of friends' utility, default=0.5
gamma = 0 # weight on the trust, default=0
T = 0.2 # average surplus
m = 0 # marginal cost

MAX_ORDER = 500
alpha = 2.3 # power-law coef, default=2
prob = [0] * MAX_ORDER
for k in range(1, MAX_ORDER):
	prob[k] = k**(-alpha)
Sum = sum(prob)
for k in range(MAX_ORDER):
	prob[k] = prob[k] / Sum

z = 0
for k in range(MAX_ORDER):
	z += k * prob[k]

def G0(x):
	y = 0
	for k in range(MAX_ORDER):
		y += prob[k] * x**k
	return y

def G1(x):
	y = 0
	for k in range(MAX_ORDER):
		y += k * prob[k] * x**k
	return y / z

def get_r(p, u):
	q = (1-u) / (1-(1-omega)*G1(u))
	q_R = q/(1-p+gamma/(1-gamma)*T)
	if q_R > 1:
		return None
	r = q_R - eta*(0.5-p)
	if r < 0:
		return None
	if r > p:
		return None
	return r

def get_profit(p, u):
	r = get_r(p,u)
	if r == None:
		return None, None
	unit_profit = p-m-r*(r+eta*(0.5-p))
	demand = (1-p+gamma/(1-gamma)*T) * (1-(1-omega)*G0(u))
	profit = unit_profit * demand
	return profit, r

if __name__ == '__main__':
	p_vec = np.linspace(0,0.99, 100)
	u_vec = np.linspace(0,0.99, 100)
	p_plot_vec = []
	r_plot_vec = []
	profit_plot_vec = []
	max_profit = -1
	argmax = (None, None)
	for p in p_vec:
		for u in u_vec:
			profit, r = get_profit(p, u)
			if profit != None:
				p_plot_vec.append(p)
				r_plot_vec.append(r)
				profit_plot_vec.append(profit)
				if profit > max_profit:
					max_profit = profit 
					argmax = (p, r)

	print ('opt price, opt reward:', argmax, 'max profit:', max_profit)

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.scatter(p_plot_vec, r_plot_vec, profit_plot_vec)

	ax.set_xlabel('price $p$')
	ax.set_ylabel('reward $r$')
	ax.set_zlabel('profit')

	plt.show()
