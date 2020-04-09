#!/usr/bin/env python3
import argparse
import pandas as pd
import os

# Preprocess the data from UN (https://population.un.org/wpp/Download/Standard/CSV/)
# to the common csv format that contains 'name' and 'population'.
def preprocess(input, output):
    assert(os.path.exists(input))
    data = pd.read_csv(input)

    # Rename column names
    population = data.rename(columns={'Location':'name','Time':'year'})

    # Convert the population (thousands) to actual number.
    population['population'] = population.PopTotal * 1000

    # Extract estimated population of 2020 (Variand:Medium) for each country.
    population = population.loc[(population.year==2020) & (population.Variant=='Medium'),['name','year','population']]
    population.set_index('name', inplace=True)

    # Convert some country names variations.
    COUNTRY_NAME_VARIATION = {
        "Democratic People's Republic of Korea": 'North Korea',
        "China, Taiwan Province of China": 'Taiwan',
        "China, Hong Kong SAR": 'Hong Kong',
        "Dem. People's Republic of Korea": 'North Korea',
        'Republic of Korea': 'South Korea',
        'United Kingdom of Great Britain and Northern Ireland': 'United Kingdom',
        'Viet Nam': 'Vietnam',
        'Republic of North Macedonia': 'North Macedonia',
        'Bolivia (Plurinational State of)':'Bolivia',
        'Cabo Verde': 'Cape Verde',
        "Côte d'Ivoire": 'Cote dIvoire',
        'Guinea-Bissau': 'Guinea Bissau',
        'Iran (Islamic Republic of)': 'Iran',
        "Lao People's Democratic Republic": 'Laos',
        'Republic of Moldova': 'Moldova',
        'Russian Federation': 'Russia',
        'Syrian Arab Republic': 'Syria',
        'Timor-Leste': 'Timor Leste',
        'Venezuela (Bolivarian Republic of)': 'Venezuela',
        }
    population.rename(index=COUNTRY_NAME_VARIATION, inplace=True)

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
