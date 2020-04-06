#!/usr/bin/env python3
import argparse
from datetime import datetime
import pandas as pd
import os

# Preprocess the data from The New York Times 
# (https://www.nytimes.com/interactive/2020/us/coronavirus-us-cases.html)
# to the common csv format that contains 'name', 'date', and 'total_cases'.
def preprocess(input, output):
    assert(os.path.exists(input))
    data = pd.read_csv(input)

    # Reformat name and date columns.
    cases = data
    cases.rename(columns= {'state':'name','date':'dateStr', 'cases':'total_cases'},inplace=True)
    cases['date'] = [datetime.strptime(date, "%Y-%m-%d") for date in cases.dateStr]
    cases.sort_values(by='date',inplace=True)
    
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
