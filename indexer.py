from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords 

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import Pipeline
from sklearn.metrics import pairwise_distances

import pickle
import gensim
import string
import json

from util import Util
from config import Config

import numpy as np 
import pandas as pd 

class Indexer:
    VECTOR_DIM = 300
    
    def __init__(self):
        model_path = Util.rel2abs(Config.MODEL_PATH)
        self.model = gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=True)
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
    
    def sanitize_text(self, t):
        return [self.stem(text) for text in t]

    def stem(self, s):
        """ Stems words and removes punctuation
        """
        words = word_tokenize(self.remove_punctuation(s))
        stop_words = set(stopwords.words('english')) 
        words = [w for w in words if not w in stop_words] 

        new_doc = ''
        for w in words:
            new_doc += self.stemmer.stem(w) + ' '
            
        return new_doc

    def build_transformers(self):
        """ Build tfidf transformers
        """
        
        exploits = Util.load_json(Config.PATH_EXPLOITS)
        docs = []
        doc_names = []
        
        for exploit_key, exploit in exploits.items():
            doc_names.append(exploit_key)
            docs.append(' '.join(str(x) for x in exploit.values()))
        
        docs = self.sanitize_text(docs)
        
        tf = TfidfVectorizer(analyzer='word')
        tfidf_matrix =  tf.fit_transform(docs)
        
        with open("./data/tdif.sav",'wb') as outfile:
            pickle.dump(tf, outfile)
        
        with open("./data/dm.sav",'wb') as outfile:
            pickle.dump(tfidf_matrix, outfile)
        
        with open("./data/doc_names.sav",'wb') as outfile:
            pickle.dump(doc_names, outfile)


    def build_centroids(self):
        exploits = Util.load_json(Config.PATH_EXPLOITS)
        centroids = dict()
        centroids['centroids'] = []
        centroids['document_id'] = []
   
        for exploit_key, exploit in exploits.items():
            bag_of_vectors = []
            
            for exploit_feature, exploit_feature_data in exploit.items():
                bag_of_vectors += self.get_bag_of_vectors(exploit_feature_data)
            
            bag_of_vectors = np.array(bag_of_vectors)
            centroid = np.average(bag_of_vectors, axis=0)
            
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