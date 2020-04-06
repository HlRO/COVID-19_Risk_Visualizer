#!/bin/bash
wget "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv" -O $PROJECT_HOME"/data/usa/NYT_covid-19_data.csv"
wget "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv" -O $PROJECT_HOME"/data/world/ECDC_covid-19_data.csv"
