import classrank.database.wrapper as db
class DataWrapper:
    def __init__(self, instances=dict(), db=None, school="gatech", metric="rating"):
        self.db = db
        self.datadict = instances
        if db:
            self.school = school
            self.metric = metric
            self.queryDB()
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

    def getData(self, *args):
        if len(args) == 2:
            return self.data[self.instanceLookup[args[0]]][self.featureLookup[args[1]]]
        else:
            return self.data
    
    def getInstanceLookup(self):
        return self.instanceLookup

    def getFeatureLookup(self):
        return self.featureLookup

    def getDataDict(self):
        return self.dataDict
        
    def getRow(self, instance):
        return self.instanceLookup[instance]

    def getColumn(self, feature):
        return self.featureLookup[feature]
    
    def queryDB(self):
        query = wrapper.Query(self.db)
        for student in query.query(self.db.Student).filter(self.db.Student==self.school).all():
            results = query.query(self.db.Rating, self.db.Section, self.db.Course).filter(self.db.Rating.student_id == student.uid).\
                filter(self.db.Rating.section_id==self.db.Course.section_id).all() #a tuple of lists
            results = zip(*results) #a list of tuples
            instance = {}
            for result in results:
                courseName = query.query(self.db.Course).filter(self.db.Course.uid==result[1].course_id).first()
                courseName = courseName.name
                if metric == "rating":
                    rating = result[0][0].rating
                elif metric == "grade":
                    rating = result[0][0].grade
                elif metric == "workload":
                    rating = result[0][0].workload
                elif metric == "difficulty":
                    rating = result[0][0].difficulty
                instance[courseName] = rating
            self.instances[student.uid] = instance
