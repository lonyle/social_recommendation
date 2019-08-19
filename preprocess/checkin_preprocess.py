import json
import os

checkinoffer_filename = 'data/check_in_offer.json'
business_filename = 'data/business.json'
business_output_filename = 'data/drv_business_checkin.json'
checkin_filename = 'data/checkin.json'

def add_check_in_offer(business_dict):
	f_checkinoffer = open(checkinoffer_filename)
	line = f_checkinoffer.readline()	
	while line:
		data = json.loads(line)
		url = data['url']
		url_prefix = 'https://www.yelp.ca/biz/'
		name_str = url.replace(url_prefix, '').replace("%C3%A9", 'e')
		if name_str[-1].isdigit():
			i = -2
			while name_str[i].isdigit():
				i -= 1
			name_str = name_str[:i]
		if name_str in business_dict.keys():
			business_dict[name_str]['check_in_offer_text'] = data['check_in_offer_text']
			#print (name_str)
		else:
			pass
			#print (name_str)

		line = f_checkinoffer.readline()
	f_checkinoffer.close()
	return business_dict
	

def add_check_in_count(business_dict):
	f = open(checkin_filename)
	line = f.readline()
	while line:
		checkin_count = 0
		data = json.loads(line)
		business_id = data['business_id']
		#days_str = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
		time = data['time']
		for time_key in time:
			for clock_key in time[time_key]:
				checkin_count += time[time_key][clock_key]

		if business_id in business_dict.keys():
			business_dict[business_id]['checkin_count'] = checkin_count
		#else: 
			#print (business_id)

		line = f.readline()
	f.close()
	return business_dict

if __name__ == '__main__':
	business_dict_name = utils.load_business_by_name(business_filename)
	business_dict_name = add_check_in_offer(business_dict_name)
	utils.dump_business(business_dict_name, business_output_filename)
	business_dict_id = utils.load_business_by_id(business_output_filename)
	business_dict_id = add_check_in_count(business_dict_id)
	utils.dump_business(business_dict_id, business_output_filename)