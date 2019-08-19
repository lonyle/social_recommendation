from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import matplotlib.pyplot as plt

price_vec = [0,0,0,0,0,-0.1,-1,0,0]
reward_vec = [1,1,0.05,1,0.5,0,0,0,0]
rec_prob_vec = [0.045615,0.045647,0.02636,0.009528,0.008174,0.001887,0.029088,0.00763,0.00539]

def train_reward_price():
	X = np.c_[price_vec, reward_vec]
	y = np.asarray(rec_prob_vec)

	regr = linear_model.LinearRegression()
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

	return y, y_pred

def train_price():
	X = np.c_[price_vec]
	y = np.asarray(rec_prob_vec)

	regr = linear_model.LinearRegression()
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

	return y, y_pred

def plot(y, y_pred):
	plt.scatter(y, y_pred)
	plt.show()

if __name__ == '__main__':
	#y, y_pred = train_reward_price()
	y, y_pred = train_price()
	#plot(y, y_pred)





