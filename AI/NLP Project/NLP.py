from numpy import empty # Creates an empty array
import numpy as np # Used for linear algebra
import math # Used for square roots

stop_words = ["a", "about", "above", "after", "again", "against", "ain", "all", "am", "an", "and", "any", "are", "aren", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can", "couldn", "couldn't", "d", "did", "didn", "didn't", "do", "does", "doesn", "doesn't", "doing", "don", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn", "hadn't", "has", "hasn", "hasn't", "have", "haven", "haven't", "having", "he", "her", "here", "hers", "herself", "him", "himself", "his", "how", "i", "if", "in", "into", "is", "isn", "isn't", "it", "it's", "its", "itself", "just", "ll", "m", "ma", "me", "mightn", "mightn't", "more", "most", "mustn", "mustn't", "my", "myself", "needn", "needn't", "no", "nor", "not", "now", "o", "of", "off", "on", "once", "only", "or", "other", "our", "ours", "ourselves", "out", "over", "own", "re", "s", "same", "shan", "shan't", "she", "she's", "should", "should've", "shouldn", "shouldn't", "so", "some", "such", "t", "than", "that", "that'll", "the", "their", "theirs", "them", "themselves", "then", "there", "these", "they", "this", "those", "through", "to", "too", "under", "until", "up", "ve", "very", "was", "wasn", "wasn't", "we", "were", "weren", "weren't", "what", "when", "where", "which", "while", "who", "whom", "why", "will", "with", "won", "won't", "wouldn", "wouldn't", "y", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves", "could", "he'd", "he'll", "he's", "here's", "how's", "i'd", "i'll", "i'm", "i've", "let's", "ought", "she'd", "she'll", "that's", "there's", "they'd", "they'll", "they're", "they've", "we'd", "we'll", "we're", "we've", "what's", "when's", "where's", "who's", "why's", "would"]
punctuation = [".", "-", "_", ",", "<", ">", "?", "/", "'", "\"", ";", ":", "[", "{", "}", "]", "\\", "|", "`", "~", "!", "@", "#", "$", "^", "&", "*", "(", ")", "--"]
new_stop_words = []
for b in stop_words:
  for p in punctuation:
    if p in b:
      b = b.replace(p,"")
  new_stop_words.append(b)

def cosine_similarity(paragraph1, paragraph2):
	# Create a set and add all the words in paragraph1 and paragraph2
	# to this set. There's no need to keep track of duplicates
	all_words = set()
	all_words.update(paragraph1)
	all_words.update(paragraph2)

	# For each word in the set of all_words:
	#	add a 1 if this word is in paragraph1 otherwise add 0
	# Do this for both paragraph1 and paragraph2
	paragraph1vector = list()
	paragraph2vector = list()
	for word in all_words:
		paragraph1vector.append(1) if word in paragraph1 else paragraph1vector.append(0)
		paragraph2vector.append(1) if word in paragraph2 else paragraph2vector.append(0)
	
	# Convert these lists to NumPy arrays so we can use built-in linear algebra functions
	pg1vect = np.asarray(paragraph1vector, dtype=np.float32)
	pg2vect = np.asarray(paragraph2vector, dtype=np.float32)

	# Cosine similarity is defined as the dot product of two vectors over
	# the product of their magnitudes
	# Calculate these values using numpy functions
	sum_val = np.dot(pg1vect, pg2vect)
	magnitudeA = np.linalg.norm(pg1vect)
	magnitudeB = np.linalg.norm(pg2vect)

	# This prevents errors that arise due to division by 0
	if magnitudeA == 0 or magnitudeB == 0:
		return 0.0

	# Calculate the cosine similarity
	cosine_sim_val = float(sum_val) / float(magnitudeA*magnitudeB)

	# Return this value
	return cosine_sim_val

def calculate_stationary_probabilities(adjacency_matrix):
	# Code pulled from Duke University, Stats 663 from Dr. Cliburn Chan
	# http://people.duke.edu/~ccc14/sta-663-2016/homework/Homework02_Solutions.html#Part-3:-Option-2:-Using-numpy.linalg-with-transpose-to-get-the-left-eigenvectors

	a = adjacency_matrix
	b = np.sum(adjacency_matrix, 1)[:, np.newaxis]
	
	normalized_matrix = c = np.divide(a, b, out=np.zeros_like(a), where=b!=0)
	
	matrix_mult_result = np.linalg.matrix_power(normalized_matrix, 5000)
	matrix_mult_result_check = np.dot(matrix_mult_result, normalized_matrix)
	np.testing.assert_allclose(matrix_mult_result, matrix_mult_result_check)
	return matrix_mult_result_check

def clean_paragraph(paragraph):
  book = paragraph.split(" ")
  new_book = []
  for b in book:
    for p in punctuation:
      if p in b:
        b = b.replace(p, "")
    if b not in new_stop_words:
      new_book.append(b)
  return new_book
  
def clean_book(file_location):
  b = open(file_location, 'r')
  lines = b.readlines()
  lines = ''.join(lines)
  paragraph = lines.split('\n')
  our_map = []
  for p in paragraph:
    our_map.append(clean_paragraph(p))
  b.close()
  return our_map


def build_matrix(paragraph_list):
  n = len(paragraph_list)
  adjacency_matrix = np.zeros((n,n))
  #paragraph_map = list(paragraph_list.values())
  for i,r in enumerate(adjacency_matrix):
    for j, c in enumerate(r):
      if i != j:
        adjacency_matrix[i,j] = cosine_similarity(paragraph_list[i],paragraph_list[j])
  return adjacency_matrix

def output_summarization_paragraphs(distribution, gatsby_map, num_paragraphs):
  dis_sort = np.argsort(distribution)[-num_paragraphs:][::-1]
  for d in dis_sort:
    print(gatsby_map[d])
  

def main():
  file_location = "the-great-gatsby.txt"
  my_map = clean_book(file_location)
  adj_m = build_matrix(my_map)
  sp = calculate_stationary_probabilities(adj_m)
  output_summarization_paragraphs(sp, my_map, 1)

if __name__ == '__main__':
  main()
