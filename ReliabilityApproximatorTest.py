from unittest import TestCase
from ReliabilityApproximator import ReliabilityApproximator


class TestReliabilityApproximator(TestCase):
    @classmethod
    def setUpClass(cls):
        cls._instance = ReliabilityApproximator(
            "./test_file.txt", 10)

    def test_reliability_approximation(self):
        self.assertEqual(1, self._instance.approximate(2))

    def test_emprical_pdf(self):
        self._instance.compute_empirical_pdf()
        for item in self._instance.binned_data:
            if item['starts'] == 0:
                self.assertEqual(1, item['content'])
            elif item['starts'] == 10.0:
                self.assertEqual(1, item['content'])
            elif item['starts'] == 22.0:
                self.assertEqual(1, item['content'])
            elif item['starts'] == 34.0:
                self.assertEqual(0, item['content'])
            elif item['starts'] == 46.0:
                self.assertEqual(1, item['content'])
            elif item['starts'] == 58.0:
                self.assertEqual(0, item['content'])
            elif item['starts'] == 70.0:
                self.assertEqual(0, item['content'])
            elif item['starts'] == 82.0:
                self.assertEqual(1, item['content'])
            elif item['starts'] == 94.0:
                self.assertEqual(0, item['content'])
            elif item['starts'] == 106.0:
                self.assertEqual(0, item['content'])
            elif item['starts'] == 118.0:
                self.assertEqual(1, item['content'])

    def test_chi_test(self):
        self.assertAlmostEquals(1, self._instance.distribution_fitting(False, True, None, [1, 1, 1, 0.001, 1, 0.001, 0.001, 1, 0.001, 0.001, 1], None)[0],10)

    def test_k_test(self):
        print self._instance.distribution_fitting(True, False, 'uniform', None, [9, 130])
