#!/usr/bin/env python3
import argparse
from datetime import datetime
from datetime import date
import pandas as pd
import os
import re

# Preprocess the data from Toyo Kezai Online 
# (https://github.com/kaz-ogiwara/covid19/)
# to the common csv format that contains 'name', 'date', and 'total_cases'.
def preprocess(input, output):
    assert(os.path.exists(input))
    data = pd.read_csv(input)

    # Reformat name and date columns.
    cases = data
    cases.columns = ['year','month','day', 'name', 'total_cases', 'hospitalized', 'recovered', 'dead']
    cases['date'] = [date(year,month,day) for year,month,day in zip(cases['year'], cases['month'], cases['day'])]
    # Some entry have '"' around the case number. Clean these up to make sure the data is treated as integer not string. 
    cases['total_cases'] = [int(re.sub('[^\d]+','',item)) for item in cases['total_cases']]
    cases.sort_values(by='date',inplace=True)

    # Extract only columns needed.
    cases = cases.loc[:,['name','date','total_cases']]
    cases.set_index('name', inplace=True)

    # Translate prefecture names to English.
    PREFECTURE_NAMES = {
            "北海道": 'Hokkaido',
            "青森県": 'Aomori',
            "岩手県": 'Iwate',
            "宮城県": 'Miyagi',
            "秋田県": 'Akita',
            "山形県": 'Yamagata',
            "福島県": 'Fukushima',
            "茨城県": 'Ibaraki',
            "栃木県": 'Tochigi',
            "群馬県": 'Gunma',
            "埼玉県": 'Saitama',
            "千葉県": 'Chiba',
            "東京都": 'Tokyo',
            "神奈川県": 'Kanagawa',
            "新潟県": 'Niigata',
            "富山県": 'Toyama',
            "石川県": 'Ichikawa',
            "福井県": 'Fukui',
            "山梨県": 'Yamanashi',
            "長野県": 'Nagano',
            "岐阜県": 'Gifu',
            "静岡県": 'Shizuoka',
            "愛知県": 'Aichi',
            "三重県": 'Mie',
            "滋賀県": 'Shiga',
            "京都府": 'Kyoto',
            "大阪府": 'Osaka',
            "兵庫県": 'Hyogo',
            "奈良県": 'Nara',
            "和歌山県": 'Wakayama',
            "鳥取県": 'Tottori',
            "島根県": 'Shimane',
            "岡山県": 'Okayama',
            "広島県": 'Hiroshima',
            "山口県": 'Yamaguchi',
            "徳島県": 'Tokushima',
            "香川県": 'Kagawa',
            "愛媛県": 'Ehime',
            "高知県": 'Kouchi',
            "福岡県": 'Fukuoka',
            "佐賀県": 'Saga',
            "長崎県": 'Nagasaki',
            "熊本県": 'Kumamoto',
            "大分県": 'Oita',
            "宮崎県": 'Miyazaki',
            "鹿児島県": 'Kagoshima',
            "沖縄県": 'Okinawa',
            }
    cases.rename(index=PREFECTURE_NAMES, inplace=True)

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
