#!/usr/bin/env python3
import argparse
import pandas as pd
import os

# Preprocess the data from Kaiser Family Foundation
# (https://www.kff.org/other/state-indicator/beds-by-ownership)
# to the common csv format that contains 'name' and 'beds_per_1000'.
def preprocess(input, output):
    assert(os.path.exists(input))
    data = pd.read_csv(input, header=2)

    # Rename column names
    beds = data.rename(columns={'Location':'name','Total':'beds_per_1000'})
    beds.set_index('name', inplace=True)

    # Output the results as CSV.
    beds.to_csv(output)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input', required=True)
    parser.add_argument('-o','--output', required=True)
    args = parser.parse_args()
    preprocess(args.input, args.output)

if __name__ == '__main__':
    main()
