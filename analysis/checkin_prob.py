import re
import json
import numpy as np 
import matplotlib.pyplot as plt

business_output_filename = 'data/business_checkinoffer.json'

def check_in_offer_level(business):
	average_price_in_range = [5, 20, 45, 100]
	text = business['check_in_offer_text']

	offer = None
	category = 'None'
	level = 0

	if text:
		text_vec = text.split(' ')	
		if text_vec[1] == 'off':
			if '%' in text_vec[0]:
				category = 'percentage'
				if 'RestaurantsPriceRange2' in business.keys():
					price_range = business['RestaurantsPriceRange2']
					offer = float(re.sub("[^\d\.]", "", text_vec[0])) #/100 * average_price_in_range[price_range]
				else:
					offer = float(re.sub("[^\d\.]", "", text_vec[0])) #/ 100 * 20 # use 20 as the default
				if offer <= 10:
					level = 1
				elif offer <= 30:
					level = 2
				else:
					level = 3
				# if offer == 1:
				# 	print (text)
			elif '$' in text_vec[0]:
				category = 'money'
				offer = float(re.sub("[^\d\.]", "", text_vec[0]))
				if offer <= 10:
					level = 1
				elif offer <= 20:
					level = 2
				else:
					level = 3
			else:
				print (text)
		elif text_vec[1] == 'free':
			category = 'free'
			offer = int(text_vec[0]) * 2 # use 2 dollars as default
			level = 2
		else:
			offer = 0
			category = 'None'
	return offer, category, level


def plot_review_checkin(filename):
	f = open(filename)
	line = f.readline()
	review_vec = []
	checkin_vec = []
	checkin_ratio_vec = []
	line = f.readline()
	while line:
		business = json.loads(line)
		if 'checkin_count' in business.keys():
			review_vec.append(business['review_count'])
			checkin_vec.append(business['checkin_count'])
			checkin_ratio_vec.append(business['checkin_count']/business['review_count'])
		line = f.readline()

	plt.scatter(review_vec, checkin_ratio_vec, alpha=0.1)
	plt.xlim(0,2000)
	plt.ylim(0,200) 
	plt.show()

def checkin_review_ratio_checkinoffer(filename):
	'''
	checkin_review_ratio with or without checkin offer
	'''
	f = open(filename)
	#line = f.readline()
	review_count_with_offer = 0
	review_count_without_offer = 0
	checkin_count_with_offer = 0
	checkin_count_without_offer = 0

	N_checkin_offer = 0
	N_no_checkin_offer = 0
	
	line = f.readline()
	while line:
		business = json.loads(line)
		if 'checkin_count' in business.keys():
			if business['check_in_offer_text'] != None:
				review_count_with_offer += business['review_count']
				checkin_count_with_offer += business['checkin_count']
				N_checkin_offer += 1
			else:
				review_count_without_offer += business['review_count']
				checkin_count_without_offer += business['checkin_count']
				N_no_checkin_offer += 1
		line = f.readline()

	print ('N_checkin_offer:', N_checkin_offer)
	print ('checkin_count_with_offer:', checkin_count_with_offer)
	print ('review_count_with_offer:', review_count_with_offer)
	print ('average checkin/review ratio with check-in offer:', \
		checkin_count_with_offer/review_count_with_offer)

	print ('N_no_checkin_offer:', N_no_checkin_offer)
	print ('checkin_count_without_offer:', checkin_count_without_offer)
	print ('review_count_without_offer:', review_count_without_offer)
	print ('average checkin/review ratio without check-in offer:', \
		checkin_count_without_offer/review_count_without_offer)
	

def plot_checkinoffer_star(filename):
	star_vec_with_offer = []
	review_count_vec_with_offer = []
	star_vec_without_offer = []
	review_count_vec_without_offer = []

	f = open(filename)
	line = f.readline()	
	while line:
		business = json.loads(line)
		stars = business['stars']
		review_count = business['review_count']
		if business['check_in_offer_text'] == None:
			star_vec_without_offer.append(stars)
			review_count_vec_without_offer.append(review_count)
		else:
			star_vec_with_offer.append(stars)
			review_count_vec_with_offer.append(review_count)
		line = f.readline()	

	average_star_with = np.average(star_vec_with_offer, weights=review_count_vec_with_offer)
	average_star_without = np.average(star_vec_without_offer, weights=review_count_vec_without_offer)
	print ('the average stars with offer is', average_star_with)
	print ('the average stars without offer is', average_star_without)


