#!/bin/bash
cd /home/Visualization/covid_risk_visualizer/data/
curl -O "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv" -o "../data/NYT_covid-19_data.csv"
wget "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv" -O "../data/world/ECDC_covid-19_data.csv"
