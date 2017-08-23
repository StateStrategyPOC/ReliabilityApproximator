#!/usr/bin/env python
import math
import os.path as path
import sys

from scipy.stats import kstest, chisquare


class ReliabilityApproximator:
    def __init__(self, data_file_path, bins_cardinality):
        self.data_file_path = data_file_path
        self.bins_cardinality = bins_cardinality
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

    def distribution_fitting(self, use_k_test, use_chi_test, distribution_identifier, distribution_object,
                             parameters):
        if use_k_test:
            with open(self.data_file_path) as f:
                data = [int(datum) for datum in f.readlines()]
            print("Ktest pvalue: " + str(kstest(data, distribution_identifier, parameters)[1]))
        if use_chi_test:
            expected_frequencies = [item * self.data_len for item in
                                    self.compute_expected_frequencies(distribution_object, parameters)]
            print ("CHI2 TEST pvalue = " +
                   str(chisquare([datum['content'] for datum in self.binned_data], expected_frequencies)[1]))

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

    def compute_expected_frequencies(self, distribution_object, parameters):
        self.compute_empirical_pdf()
        return [
            distribution_object.cdf(datum['ends'], *parameters) - distribution_object.cdf(datum['starts'], *parameters)
            for datum in self.binned_data]


def main():
    argv = sys.argv
    argc = len(argv)

    if argc != 3:
        print "SCRIPT USAGE: [DATA_FILE_PATH] [# OF BINS]"
        exit(-1)
    if path.isfile(argv[1]) is False:
        print "PLEASE PROVIDE A VALID DATA_FILE_PATH"
        exit(-1)
    if check_if_integer(argv[2]) is False:
        print "PLEASE PROVIDE A VALID INTEGER FOR [# OF BINS]"
        exit(-1)


def check_if_integer(number):
    try:
        int(number)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    main()
