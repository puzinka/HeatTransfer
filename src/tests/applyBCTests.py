import unittest
import sys
sys.path.append('../')
from applyBC import nullMatrixRow, applyBCtoF

class applyBCTests(unittest.TestCase):

    def test_nullMatrixRow(self):

        Matrix = [
            [1,2,3,4],
            [5,6,7,8],
            [9,10,11,12],
            [13,14,15,16],
        ]
        BC = {5: [2], 20: [4]}
        
        ExpectMatrix = [
            [1,2,3,4],
            [0,6,0,0],
            [9,10,11,12],
            [0,0,0,16],
        ]
        
        self.assertEqual(nullMatrixRow(Matrix, BC), ExpectMatrix)

    def test_applyBCtoF(self):
        
        Matrix = [
            [55, 0, 0, 0, 0],
            [-46, 140, -46, 0, 0],
            [4, -46, 110, -46, 4],
            [0,0, -46, 142, -46],
            [0,0, 0, 0, 65]
        ]
        BC = {150: [1], 40: [5]}
        
        Force = [
            500,
            2000,
            1000,
            2000,
            900
        ]
        
        F = applyBCtoF(Matrix, Force, BC)
        
        expectedF = [
            8250,
            8900,
            240,
            3840,
            2600
        ]
        
        self.assertEqual(F, expectedF)




if __name__ == '__main__':
    unittest.main()

