from unittest import TestCase
from ReliabilityApproximator import ReliabilityApproximator


class TestReliabilityApproximator(TestCase):
    @classmethod
    def setUpClass(cls):
        cls._instance = ReliabilityApproximator("./test_file.txt")
        cls._instance.bins_cardinality = 10

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

    def test_empirical_cdf(self):
        self._instance.compute_empirical_pdf()
        self.assertEqual(0, self._instance.empirical_cdf(8))
        self.assertEqual(1, self._instance.empirical_cdf(200))
        self.assertEqual(4.0/6, self._instance.empirical_cdf(65))
