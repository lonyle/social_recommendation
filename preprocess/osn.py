import json
import sys
sys.path.insert(0, 'simulation')
import setting
import random

# !!! this directed osn stores the incoming friends of a user (reversed)
class OnlineSocialNetwork:
	def __init__(self, dataset_name):
		self.edges = dict() # the retained edges
		self.nodes = None
		self.weighted_edges = dict()
		self.dataset_name = dataset_name
		print ('constructing the online social network graph...')
		if dataset_name == 'yelp':
			self.is_weighted = False
			self.init_yelp('data/user.json')
			#self.init_yelp('data/user_0.7.json')
		elif dataset_name == 'wechat':
			self.is_weighted = True
			self.init_wechat()
		print ('construction completed.')

	def init_yelp(self, filename): # this is a directed unweighted graph
		f = open(filename)
		self.N_zero_degree = 0
		for line in f:	
			data = json.loads(line)
			user_id = data['user_id']
			friends = data['friends']
			self.edges[user_id] = friends
			if len(friends) == 0:
				self.N_zero_degree += 1
						
		f.close()

		self.N_node = len(self.edges)
		print ('In Yelp, the fraction of zero-degree nodes:', self.N_zero_degree/self.N_node)
		self.nodes = self.edges.keys()
		self.classify_types()


	def get_random_edges_by_weight(self):
		for user_id in self.weighted_edges:
			friends_weighted = self.weighted_edges[user_id]
			friends_retained = []
			for pair in friends_weighted:
				friend = pair[0]
				weight = pair[1]
				if random.random() < weight:
					friends_retained.append(friend)
			self.edges[user_id] = friends_retained

	# list of nodes in a certain type, for different types
	def classify_types(self):
		self.nodes_type = dict()
		Types = setting.Types + ['zero']
		for Type in Types:
			self.nodes_type[Type] = []
		for node in self.nodes:
			if self.is_weighted == False:
				degree = len(self.edges[node])
			else:
				degree = len(self.weighted_edges[node])
			Type = setting.type_of_node(degree)
			self.nodes_type[Type].append(node)
		for Type in Types:
			print ('The numbers of nodes of type', Type, ':', len(self.nodes_type[Type]))

if __name__ == '__main__':
	graph = OnlineSocialNetwork('yelp')
