import unittest

from classrank.filters.collabfilter import CollaborativeFilter
import numpy as np
from scipy import sparse

class TestSVDFilter(unittest.TestCase):
    def setUp(self):
        self.data = [[2.5, 3.5, 3.0, 3.5, 2.5, 3.0],[3.0, 3.5, 1.5, 5.0, 3.0, 3.5],[2.5, 3.0, None, 3.5, 4.0, None],[None, 3.5, 3.0, 4.0, 4.5, 2.5], [3.5, 4.0, 2.0, 3.0, 3.0, 2.0], [3.0, 4.0, None, 5.0, 3.0, 3.5], [None, 4.5, None, 4.0, None, 1.0]]
        self.fltr = CollaborativeFilter(self.data, 1)
    
    def test_update_value(self):
        self.fltr.updateValue(2, 2, 10)
        self.assertEqual(10,self.fltr.getData()[2][2])

    def test_get_recommendation(self):
        recom = self.fltr.getRecommendation(2,2)
        self.assertIsNot(recom, None)
    
    def test_force_model_update(self):
        model = self.fltr.getModel()
        self.fltr.updateValue(2, 2, 10)
        self.assertListNotEqual(model, self.fltr.getModel())

    def test_get_data(self):
        self.assertListEqual(self.data, self.fltr.getData())

    def test_get_model(self):
        temp = np.array([1])
        self.assertIsInstance(self.fltr.getModel(), type(temp))

    def test_sparseify_data(self):
        temp = sparse.dok_matrix([[1, 0],[1, 0]])
        self.assertIsInstance(self.fltr.getSparseData(), type(temp))
        
        temp2 = self.fltr.getSparseData()

        self.fltr.updateValue(2, 2, 10)
        self.fltr.getRecommendation(2, 2)
        self.assertIsInstance(self.fltr.getSparseData(), type(temp))
        self.assertListNotEqual(self.fltr.getSparseData(), temp2)

        temp3 = self.fltr.getSparseData()

        self.fltr.updateValue(2, 2, 20)
        self.fltr.forceModelUpdate()
        self.assertIsInstance(self.fltr.getSparseData(), type(temp))
        self.assertListNotEqual(self.fltr.getSparseData(), temp2)
        self.assertListNotEqual(self.fltr.getSparseData(), temp3)

    def test_is_updated(self):
        self.assertFalse(self.fltr.getUpdated())
        
        self.fltr.updateValue(2, 2, 10)
        self.assertTrue(self.fltr.getUpdated())

        self.fltr.getRecommendation(2, 2)
        self.assertFalse(self.fltr.getUpdated())

        self.fltr.updateValue(2, 2, 20)
        self.assertTrue(self.fltr.getUpdated())
        
        self.fltr.forceModelUpdate()
        self.assertFalse(self.fltr.getUpdated())

    def assertListNotEqual(self, list1, list2):
        self.assertEqual(len(list1), len(list2))
        for i in range(len(list1)):
            self.assertEqual(len(list1[i]), len(list2[i]))
            for j in range(len(list1[i])):
                self.assertEqual(list1[i][j], list2[i][j])

