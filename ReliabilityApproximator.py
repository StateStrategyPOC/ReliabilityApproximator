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
        """
        Computes an approximation of the reliability of the system by applying the formula:
        R(t) = 1 - Femp(t)

        Where Femo(t) is the empirical CDF computed from timestamps relative to errors in the system
        @param time: The time instant for which we want to compute the reliability of the system
        @return: The probability that the system has not failed within time t (reliability in t)
        """
        counter = 0
        with open(self.data_file_path) as f:
            for index, line in enumerate(f):
                if int(line) <= time:
                    counter += 1

        result = 1 - float(counter) / (index+1)
        return result

    def distribution_fitting(self, use_ks_test, use_chi_test, ks_distribution_identifier,
                             cs_expected_frequencies, distribution_parameters):
        """
        Computes the p-value for either the chi square and kolmogorov smirnov goodness of fit test. Note
        that the implementation of this method is tighly coupled with Scipy's provided method
        for doing the above mentioned tests.
        @param use_ks_test: If the kolmogorov smirnov test should be used
        @param use_chi_test: If the chi-squared test should be used
        @param ks_distribution_identifier: A Scipy dependent distribution identifier for the distribution for which
        the k-s test should be done
        @param cs_expected_frequencies: The expected frequencies of the data into the bins of the emprical PDF
        in order to perform the chi-square test
        @param distribution_parameters: The Scipy dependent parameters of the distribution to be used for the k-s test
        @return: Nothing
        """
        to_return = []
        if use_ks_test:
            with open(self.data_file_path) as f:
                data = [int(datum) for datum in f.readlines()]
                p_value = kstest(data, ks_distribution_identifier, distribution_parameters)[1]
                to_return.append(p_value)
        if use_chi_test:
            # organize data into bins
            self.compute_empirical_pdf()
            # extract the content of these bins
            real_frequencies = [datum['content'] for datum in self.binned_data]
            # execute the cs test with the given expected frequencies and retrieve the p-value
            p_value = chisquare(real_frequencies, cs_expected_frequencies)[1]
            to_return.append(p_value)
        return to_return

    def compute_empirical_pdf(self):
        """
        Computes the emprical PDF of the data provided to objects of this class, i.e
        divides the data into bins and makes these binned data available in the context of this class
        @return: Nothing
        """
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
