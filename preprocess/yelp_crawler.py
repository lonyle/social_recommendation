import scrapy
import json

input_filename = 'business.json'
output_filename = 'data/check_in_offer_remaining.json'

class OpenriceSpider(scrapy.Spider):
	#download_delay = 5
	name = 'yelp'
	allowed_domains = ['www.yelp.com']

	def start_requests(self):
		headers = {
			'accept-encoding': 'gzip, deflate, sdch, br',
			'accept-language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
			'upgrade-insecure-requests': '1',
			#'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
			'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
			'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'cache-control': 'max-age=0',
		}

		#urls = ['https://www.yelp.ca/biz/insomnia-restaurant-and-lounge-toronto']
		
		prefix = 'https://www.yelp.com/biz/'
		#business_ids = ['insomnia-restaurant-and-lounge-toronto']
		business_ids = json.load(open('data/output_remaining_businesses.json'))
		
		# with open(input_filename) as f:
		# 	line = f.readline()
		# 	while line:
		# 		data = json.loads(line)
		# 		business_ids.append(data['business_id'])
		# 		line = f.readline()
		

		for business_id in business_ids:
			url = prefix + business_id
			yield scrapy.Request(url=url, headers=headers, callback=self.parse, meta={'business_id': business_id})

	def parse(self, response):
		check_in_offer_selector = 'b.check-in-offer-text::text'
		check_in_offer_text = response.css(check_in_offer_selector).extract_first()
		
		# name_selector = 'h1.biz-page-title.embossed-text-white::text'
		# name_text = response.css(name_selector).extract_first()

		url = response.request.url
		business_id = response.meta.get('business_id')

		business = {"url": url, "check_in_offer_text": check_in_offer_text, "business_id": business_id}

		with open(output_filename, 'a+') as f:
			string = json.dumps(business)
			f.write(string + '\n')