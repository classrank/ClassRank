import numpy as np
from sklearn.decomposition import TruncatedSVD 
from scipy import sparse
class CollaborativeFilter:
    #This takes in a matrix
    def __init__(self, data, numRecommendations):
        self.dataset = data
        self.updated = False
        self.sparsedata = None
        self.sparseifyData()
        self.svd = TruncatedSVD()
        self.model = self.svd.inverse_transform(self.svd.fit_transform(self.sparsedata))

    def getRecommendation(self, row, column):
        if(self.updated):
            self.sparseifyData()
            self.model = self.svd.inverse_transform(self.svd.fit_transform(self.sparsedata))
            self.updated = False
        return self.model[row][column]

    def updateValue(self, row, column, value):
        self.dataset[row][column] = value
        self.updated = True

    def forceModelUpdate(self):
        self.updated = False
        self.sparseifyData()
        self.model = self.svd.inverse_transform(self.svd.fit_transform(self.sparsedata))

    def sparseifyData(self):
        sparsematrix = sparse.dok_matrix((len(self.dataset), len(self.dataset[0])))
        for i in range(len(self.dataset)):
            for j in range(len(self.dataset[i])):
                if self.dataset[i][j] is not None:
                    sparsematrix[i, j] = self.dataset[i][j]
        self.sparsedata = sparsematrix

    def getSparseData(self):
        return self.sparsedata

    def getModel(self):
        return self.model

    def getData(self):
        return self.dataset

    def getUpdated(self):
        return self.updated
