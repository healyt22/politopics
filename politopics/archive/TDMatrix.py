import os
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import CountVectorizer
from scipy.sparse.linalg import svds, eigs
import seaborn as sb
import matplotlib.pyplot as plt

from preprocess import *

class TDMatrix():
    def __init__(self):
        crook_dirs = os.listdir('tweet_data')
        self.clean_tweets = {}
        for crook in crook_dirs:
            crook_obj = Preprocess(crook)
            self.clean_tweets.update(crook_obj.clean_tweets)
        self.docs = self.clean_tweets.keys()
        log.info('{0} Tweets Processed'.format(len(self.clean_tweets)))
        self.construct_td_matrix()

    def construct_td_matrix(self):
        '''
        Construct a TD Matrix from inputted tweets data
        TODO: Implement term frequency - inverse document frequency
              (tf-idf) statistic
        '''
        log.info("Constructing Term-Document Matrix")
        indptr = [0]
        indices = []
        data = []
        self.vocabulary = {}
        for d in self.docs:
            for term in self.clean_tweets[d]:
                index = self.vocabulary.setdefault(term, len(self.vocabulary))
                indices.append(index)
                data.append(1)
            indptr.append(len(indices))
        self.td_matrix = csr_matrix((data, indices, indptr), dtype=int).asfptype()
        return(self.td_matrix, self.vocabulary)

    def svd(self, components):
        log.info("Singular Value Decomposition with {0} Components".format(components))
        self.u, self.s, self.vt = svds(self.td_matrix, k=components)
        return(self.u, self.s, self.vt)

    def plot_2d(self):
        if self.u.shape[1] == 2:
            sb.set_style('darkgrid')
            plt.scatter(self.u[:,0], self.u[:,1])
            plt.show()
        else:
            log.ERROR('Can only plot in 2 dimensions - choose less principal components')

    def main(self, components):
        x.svd(components)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-c", "--components",
        help="Number of principal components to use")
    args = parser.parse_args()
    TDMatrix().main(args.components)
