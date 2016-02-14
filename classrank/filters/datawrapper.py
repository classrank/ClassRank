class DataWrapper:
    def __init__(self, instances):
        self.dataDict = instances
        self.instanceLookup = {}
        self.featureLookup = {}
        self.createLookups()
        self.data = [[None for feature in self.featureLookup] for instance in self.instanceLookup]
        self.convertData()

    def createLookups(self):
        instanceCounter = 0
        featureCounter = 0
        for instance in self.dataDict:
            if instance not in self.instanceLookup:
                self.instanceLookup[instance] = instanceCounter
                instanceCounter += 1
                for feature in self.dataDict[instance]:
                    if feature not in self.featureLookup:
                        self.featureLookup[feature] = featureCounter
                        featureCounter += 1

    def convertData(self):
        for instance in self.dataDict:
            for feature in self.dataDict[instance]:
                self.data[self.instanceLookup[instance]][self.featureLookup[feature]] = self.dataDict[instance][feature]

    def addData(self, instances):
        #update the data dictionary
        for instance in instances:
            if instance in self.dataDict:
                self.dataDict[instance].update(instances[instance])
            else:
                self.dataDict[instance] = instances[instance]
        #probably more taxing than necesarry
        self.createLookups()
        self.convertData()

    def getData(self):
        return self.data

    def getInstanceLookup(self):
        return self.instanceLookup

    def getFeatureLookup(self):
        return self.featureLookup

    def getDataDict(self):
        return self.dataDict