def plot_star_checkin(filename):
	'''
	the average ratio between the check-in count and # reviews, for different stars
	'''
	f = open(filename)
	line = f.readline()
	star_vec = []
	checkin_vec = []
	line = f.readline()
	ratio_sum = [0] * 11
	star_count = [0] * 11
	while line:
		business = json.loads(line)
		if 'checkin_count' in business.keys():
			star_vec.append(business['stars'])
			ratio = business['checkin_count']/business['review_count']
			checkin_vec.append(ratio)
			idx = int(business['stars'] * 2)
			ratio_sum[idx] += ratio * business['review_count']
			star_count[idx] += business['review_count']
		line = f.readline()

	for idx in range(11):
		if star_count[idx] != 0:
			print ('stars:', idx/2, 'average ratio:', ratio_sum[idx]/star_count[idx])
	plt.scatter(star_vec, checkin_vec, alpha=0.1)
	plt.xlim(0,2000)
	plt.ylim(0,200)
	plt.show()

def plot_offer_scale(filename):
	f = open(filename)
	line = f.readline()
	check_in_offer_percentage = []
	check_in_offer_money = []
	check_in_offer_free = []
	review_count_percentage = [0] * 4
	count_percentage = [0] * 4
	review_count_money = [0] * 4
	count_money = [0] * 4
	review_count_free = [0] * 4
	count_free = [0] * 4
	while line:
		business = json.loads(line)
		review_count = business['review_count']
		offer, category, level = check_in_offer_level(business)
		if category == 'percentage':
			check_in_offer_percentage.append(offer)
			review_count_percentage[level] += review_count
			count_percentage[level] += 1
		elif category == 'money':
			check_in_offer_money.append(offer)
			review_count_money[level] += review_count
			count_money[level] += 1
		elif category == 'free':
			check_in_offer_free.append(offer)
			review_count_free[level] += review_count
			count_free[level] += 1
		line = f.readline()
	f.close()
	print ('percentage:', np.divide(review_count_percentage[1:], count_percentage[1:]))
	print ('money:', np.divide(review_count_money[1:], count_money[1:]))
	print ('free:', np.divide(review_count_free[1:], count_free[1:]))
	# plt.hist(check_in_offer_free, 100, range=[0,100])
	# plt.show()

def plot_checkin(filename):
	color_dict = {"percentage": "red", "money": "blue", "free": "green", 'None': "black"}
	f = open(filename)
	line = f.readline()
	offer_vec = []
	ratio_vec = []
	review_count_vec = []
	color_vec = []
	ratio_vec_no_reward = []
	ratio_vec_reward = []
	weight_vec_no_reward = []
	weight_vec_reward = []
	while line:
		business = json.loads(line)
		# focus on a specific star
		if True:#business['stars'] == 4.5:
			if 'checkin_count' in business.keys():
				checkin_count = business['checkin_count']
			else:
				checkin_count = 0
			checkin_ratio = checkin_count / business['review_count']
			offer, category = check_in_offer_level(business)			
			if category == 'None':
				ratio_vec_no_reward.append(checkin_ratio)
				weight_vec_no_reward.append(business['review_count'])
			else:
				ratio_vec_reward.append(checkin_ratio)
				weight_vec_reward.append(business['review_count'])
			#if category == 'money':
			offer_vec.append(offer)
			review_count_vec.append(business['review_count'])
			ratio_vec.append(checkin_ratio)
			color_vec.append(color_dict[category])

		line = f.readline()
	f.close()

	print ('N check-in offer:', len(ratio_vec_reward), 'N others:', len(ratio_vec_no_reward))
	print ('average ratio with reward', np.average(ratio_vec_reward, weights=weight_vec_reward))
	print ('average ratio without reward', np.average(ratio_vec_no_reward, weights=weight_vec_no_reward))
	print ('average review count with reward', np.average(weight_vec_reward))
	print ('average review count without reward', np.average(weight_vec_no_reward))
	# plt.scatter(offer_vec, review_count_vec, color=color_vec, alpha=0.1)
	# plt.xlim(0, 100)
	# plt.ylim(0, 1000)
	plt.show()


if __name__ == '__main__':
	#plot_offer_scale(business_output_filename)
	#plot_checkin(business_output_filename)
	#plot_review_checkin(business_output_filename)
	#plot_star_checkin(business_output_filename)

	#plot_checkinoffer_star(business_output_filename)

	checkin_review_ratio_checkinoffer(business_output_filename)















