import os
import json

def load_business_by_name(filename):
	business_dict = dict()
	f_business = open(filename)
	line = f_business.readline()
	while line:
		business = json.loads(line)
		business_name = business['name']
		business_name = business_name.replace('&', 'and')
		business_name = business_name.replace(' ', '-')
		business_name = business_name.replace('\u2019', '').replace('\'', '')
		city = business['city']
		city = city.replace(' ', '-')
		business_idx = business_name.lower() + '-' + city.lower()
		#if business_idx in business_dict.keys():
		#	print ('duplicated index:', business_idx)
		business_dict[business_idx] = business
		#print ('business_idx:', business_idx)

		line = f_business.readline()
	f_business.close()
	return business_dict

def load_business_by_id(filename):
	business_dict = dict()
	f_business = open(filename)
	line = f_business.readline()
	while line:
		business = json.loads(line)
		business_dict[business['business_id']] = business
		line = f_business.readline()
	f_business.close()
	return business_dict

def dump_business(business_dict, filename):
	try:
	    os.remove(filename)
	except OSError as e:
	    print (e)

	f_output = open(filename, 'a')
	remaining_business_id_vec = []
	for key in business_dict:
		business = business_dict[key]
		
		if 'check_in_offer_text' in business.keys():
			f_output.write(json.dumps(business) + '\n')
		else:
			#print (business["business_id"])
			remaining_business_id_vec.append(business["business_id"])
	f_output.close()
	print ('number of businesses:', len(business_dict))
	print ('number of remaining businesses:', len(remaining_business_id_vec))
	# with open('data/output_remaining_businesses.json', 'w') as output_file:
	# 	json.dump(remaining_business_id_vec, output_file)
	return 0
