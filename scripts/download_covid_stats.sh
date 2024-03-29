#!/bin/bash
# Download
wget "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv" -O $PROJECT_HOME"/data/usa/NYT_covid-19_data.csv"
wget "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv" -O $PROJECT_HOME"/data/world/ECDC_covid-19_data.csv"
wget "https://www.chp.gov.hk/files/misc/enhanced_sur_covid_19_eng.csv" -O $PROJECT_HOME"/data/world/HKG_covid-19_data.csv"
wget "https://raw.githubusercontent.com/kaz-ogiwara/covid19/master/data/prefectures.csv" -O $PROJECT_HOME"/data/japan/TKO_covid-19_data.csv"

# Preprocess
cd $PROJECT_HOME/scripts
./usa/preprocess_covid_data.py -i $PROJECT_HOME"/data/usa/NYT_covid-19_data.csv" -o $PROJECT_HOME"/data/usa/total_cases.csv"
./world/preprocess_covid_data.py -i $PROJECT_HOME"/data/world/ECDC_covid-19_data.csv" -o $PROJECT_HOME"/data/world/total_cases_ecdc.csv"
./world/preprocess_covid_data_hk.py -i $PROJECT_HOME"/data/world/HKG_covid-19_data.csv" -o $PROJECT_HOME"/data/world/total_cases_hkg.csv"
./merge_total_cases_data.py -i1 $PROJECT_HOME"/data/world/total_cases_ecdc.csv" -i2 $PROJECT_HOME"/data/world/total_cases_hkg.csv" -o $PROJECT_HOME"/data/world/total_cases.csv"
./japan/preprocess_covid_data.py -i $PROJECT_HOME"/data/japan/TKO_covid-19_data.csv" -o $PROJECT_HOME"/data/japan/total_cases.csv"

