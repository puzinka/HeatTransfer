import unittest
import sys
sys.path.append('../')
from operationsMatrix import sumVectors

class operationsMatrixTests(unittest.TestCase):

    def test_sumVector(self):

        A = [1, 2, 3]
        B = [3, 2, 1]
        C = [4, 4, 4]
        self.assertEqual(sumVectors(A, B), C)

    def test_sumVector_exeption(self):

        A = [1, 2, 3]
        B = [3, 2, 1, 4]

        with self.assertRaises(Exception) as context:
            sumVectors(A, B)

    # def test_multiplyVector(self):

    #     A = [1, 2, 3]
    #     B = [3, 2, 1]
    #     C = [4, 4, 4]
    #     self.assertEqual(multiplyVector(A, B), C)



if __name__ == '__main__':
    unittest.main()

