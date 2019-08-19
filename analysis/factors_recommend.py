# see the impacts of various factors on the recommendation probability
import json
import matplotlib.pyplot as plt

import matplotlib
font = {'size'   : 18}
matplotlib.rc('font', **font)


'''the relationship between the price and the recommenation prob (review count)'''
def price_recommend(business_filename):
	f = open(business_filename)
	line = f.readline()
	sum_dict = dict()
	count_dict = dict()
	while line:
		business = json.loads(line)
		if 'RestaurantsPriceRange2' in business['attributes']:
			price_range = business['attributes']['RestaurantsPriceRange2']
		else:
			line = f.readline()
			continue
		review_count = business['review_count']
		if price_range in sum_dict:
			sum_dict[price_range] += review_count
			count_dict[price_range] += 1
		else:
			sum_dict[price_range] = review_count
			count_dict[price_range] = 1
		line = f.readline()

	average_reviewcount = dict()
	for key in count_dict.keys():
		average_reviewcount[key] = sum_dict[key]/count_dict[key]
	print ('average reviewcount for different price_range:', average_reviewcount)

'''the relationship between the stars and the recommenation prob'''
def stars_recommend(business_filename):
	f = open(business_filename)
	line = f.readline()
	sum_dict = dict()
	count_dict = dict()
	while line:
		business = json.loads(line)
		line = f.readline()
		if 'stars' in business:
			stars = business['stars']
		else:			
			continue
		review_count = business['review_count']
		if 'p_with' not in business:
			continue
		p_with = business['p_with']
		if p_with == None:
			continue
		if stars in sum_dict:
			sum_dict[stars] += p_with
			#sum_dict[stars] += review_count
			count_dict[stars] += 1
		else:
			sum_dict[stars] = p_with
			#sum_dict[stars] = review_count
			count_dict[stars] = 1

	average_reviewcount = dict()
	for key in count_dict.keys():
		average_reviewcount[key] = sum_dict[key]/count_dict[key]
	print ('average reviewcount for different stars:', average_reviewcount)
	f.close()

'''the relationship between the category and the enhancement of recommendation prob (by receiving recommendation)'''
def category_enhancement(business_filename):
	f = open(business_filename)
	line = f.readline()
	sum_dict = dict()
	weight_dict = dict()
	while line:
		business = json.loads(line)
		line = f.readline()
		if 'categories' in business:
			categories = business['categories']
		else:
			continue
		if 'p_with' not in business or 'p_without' not in business:
			continue
		if business['p_without'] != 0 and business['p_with'] != None:
			enhancement = business['p_with']/business['p_without']
		else:
			continue
		for category in categories:
			if category in sum_dict:
				sum_dict[category] += enhancement * 1
				weight_dict[category] += 1
			else:
				sum_dict[category] = enhancement * 1
				weight_dict[category] = 1

	average_enhancement = dict()
	for key in sum_dict.keys():
		if weight_dict[key] > 50:
			average_enhancement[key] = sum_dict[key]/weight_dict[key]
			if average_enhancement[key] < 200:
				print ('average enhancement of', key, ':', average_enhancement[key], 'weight:', weight_dict[key])
	f.close()
	return 0


if __name__ == '__main__':
	#price_recommend('data/business_checkinoffer.json')
	#stars_recommend('data/business_reviewers.json')
	category_enhancement('data/business_reviewers.json')
	