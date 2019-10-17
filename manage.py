# # importing all necessary modules
# from nltk.tokenize import sent_tokenize, word_tokenize
# import warnings

# warnings.filterwarnings(action = 'ignore')

# import gensim
# from gensim.models import Word2Vec

# #  Reads ‘alice.txt’ file
# sample = open("C:\\Users\\Admin\\Desktop\\alice.txt", "r")
# s = sample.read()

# # Replaces escape character with space
# f = s.replace("\n", " ")

# data = []

# # iterate through each sentence in the file
# for i in sent_tokenize(f):
#     temp = []

#     # tokenize the sentence into words
#     for j in word_tokenize(i):
#         temp.append(j.lower())

#     data.append(temp)

# model = gensim.models.Word2Vec.load_word2vec_format('./model/GoogleNews-vectors-negative300.bin', binary=True)

# ## for document calculate its centroid

# # for every query calculate its centroid and get the similarity
import argparse
import sys
from scrapper import ExploitDBScrapper
from ranker import Ranker
from os import path


def scrap(num_pages, timeout):
    scrapper = ExploitDBScrapper(num_pages, timeout)
    scrapper.scrap()


def query(q):
    if not path.exists("./exploit.csv"):
        print('please run scrap command first')
        return
    ranker = Ranker()
    #ranker.get_rank()
    print(q)
    

def main():
    FUNCTION_MAP = {'scrap': scrap, 'query': query}
    parser = argparse.ArgumentParser()

    parser.add_argument('command', choices=FUNCTION_MAP.keys(), type=str,
                        help='an integer for the accumulator')
    parser.add_argument('--num_pages', type=int, required=False,
                        help='number of pages that will be scrapped')
    parser.add_argument('--timeout', type=int, required=False,
                        help='time to wait between calls')
    parser.add_argument('--query', type=str, required=False,
                        help='dcument query')

    args = parser.parse_args()
    func = FUNCTION_MAP[args.command]
    
    if 'scrap' in args.command:
        if not args.num_pages or not args.timeout:
            print ('Please provide --num_pages and --timeout. Run with -h flag for help')
        else:
            func(args.num_pages, args.timeout)
    else:
        if not args.query:
            print ('Please provide --query. Run with -h flag for help')
        else:
            func(args.query)


if __name__ == "__main__":
    main()
