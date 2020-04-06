#!/usr/bin/env python3
import argparse
import pandas as pd
import os

# Preprocess the data from United States Census
# (https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/state/detail)
# to the common csv format that contains 'name' and 'population'.
def preprocess(input, output):
    assert(os.path.exists(input))
    data = pd.read_csv(input)

    # Rename column names
    population = data.rename(columns={'NAME':'name','POPESTIMATE2019':'population'})

    # Extract estimated population of 2020 (Variand:Medium) for each country.
    population = population.loc[:,['name','population']]
    population.set_index('name', inplace=True)

    # Output the results as CSV.
    population.to_csv(output)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input', required=True)
    parser.add_argument('-o','--output', required=True)
    args = parser.parse_args()
    preprocess(args.input, args.output)

if __name__ == '__main__':
    main()
