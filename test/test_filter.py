import unittest

from classrank.filters.collabfilter import CollaborativeFilter
import numpy as np
from scipy import sparse

class TestSVDFilter(unittest.TestCase):
    
    def setUp(self):
        self.data = {
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
        self.instance = 'Gene Seymour'
        self.feature = 'Snakes on a Plane'
        self.testInstance = { 'Gene Seymour': { 'Snakes on a Plane': 10} }
        self.recTester = { 'Gene Seymour': ['Snakes on a Plane'] }
        self.fltr = CollaborativeFilter(self.data, 1)
        self.test2Instance = {'Gene Seymour' : {'Snakes on a Plane' : 20}}
    
    def test_update_value(self):
        self.fltr.updateValues(self.testInstance)
        self.assertEqual(10,self.fltr.getDataDict()[self.instance][self.feature])

    def test_get_recommendation(self):
        recom = self.fltr.getRecommendation(self.recTester)
        self.assertIsNot(recom, None)
    
    def test_force_model_update(self):
        model = self.fltr.getModel()
        self.fltr.updateValues(self.testInstance)
        self.fltr.forceModelUpdate()
        self.assertTrue(self.listNotEqual(model, self.fltr.getModel()))

    def test_get_data_dict(self):
        self.assertEqual(self.data, self.fltr.getDataDict())
    
    def test_get_data(self):
        self.assertIsNot(self.fltr.getData("Gene Seymour", "Snakes on a Plane"), None)
        self.assertIsInstance(self.fltr.getData(), type([]) )

    def test_get_model(self):
        temp = np.array([1])
        self.assertIsInstance(self.fltr.getModel(), type(temp))

    def test_sparseify_data(self):
        temp = sparse.dok_matrix([[1, 0],[1, 0]])
        self.assertIsInstance(self.fltr.getSparseData(), type(temp))
        
        temp2 = self.fltr.getSparseData()

        self.fltr.updateValues(self.testInstance)
        self.fltr.getRecommendation(self.recTester)
        self.assertIsInstance(self.fltr.getSparseData(), type(temp))
        self.assertTrue(self.npListNotEqual(self.fltr.getSparseData(), temp2))

        temp3 = self.fltr.getSparseData()
        self.fltr.updateValues(self.test2Instance)
        self.fltr.forceModelUpdate()
        self.assertIsInstance(self.fltr.getSparseData(), type(temp))
        self.assertTrue(self.npListNotEqual(self.fltr.getSparseData(), temp2))
        self.assertTrue(self.npListNotEqual(self.fltr.getSparseData(), temp3))

    def test_is_updated(self):
        self.assertFalse(self.fltr.getUpdated())
        
        self.fltr.updateValues(self.testInstance)
        self.assertTrue(self.fltr.getUpdated())

        self.fltr.getRecommendation(self.recTester)
        self.assertFalse(self.fltr.getUpdated())

        self.fltr.updateValues(self.test2Instance)
        self.assertTrue(self.fltr.getUpdated())
        
        self.fltr.forceModelUpdate()
        self.assertFalse(self.fltr.getUpdated())

    def npListNotEqual(self, list1, list2):
        if list1.get_shape()[0] != list2.get_shape()[0] or list1.get_shape()[1] != list2.get_shape()[1]:
            return True
        for i in range(list1.get_shape()[0]):
            for j in range(list1.get_shape()[1]):
                if list1[i, j] != list2[i, j]:
                    return True
        return False

    def listNotEqual(self, list1, list2):
        if len(list1) != len(list2):
            return True
        for i in range(len(list1)):
            if len(list1[i]) != len(list2[i]):
                return True
            for j in range(len(list1[i])):
                if list1[i][j] != list2[i][j]:
                    return True
        return False
