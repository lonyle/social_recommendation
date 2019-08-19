import sys
sys.path.insert(1, 'preprocess')
import osn

def get_edges():
	''' get the edges (dictionary of lists) for yelp network, bi-directed
	'''
	print ('getting edges for yelp...')
	yelp_osn = osn.OnlineSocialNetwork('yelp')
	return yelp_osn.edges