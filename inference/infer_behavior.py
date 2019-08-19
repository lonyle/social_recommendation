import regression
import os
import joblib

import sys
sys.path.insert(0, 'simulation')
import setting

# predict the recommendation prob. for new price and reward (the improvement ratio)
model_filename = 'data/drv_regrmodel.sav'
model_adopt_filename = 'data/drv_regrmodel_adopt.sav'

def ImpRatio_rec_prob(price, reward, old_price, old_reward):
	if not os.path.isfile(model_filename):
		X, y, sample_weight = regression.preprocessing()
		model = regression.linear_regression(X, y, sample_weight)
		joblib.dump(model, model_filename)
	model = joblib.load(model_filename)
	# Note: the input for model.predict should be 2d array
	ImpRatio = model.predict([[reward, price]]) / model.predict([[old_reward, old_price]])
	return ImpRatio

def ImpRatio_adopt_prob(price, old_price):
	if not os.path.isfile(model_adopt_filename):
		model_adopt = regression.linear_regression_price()
		joblib.dump(model_adopt, model_adopt_filename)

	model_adopt = joblib.load(model_adopt_filename)
	ImpRatio = model_adopt.predict([[price]]) / model_adopt.predict([[old_price]])
	return ImpRatio

## directly compute from the inferred parameters of wechat
def ImpRatio_rec_prob_wechat(price, reward, old_price, old_reward):
	# f(p_i,r_i) = 0.00803 + 0.0239 r_i - 0.0202 p_i
	discount = price - 1#non-positive, the default price is 1
	old_discount = old_price - 1
	def f(discount, reward):
		return 0.00803 + 0.0239 * reward - 0.0202 * discount
	ImpRatio = f(discount, reward) / f(old_discount, old_reward)
	return ImpRatio

def ImpRatio_adopt_prob_wechat(price, reward, old_price, old_reward):
	# f(p_i) = 0.0189 - 0.008406 p_i
	discount = price - 1#non-positive, the default price is 1
	old_discount = old_price - 1
	def f(discount, reward):
		return 0.0189 - 0.008406 * (discount)#- 0.3*reward)
	ImpRatio = f(discount, reward) / f(old_discount, old_reward)
	return ImpRatio

def inf_rec_prob(price, reward, old_price, old_reward, old_prob_type):
	#ImpRatio = ImpRatio_rec_prob(price, reward, old_price, old_reward)
	ImpRatio = ImpRatio_rec_prob_wechat(price, reward, old_price, old_reward)
	new_prob_type = {}
	for Type in setting.Types:
		new_prob_type[Type] = old_prob_type[Type] * ImpRatio
		if new_prob_type[Type] > 1:
			#print ('the recommendation probability > 1')
			new_prob_type[Type] = 1
		elif new_prob_type[Type] < 0: # cannot be negative, truncated
			#print ('the recommendation probability < 0')
			new_prob_type[Type] = 0
	return new_prob_type

def inf_adopt_prob(price, reward, old_price, old_reward, old_prob_type):
	#ImpRatio = ImpRatio_adopt_prob(price, old_price)
	ImpRatio = ImpRatio_adopt_prob_wechat(price, reward, old_price, old_reward)
	new_prob_type = {}
	for Type in setting.Types:
		new_prob_type[Type] = old_prob_type[Type] * ImpRatio
		if new_prob_type[Type] > 1:
			#print ('the adopting probability > 1')
			new_prob_type[Type] = 1
		elif new_prob_type[Type] < 0: # cannot be negative, truncated
			#print ('the adopting probability < 0')
			new_prob_type[Type] = 0
	return new_prob_type
