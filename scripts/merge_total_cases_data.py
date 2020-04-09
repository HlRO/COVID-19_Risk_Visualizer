#!/usr/bin/env python3
import argparse
from datetime import datetime
import pandas as pd
import os

# Merge 2 total_cases csv files that has 'name', 'date' and 'total_cases'. 
def preprocess(input1, input2, output):
    assert(os.path.exists(input1))
    assert(os.path.exists(input2))
    data1 = pd.read_csv(input1)
    data2 = pd.read_csv(input2)

    # Merge 2 data.
    cases = pd.concat([data1, data2])

    # Reformat name and date columns.
    cases['date'] = [datetime.strptime(date, "%Y-%m-%d") for date in cases.date]
    cases.sort_values(by='date',inplace=True)

    # Extract only columns needed.
    cases = cases.loc[:,['name','date','total_cases']]
    cases.set_index('name', inplace=True)

    # Output the results as CSV.
    cases.to_csv(output)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i1','--input1', required=True)
    parser.add_argument('-i2','--input2', required=True)
    parser.add_argument('-o','--output', required=True)
    args = parser.parse_args()
    preprocess(args.input1, args.input2, args.output)

if __name__ == '__main__':
    main()
