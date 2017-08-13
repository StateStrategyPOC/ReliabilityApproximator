#!/usr/bin/env python
import math
import os.path as path
import sys

from scipy.stats import kstest, anderson


class ReliabilityApproximator:
    def __init__(self, data_file_path):
        self.data_file_path = data_file_path
        self.bins_cardinality = 100
        self.data = []
        self.data_len = None
        self.interval_size = None
        self.binned_data = []

    def approximate(self, time):
        counter = 0
        with open(self.data_file_path) as f:
            for index, line in enumerate(f):
                if int(line) <= time:
                    counter += 1

        result = 1 - float(counter) / index
        return result

    def distributionFitting(self, useKTest, useChiTest, useADTest, cdfGenerator):
        with open(self.data_file_path) as f:
            data = f.readlines()

        if useKTest:
            print("Ktest pvalue: " + kstest(data, cdfGenerator)[1])
        if useChiTest:
            pass
        if useADTest:
            print("AD test critical values : " + anderson(data, distribIdentifier)[1])

    def compute_empirical_pdf(self):
        with open(self.data_file_path) as f:
            data = f.readlines()
        self.data = [int(datum) for datum in data]
        self.data_len = len(data)
        self.interval_size = float(self.data[self.data_len - 1] - self.data[0]) / self.bins_cardinality
        current_end = self.data[0]
        self.binned_data = []
        self.binned_data.append({
            'starts': 0,
            'ends': math.ceil(self.data[0] * 100) / 100,
            'content': 0
        })
        for i in range(1, self.bins_cardinality + 1):
            self.binned_data.append({
                'starts': current_end,
                'ends': math.ceil((current_end + self.interval_size) * 100) / 100,
                'content': 0
            })
            current_end = math.ceil((current_end + self.interval_size) * 100) / 100
        for datum in self.data:
            for i in range(0, self.bins_cardinality + 1):
                item = self.binned_data[i]
                if item['starts'] < datum <= item['ends']:
                    item['content'] += 1

    def empirical_cdf(self, value):
        start = self.data[0]
        end = self.data[self.data_len - 1]
        counter = 0
        if value < start:
            return 0
        if value >= end:
            return 1

        for item in self.binned_data:
            if item['ends'] <= value and item['content'] != 0:
                counter += item['content']
        return float(counter) / self.data_len


def main():
    argv = sys.argv
    argc = len(argv)

    if argc != 2:
        print "SCRIPT USAGE: [DATA_FILE_PATH]"
        exit(-1)
    if path.isfile(argv[1]) is False:
        print "PLEASE PROVIDE A VALID DATA_FILE_PATH"
        exit(-1)
    instance = ReliabilityApproximator(argv[1])
    instance.compute_empirical_pdf()


if __name__ == "__main__":
    main()
