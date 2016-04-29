from classrank.database.wrapper import Query
import pprint
class DataWrapper:
    def __init__(self, instances=dict(), db=None, school="gatech", metric="rating"):
        self.db = db
        self.dataDict = instances
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
        with Query(self.db) as query:
            for student in query.query(self.db.student).filter(self.db.school.abbreviation==self.school).all():
                results = query.query(self.db.rating, self.db.section).filter(self.db.rating.student_id == student.uid).\
                    filter(self.db.rating.section_id==self.db.section.uid).all() #a tuple of lists
                #results = list(zip(*results)) #a list of tuples
                instance = {}
                for result in results:
                    courseName = query.query(self.db.course).filter(self.db.course.uid==result[1].course_id).first()
                    courseName = courseName.name
                    rating = result[0].__getattribute__(self.metric)
                    #if self.metric == "rating":
                    #    rating = result[0][0].rating
                    #elif self.metric == "grade":
                    #    rating = result[0][0].grade
                    #elif self.metric == "workload":
                    #    rating = result[0][0].workload
                    #elif self.metric == "difficulty":
                    #    rating = result[0][0].difficulty
                    instance[courseName] = rating
                self.dataDict[student.uid] = instance
