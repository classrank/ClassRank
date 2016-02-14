class DataWrapper:
    def __init__(self, instances):
        self.dataDict = instances
        self.instanceLookup = {}
        self.featureLookup = {}
        createLookups()
        self.data = [[None for feature in self.featureLookup] for instance in instanceLookup]
        convertData()
    
    def createLookups(self):
        instanceCounter = 0
        featureCounter = 0
        for instance in self.datadict:
            if instance not in self.instanceLookup:
                instanceLookup[instance] = instanceCounter
                instanceCounter += 1
                for feature in self.dataDict[instance]:
                    if feature not in self.featureLookup:
                        featureLookup[feature] = featureCounter
                        featureCounter += 1

    def convertData(self):
        for instance in self.dataDict:
            for feature in self.dataDict[instance]:
                data[self.instanceLookup[instance]][self.featureLookup[feature]] = self.dataDict[instance][feature]

    def addData(self, instances):
        #update the data dictionary
        for instance in instances:
            if instance in self.dataDict:
                self.dataDict[instance].update(instances[intance])
            else:
                self.dataDict[instance] = instances[instance]
        #probably more taxing than necesarry
        createLookups()
        convertData()

    def getData(self):
        return self.data

    def getInstanceLookup(self):
        return self.instanceLookup

    def getFeatureLookup(self):
        return self.featureLookup

    def getDataDict(self):
        return self.dataDict


