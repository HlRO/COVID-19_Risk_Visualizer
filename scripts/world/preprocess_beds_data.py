#!/usr/bin/env python3
import argparse
import pandas as pd
import os

# Preprocess the data from WHO (https://apps.who.int/gho/data/view.main.HS07v)
# to the common csv format that contains 'name' and 'beds_per_1000'.
def preprocess(input, output):
    assert(os.path.exists(input))
    data = pd.read_csv(input)

    # Extract latest data for each country.
    beds = data.sort_values(by=['Year']).groupby('Country').first()

    # Rename column names
    beds.rename(columns={'Year':'year','Hospital beds (per 10 000 population)':'beds_per_10000'},inplace=True)
    beds.index.names = ['name']

    # Convert some country names variations.
    COUNTRY_NAME_VARIATION = {
        "Democratic People's Republic of Korea": 'North Korea',
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
    beds.rename(index=COUNTRY_NAME_VARIATION, inplace=True)

    # Add Taiwan Data from PWC Taiwan
    # (https://www.pwc.tw/en/publications/assets/taiwan-health-industries.pdf)
    beds.loc['Taiwan']= [2016, 57]

    # Add Hong Kong Data from Hong Kong Government.
    # (https://www.gov.hk/en/about/abouthk/factsheets/docs/public_health.pdf)
    beds.loc['Hong Kong'] = [2015, 52]

    beds.sort_index(inplace=True)

    # Convert to the number of beds per 1000 people.
    beds['beds_per_1000'] = beds['beds_per_10000'] * 0.1

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
