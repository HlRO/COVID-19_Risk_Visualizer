#!/usr/bin/env python3
import argparse
from datetime import datetime
import pandas as pd
import os

# Preprocess the data from Hong Kong Government. 
# (https://data.gov.hk/en-data/dataset/hk-dh-chpsebcddr-novel-infectious-agent/resource/a09134c1-53ea-4916-a573-62cf972562af)
# to the common csv format that contains 'name', 'date', and 'total_cases'.
def preprocess(input, output):
    assert(os.path.exists(input))
    data = pd.read_csv(input)

    # Reformat name and date columns.
    cases = data
    cases['name'] = ['Hong Kong'] * len(cases)
    cases['date'] = [datetime.strptime(date, "%d/%m/%Y") for date in cases['Report date']]
    cases.rename(columns={'Case no.':'total_cases'}, inplace=True)
    cases.sort_values(by='date',inplace=True)

    # Extract the last data of the day.
    cases = cases.groupby(['date']).last()
    cases.reset_index(inplace=True)
    
    # Extract only columns needed.
    cases = cases.loc[:,['name','date','total_cases']]
    cases.set_index('name', inplace=True)

    # Output the results as CSV.
    cases.to_csv(output)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input', required=True)
    parser.add_argument('-o','--output', required=True)
    args = parser.parse_args()
    preprocess(args.input, args.output)

if __name__ == '__main__':
    main()
