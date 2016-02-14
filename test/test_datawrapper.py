import unittest

from classrank.filters.datawrapper import DataWrapper
class TestDataWrapper(unittest.TestCase):
   
    def setUp(self):
        self.dataset = {
            'Lisa Rose': {
                'Lady in the Water': 2.5,
                'Snakes on a Plane': 3.5,
                'Just My Luck': 3.0,
                'Superman Returns': 3.5,
                'You, Me and Dupree': 2.5,
                'The Night Listener': 3.0
            },
            'Gene Seymour': {
                'Lady in the Water': 3.0,
                'Snakes on a Plane': 3.5,
                'Just My Luck': 1.5,
                'Superman Returns': 5.0,
                'The Night Listener': 3.0,
                'You, Me and Dupree': 3.5
            },
            'Michael Phillips': {
                'Lady in the Water': 2.5,
                'Snakes on a Plane': 3.0,
                'Superman Returns': 3.5,
                'The Night Listener': 4.0
            },
            'Claudia Puig': {
                'Snakes on a Plane': 3.5,
                'Just My Luck': 3.0,
                'The Night Listener': 4.5,
                'Superman Returns': 4.0,
                'You, Me and Dupree': 2.5
            },
            'Mick LaSalle': {
                'Lady in the Water': 3.0,
                'Snakes on a Plane': 4.0,
                'Just My Luck': 2.0,
                'Superman Returns': 3.0,
                'The Night Listener': 3.0,
                'You, Me and Dupree': 2.0
            },
            'Jack Matthews': {
                'Lady in the Water': 3.0,
                'Snakes on a Plane': 4.0,
                'The Night Listener': 3.0,
                'Superman Returns': 5.0,
                'You, Me and Dupree': 3.5
            },
            'Toby': {
                'Snakes on a Plane':4.5,
                'You, Me and Dupree':1.0,
                'Superman Returns':4.0
            }
        }
        self.wrapper = DataWrapper(self.dataset)

        def test_create_lookups(self):
            self.assertIsInstance(self.wrapper.getInstanceLookup(), {})
            self.assertIsInstance(self.wrapper.getFeatureLookup(), {})

        def test_getters(self):
            self.assertIsInstance(self.wrapper.getInstanceLookup(), {})
            self.assertNotEqual(self.wrapper.getInstanceLookup(), {})

            self.assertIsInstance(self.wrapper.getFeatureLookup(), {})
            self.assertNotEqual(self.wrapper.getFeatureLookup(), {})

            self.assertIsEqual(self.wrapper.getDataDict(), self.dataset)
            
            self.assertNotEqual(self.wrapper.getData(), [[None],[None],[None],[None],[None],[None],[None]])

        def test_add_data(self):
            dataDict = self.wrapper.getDataDict()
            tempData = self.wrapper.getData()

            instance = {'Casey' : { 'Snakes on a Plane': 5.0, 'Superman Returns' : 3.4}}

            self.wrapper.addData(instance)
            self.assertNotEqual(dataDict, self.wrapper.getDataDict())
            self.assertNotEqual(tempData, self.wrapper.getData())

        def test_convert_data(self):
            self.assertNotEqual(self.wrapper.getData(), [[None],[None],[None],[None],[None],[None],[None]])
