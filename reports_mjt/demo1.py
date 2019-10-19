import unittest

class test(unittest.TestCase):
    def setUp(self):
        print('99999999')

    def test_something(self):
        print(8888)
        self.assertAlmostEqual(True, True)

    def tearDown(self):
        print('000000')

if __name__ == '__main__':
    unittest.main()