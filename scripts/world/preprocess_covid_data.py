#!/usr/bin/env python3
import argparse
from datetime import datetime
import pandas as pd
import os

# Preprocess the data from ECDC
# (https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide)
# to the common csv format that contains 'name', 'date', and 'total_cases'.
def preprocess(input, output):
    assert(os.path.exists(input))
    data = pd.read_csv(input)

    # Reformat name and date columns.
    cases = data
    cases['name'] = [name.replace('_', ' ') for name in cases.countriesAndTerritories]
    cases['date'] = [datetime.strptime(date, "%d/%m/%Y") for date in cases.dateRep]
    cases.sort_values(by='date',inplace=True)

    # Calculate cumulative cases.
    cases['total_cases'] = cases.groupby('name').cases.cumsum()
    
    # Extract only columns needed.
    cases = cases.loc[:,['name','date','total_cases']]
    cases.set_index('name', inplace=True)

    # Convert some country names variations.
    COUNTRY_NAME_VARIATION = {
        "Democratic People's Republic of Korea": 'North Korea',
        "Dem. People's Republic of Korea": 'North Korea',
        'Republic of Korea': 'South Korea',
        'United Kingdom of Great Britain and Northern Ireland': 'United Kingdom',
        'Viet Nam': 'Vietnam',
        'Republic of North Macedonia': 'North Macedonia',
        }
    cases.rename(index=COUNTRY_NAME_VARIATION, inplace=True)

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
