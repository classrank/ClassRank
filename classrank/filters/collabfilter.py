import numpy as np
from sklearn.decomposition import TruncatedSVD 
from scipy import sparse
from classrank.filters.datawrapper import DataWrapper
class CollaborativeFilter:
    #This takes in a matrix
    def __init__(self, data=dict(), numRecommendations=1, db=None, metric="rating", school="gatech"):
        self.dataset = DataWrapper(instances=data, db=db, school=school, metric=metric)
        self.updated = False
        self.sparsedata = None
        self.sparseifyData()
        try:
            self.svd = TruncatedSVD(n_components=numRecommendations)
            self.model = self.svd.inverse_transform(self.svd.fit_transform(self.sparsedata))
        except ValueError:
            self.svd = None
            self.model = None
            raise ValueError("Not enough ratings for predictions")
    
    def getRecommendation(self, instances):
        if(self.updated):
            self.sparseifyData()
            self.model = self.svd.inverse_transform(self.svd.fit_transform(self.sparsedata))
            self.updated = False
        ret = {}
        for instance in instances:
            values = {}
            for feature in instances[instance]:
                try:
                    row = self.dataset.getRow(instance)
                    column = self.dataset.getColumn(feature)
                    values[feature] = self.model[row][column]
                except KeyError:
                    values[feature] = None
            ret[instance] = values
        return ret

    def updateValues(self, instances):
        self.dataset.addData(instances)
        self.updated = True

    def forceModelUpdate(self):
        self.updated = False
        self.sparseifyData()
        self.model = self.svd.inverse_transform(self.svd.fit_transform(self.sparsedata))

    def sparseifyData(self):
        data = self.dataset.getData()
        sparsematrix = sparse.dok_matrix((len(data), len(data[0])))
        for i in range(len(data)):
            for j in range(len(data[i])):
                if data[i][j] is not None:
                    sparsematrix[i, j] = data[i][j]
        self.sparsedata = sparsematrix

    def getSparseData(self):
        return self.sparsedata

    def getModel(self):
        return self.model

    def getData(self, *args):
        if len(args) == 2:
            return self.dataset.getData(args[0], args[1])
        else:
            return self.dataset.getData()

    def getUpdated(self):
        return self.updated

    def getDataDict(self):
        return self.dataset.getDataDict()
