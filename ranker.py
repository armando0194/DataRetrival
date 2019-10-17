import pandas as pd 
from nltk.tokenize import sent_tokenize, word_tokenize
import gensim
import string
import numpy as np 

class Ranker:
    def __init__(self):
        self.model = gensim.models.KeyedVectors.load_word2vec_format('./GoogleNews-vectors-negative300.bin', binary=True)
        print(self.model.wv.vocab["word"].count)
    
    def get_rank(self):
        self.build_centroids()
        pass
    
    def build_centroids(self):
        data = pd.read_csv("exploit.csv", header=None) 
        doc_centroids = []
        for index, row in data.iterrows():
            #TODO change this in the future to do every thing in row
            # TODO might need to mve to its own class
            bag_of_vectors = []
            for i in range(3,4):
                # TODO Extract this to a method to call it for every col in row and alos in query
                content = self.remove_punctuation(row[i])
                words = word_tokenize(content) 
                
                for word in words:
                    bag_of_vectors.append(self.model.wv[word.lower()])
            bag_of_vectors = np.array(bag_of_vectors)
            print(bag_of_vectors.shape)
            print(bag_of_vectors)
            print(np.average(bag_of_vectors, axis=1).shape)
            print(np.average(bag_of_vectors, axis=1))
            
            break
            
               
    
    def remove_punctuation(self, s):
        """Given a string, replaces punctuation with blanks
        
        Args:
            s (str): string to replace puntuation
        
        Returns:
            str: string without punctuation
        """
        return s.translate(str.maketrans('', '', string.punctuation))




        
    def run_query(q):
        pass