from util import Util
from config import Config
from handler.indexer import Indexer
from sklearn.metrics import pairwise_distances
import numpy as np 
import string
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords 
import sys 

sys.setrecursionlimit(20000)
class Ranker:
    
    def __init__(self):
        self.indexer = Indexer()
        self.centroids = Util.load_json(Config.CENTROIDS_PATH)
        self.exploits = Util.load_json(Config.PATH_EXPLOITS)
        self.td_idf = Util.load_pickle(Config.TFIDF_TRANS_PATH)
        self.doc_names = Util.load_pickle(Config.DOC_NAMES_PATH)
        self.dm = Util.load_pickle(Config.DM_PATH)
        self.num_results = 50

    def query_tf_idf(self, q: str):
        q = self.stem(q)
        query_vector_tfidf =  self.td_idf.transform([q])
        dist_tf = pairwise_distances(query_vector_tfidf, self.dm, metric='cosine', n_jobs=-1)[0]
        idx = np.argsort(dist_tf)
        res = []
        for i in range(self.num_results):

            res.append( self.doc_names[idx[i]] )

        return res
    
    def remove_punctuation(self, s):
        return s.translate(str.maketrans('','',string.punctuation))

    def stem(self, s):
        """ Stems words and removes punctuation
        """
        ps = PorterStemmer()
        words = word_tokenize(self.remove_punctuation(s))
        stop_words = set(stopwords.words('english')) 
        words = [w for w in words if not w in stop_words] 

        new_doc = ''
        for w in words:
            new_doc += ps.stem(w) + ' '
            
        return new_doc
        
    def query_centroids(self, q: str):
        q_cen = self.get_query_centroid(q)
        x_train = np.array(self.centroids['centroids'])    
        y_train = np.array(self.centroids['document_id'])
        q_cen = q_cen.reshape((1,300))
        dists = self.compute_distances(x_train, q_cen)
        dists = dists.reshape((dists.shape[1],))
        idx = np.argsort(dists)
        res = []
        for i in range(self.num_results):
            res.append( self.doc_names[idx[i]] )
  
        return res
        
    def get_query_centroid(self, q):
        bag_of_vectors = self.indexer.get_bag_of_vectors(q)
        bag_of_vectors = np.array(bag_of_vectors)
        query_centroid = np.average(bag_of_vectors, axis=0)
        return query_centroid
    
    def compute_distances(self, x_train, x_test):
        dists = -2 * np.dot(x_test, x_train.T) + np.sum(x_train**2,    axis=1) + np.sum(x_test**2, axis=1)[:, np.newaxis]
        return dists
