aspect_rating_filename = 'LARA/Data/drv_aspect_rating_business.txt'
business_input_filename = 'data/drv_business_review.json'
business_output_filename = 'data/drv_business.json'

def add_aspect_rating(business_dict):
	stat_dict = dict()
	for key in business_dict:
		stat_dict[key] = {'count': 0, 'sum': 0}
	f = open(aspect_rating_filename)
	for line in f:
		data = line.split(',')
		business_id = data[0]
		aspect_rating = float(data[1])
		if aspect_rating != 0 and business_id in stat_dict:
			stat_dict[business_id]['count'] += 1
			stat_dict[business_id]['sum'] += aspect_rating
	for key in business_dict:
		if stat_dict[key]['count'] > 0:
			business_dict[key]['price_rating'] = stat_dict[key]['sum']/stat_dict[key]['count']
		else:
			business_dict[key]['price_rating'] = None
	return business_dict

if __name__ == '__main__':
	business_dict_id = utils.load_business_by_id(business_input_filename)
	add_aspect_rating(business_dict_id)
	utils.dump_business(business_dict_id, business_output_filename)