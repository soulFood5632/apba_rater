import unittest
import rating_predictor as rp


class MyTestCase(unittest.TestCase):
    def test_scaler_1(self):
        self.assertEqual(rp.scale_to(0.9, 10, 0), 9)

    def test_scaler_2(self):
        self.assertEqual(rp.scale_to(1, 10, 0), 10)

    def test_scaler_3(self):
        self.assertEqual(rp.scale_to(0.82, 10, 0), 8)

    def test_scaler_4(self):
        self.assertEqual(rp.scale_to(0.43, 10, 0), 4)

    def test_scaler_5(self):
        self.assertEqual(rp.scale_to(0.38, 10, 0), 4)

    def test_scaler_6(self):
        self.assertEqual(rp.scale_to(0.38, 5, 1), 3)



if __name__ == '__main__':
    unittest.main()
