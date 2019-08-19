import json
from operator import itemgetter

review_filename = 'data/review.json'
output_filename = 'data/sorted_review.json'

if __name__ == '__main__':	
	f = open(review_filename)
	review_vec = []
	for line in f:
		data = json.loads(line)
		user_id = data['user_id']
		business_id = data['business_id']
		stars = data['stars']
		date = data['date']
		new_data = {"user_id": user_id, "business_id": business_id, "stars": stars, "date": date}
		review_vec.append(new_data)
	f.close()
	print ('sorting...')
	sorted_review_vec = sorted(review_vec, key = itemgetter('business_id'))
	print ('sorting completed.')
	f = open(output_filename, 'a')
	for review in sorted_review_vec:
		f.write(json.dumps(review) + '\n')