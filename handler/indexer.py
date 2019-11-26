import pandas as pd 
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.porter import PorterStemmer
import gensim
import string
import json

from util import Util
from config import Config
import numpy as np 

class Indexer:
    VECTOR_DIM = 300
    
    def __init__(self):
        self.stemmer = PorterStemmer()
    
    def get_word_embeddings(self, w):
        try:
            return self.model.wv[w.lower()]
        except:
            return np.zeros((self.VECTOR_DIM,))
 
    
    def get_bag_of_vectors(self, s):
        bag_of_vectors = []
        s = self.remove_punctuation(s)
        words = [self.stemmer.stem(word) for word in word_tokenize(s)]
        
        for word in words:
            bag_of_vectors.append(self.get_word_embeddings(word))
            
        return bag_of_vectors
        
    def build_centroids(self):
        model_path = Util.rel2abs(Config.MODEL_PATH)
        self.model = gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=True)
        
        exploits = Util.load_json()
        centroids = dict()
        centroids['centroids'] = []
        centroids['document_id'] = []
   
        for exploit_key, exploit in exploits.items():
            bag_of_vectors = []
            
            for exploit_feature, exploit_feature_data in exploit.items():
                bag_of_vectors += self.get_bag_of_vectors(exploit_feature_data)
            
            bag_of_vectors = np.array(bag_of_vectors)
            centroid = np.average(bag_of_vectors, axis=0)
            
            # print("Testing pruposes")
            # print("Bag og vectors shape")
            # print(bag_of_vectors.shape)
            # print("Centroid shape")
            # print(centroid.shape)
            
            centroids['centroids'].append(centroid.tolist())
            centroids['document_id'].append(exploit_key)
    
        Util.save_json(Config.CENTROIDS_PATH, centroids)
                
    def save_json(self, centroids):
        """Saves exploits in a josn file
        """
        with open(Config.CENTROIDS_PATH, 'w') as exploit_file:
            json.dump(centroids, exploit_file)
    
    def remove_punctuation(self, s):
        """Given a string, replaces punctuation with blanks
        
        Args:
            s (str): string to replace puntuation
        
        Returns:
            str: string without punctuation
        """
        return s.translate(str.maketrans('', '', string.punctuation))