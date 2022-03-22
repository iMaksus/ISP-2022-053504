import re
import argparse
from statistics import mean, median
def parsedata() -> tuple:
	parser = argparse.ArgumentParser()
	parser.add_argument('txt', help = 'text')
	parser.add_argument('k', nargs='?', default = 10, help = 'k (default=%(default)s)')
	parser.add_argument('n', nargs='?', default = 4, help = 'n (default=%(default)s)')
	input = parser.parse_args()
	return(input.txt, input.k, input.n)

def spliting(text: str) -> list:
	chars = "@#%&,;:'()"
	for char in chars:
		text = text.replace(char,'')
	sentences = re.split('[.!?]', text)
	return sentences

def count_words_in_sentences(sentences: list) -> list:
	count_words_list = list()
	for sentence in sentences:
		count_words_list.append(len(sentence.split()))
	return count_words_list

def mean_words(count_words_list: int) -> int:
	return(mean(count_words_list))

def median_words(count_words_list: int) -> int:
	return(median(count_words_list))

def count_words(sentences: list) -> dict:
	words_dict = dict()
	for sentence in sentences:
		words = sentence.split()
		for word in words:
			if word in words_dict:
				words_dict[word] += 1
			else:
				words_dict[word] = 1
	words_dict.pop('', None)
	return words_dict

def get_ngrams(sentences: list, n: int) -> dict:
	ngrams = dict()
	for sentence in sentences:
		words = sentence.split()
		for i in range(len(words)-n+1):
			temp = [words[j] for j in range(i,i+n)]
			ngram = " ".join(temp)
			if ngram in ngrams:
				ngrams[ngram] += 1
			else:
				ngrams[ngram] = 1
	ngrams = dict(sorted(ngrams.items(), key = lambda item: item[1], reverse = True))
	return ngrams

def print_info(text: str, k: int, n: int):
	sentences = spliting(text)
	words_dict = count_words(sentences)
	for word in words_dict:
		print(f"{word} = {words_dict[word]}")
	print("---")
	count_words_list = count_words_in_sentences(sentences)
	print("average count = {}".format(mean_words(count_words_list)))
	print("median count = {}".format(median_words(count_words_list)))
	print("---")
	ngrams = get_ngrams(sentences, n)
	if not ngrams:
		print(f"No {n}-grams")
	else:
		print(f"{n}-grams")
		s = min(k,len(ngrams))
		for i in range(min(k,len(ngrams))):
			print("{} = {}".format(list(ngrams)[i], list(ngrams.values())[i]))

def main():
	try:
		text, k, n = parsedata()
		print_info(text, int(k), int(n))
	except:
		print("Inalid input!")

if __name__=="__main__":
	main()