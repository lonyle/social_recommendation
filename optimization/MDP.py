# we first consider the simplest case of a population (fully connected graph)
# the state is about (# users newly informed, # users already informed)

import numpy as np
from scipy.stats import binom

w = 0.1 # the prob for an edge to be conductive
N_user = 50
r_vec = np.linspace(0,1,11)
p = 1
c = 0

''' the recommendation prob when reward is r'''
def q(r):
	return 0.05 * r

''' the return in the transition (m,n) -> (m+n,n1) when the chosen reward is r '''
''' m is the number of already-informed, n is the number of newly informed '''
def R(m, n, n1, r):
	unit_profit = p - c - q(r) * r
	return n * unit_profit

''' the transition prob (m,n) -> (m+n,n1) when the chosen reward is r '''
def get_Pr_vec(m, n, r):
	rv = binom(N_user-m-n, 1-(1-q(r)*w)**n)
	return rv.pmf(range(N_user-m-n+1))

def get_Q(m, n, Q_mat, opt_r_mat):
	if Q_mat[m][n] != None:
		return Q_mat[m][n]
	if n == 0:
		return 0
	argmax = None
	max_value = -1
	for r in r_vec:
		value = 0
		Pr_vec = get_Pr_vec(m, n, r)
		for n1 in range(N_user-m-n+1):
			value += (R(m, n, n1, r) + get_Q(m+n, n1, Q_mat, opt_r_mat)) * Pr_vec[n1]
		if value > max_value:
			max_value = value
			argmax = r
	Q_mat[m][n] = max_value
	opt_r_mat[m][n] = argmax
	return Q_mat[m][n]

if __name__ == '__main__':
	Q_mat = [[None] * (N_user+1) for n in range(N_user+1)]
	opt_r_mat = [[None] * (N_user+1) for n in range(N_user+1)]
	Q = get_Q(0, 5, Q_mat, opt_r_mat)
	np.savetxt("data/drv_Q.csv", np.asarray(Q_mat), delimiter=",", fmt='%s')
	np.savetxt('data/drv_opt_r.csv', np.asarray(opt_r_mat), delimiter=',', fmt='%s')

