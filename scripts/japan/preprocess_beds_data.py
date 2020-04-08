#!/usr/bin/env python3
import argparse
import pandas as pd
import os

# Preprocess the data from Ministry of Health, Labour and Welfare
# (https://www.mhlw.go.jp/toukei/youran/indexyk_2_2.html)
# to the common csv format that contains 'name' and 'beds_per_1000'.
def preprocess(input, output):
    assert(os.path.exists(input))
    data = pd.read_csv(input)

    # Convert data to per 1,000. 
    beds = data
    beds['beds_per_1000'] = beds.beds_per_100000 * 0.01
    beds.set_index('name', inplace=True)

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
    beds.rename(index=PREFECTURE_NAMES, inplace=True)

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
