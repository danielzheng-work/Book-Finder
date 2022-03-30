import os
import pickle
from word_freq import word_freq


# Save an object as a pickle file; a compressed version
def save_as_pkl(object, path):
	pickle.dump(object, open(path, "wb"))

# Load an object from a pickle file
def load_pkl(path):
	obj = pickle.load(open(path, "rb"))
	return obj

# Representing books as nodes in the graph
# with edges (neighbors) for each other book
# with common review words used.
class Node:
	def __init__(self, name, neighbors):
		self.name = name
		self.neighbors = neighbors

	# Outputs nodes to which the book has edges
	def get_neighbors(self):
		return self.neighbors

# Returns the top 10 most used words in reviews for
# each book.
def find_top_10(topItems, excludedList):
	top5 = {}
	for asin in topItems:
		top5[asin] = [[],[]]
		for word in topItems[asin]:
			if len(top5[asin][0]) < 5:
				if word not in excludedList:
					top5[asin][0].append(word)
					top5[asin][1].append(topItems[asin][word])
			else:
				mi = min(top5[asin][1])
				if topItems[asin][word] > mi and word not in excludedList:
					ind = top5[asin][1].index(mi)
					top5[asin][0][ind] = word
					top5[asin][1][ind] = topItems[asin][word]
	return top5

# Returns a dictionary of structure
# word:[list of asins whose reviews use that word], ...

def find_common_words(top5):
	commonWords = {}

	for asin in top5:
		for word in top5[asin][0]:
			if word in commonWords:
				commonWords[word].append(asin)
			else:
				commonWords[word] = [asin]
	return commonWords

# Creates the adjacency list representation of the
# graph which is used for computing similar books.
def make_graph(top5, commonWords):
	# Adjacency List representation of the graph
	graph = {}
	nodes = {}
	for asin in top5:
		neighbors = set([])
		for word in top5[asin][0]:
			neighbors = neighbors | set(commonWords[word])
		nodes[asin] = Node(asin, neighbors)
		graph[asin] = neighbors

	return nodes

def main():

	# A list of words with no significance for
	# reader sentiment. These will be excluded from
	# common word comparisons between book reviews.
	excludedList = ['this', 'the', 'a', 'i', 'and', 'to', 'of', 'in', 'my', 'is', 'with', 'that', 'it', 'as', 'be',
				'but', 'was', 'an', 'me', 'for', 'her', 'she', 'he', 'you', 'are', 'have', 'at', 'on', 'they',
				'also', 'almost', 'its', 'his', 'if', 'read', 'book', 'author', 'not', 'by', 'one', 'who',
				'what', 'from', 'too', 'or', 'there', 'did', 'so', 'us', 'all', 'we', 'out', 'will', 'just',
				'when', 'has', 'how', 'your', 'can', 'has', 'than', 'their', 'about', 'into', 'first',
				'story', 'books', 'ive', 'up', 'been', 'much', 'which', 'am', 'had', 'no', 'more', 'many',
				'do', 'our', 'get', 'like', 'very', 'characters', 'series', 'would', 'some', 'novel', 'really', 'other',
				'him', 'end', 'only', 'plot', 'even', 'stories', 'most', 'girl', 'put', 'still', 'after', 'man',
				'ending', 'two', 'them', 'people', 'reading', 'time', 'well', 'were', 'these', 'wait', 'because',
				'through', 'dont', 'down', 'didnt', 'cant', 'know', 'men', 'could', 'three']

	data = load_pkl('pickles/data.pkl')
	asins = load_pkl('pickles/asinCounts.pkl')
	topItems = load_pkl('pickles/topItems.pkl')
	
	top5 = find_top_10(topItems, excludedList)
	commonWords = find_common_words(top5)
	graph = make_graph(top5, commonWords)

	return graph

if __name__ == "__main__":
	graph = main()
	unsorted = [(x, len(graph[x].get_neighbors())) for x in graph]
	unsorted.sort(key=lambda x: x[1],reverse=True)
	print("Other books with similar keywords: ")
	for i in unsorted[:10]:
		print("ASIN: " + str(i[0]) + " with " + str(i[1]) + " occurences of words")
	