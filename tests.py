
import unittest
from clustering import clustering, Point

class CalcTestCase(unittest.TestCase):
    def setUp(self):
        super(CalcTestCase, self).setUp()


    def tearDown(self):
        super(CalcTestCase, self).tearDown()

    def testBasic(self):
        point_objs = []
        for i in range(5):
            for j in range(10):
                point_objs.append(Point(i*10000 + j,i*10000 + j))

        km = clustering(point_objs,5)
        clusters = km.k_means(False)

        self.assertEqual(len(clusters), 5)

