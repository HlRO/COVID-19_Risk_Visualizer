import pandas as pd
import numpy as np
from sklearn import linear_model
from datetime import datetime
import time
import os
import json


# Extract data for the last 7 days.
# If offset is given, 7 days data up to [today - offset] day.
def ExtractAWeek(state, database, offset = 0):
    if offset == 0:
        return database.loc[database.state == state].iloc[-7:]
    else:
        return database.loc[database.state == state].iloc[-7-offset:-offset]

# Estimate daily increase ratio.
# This function applys lnear regression in logarithmic space.
def EstimateRate(state, dates, numbers):
    # Apply linear regression in log space.
    X = np.arange(7).reshape(-1, 1)
    Y = numbers.values.reshape(-1, 1)
    linear_regressor = linear_model.LinearRegression()
    linear_regressor.fit(X, np.log(Y))
    # Convert the result to rate/day.
    rate = np.exp(linear_regressor.coef_[0,0])
    return rate

# Analyse data for the given state.
def Analyse(state):
    # Get COVID-19 statistics.
    # TODO add data source.
    COVID_STATS_PATH = 'data/us-states.csv'
    covid_stats = pd.read_csv(COVID_STATS_PATH)
    stat_update_time = time.localtime(os.path.getmtime(COVID_STATS_PATH))

    # Calculate increasing ratio from past 7 days. 
    aweek = ExtractAWeek(state, covid_stats)
    day_rate = EstimateRate(state, aweek.date, aweek.cases)
    current = aweek.cases.iloc[-1]

    # Check if the rate is decreasing.
    aweek_to_yesterday = ExtractAWeek(state, covid_stats, 1)
    day_rate_yesterday = EstimateRate(state, aweek_to_yesterday.date, aweek_to_yesterday.cases)
    rate_change = day_rate - day_rate_yesterday

    # Get populaiton data.
    # TODO add data source.
    populations = pd.read_csv('data/SCPRC-EST2019-18+POP-RES.csv')
    population = populations.loc[populations.NAME == state,'POPESTIMATE2019'].values[0]

    # Get the number of hospital beds.
    # TODO add data source.
    bed_database = pd.read_csv('data/hospital_beds_2018.csv',skiprows=2)
    beds_per_1000 = bed_database.loc[bed_database.Location == state,'Total'].values[0]
    beds = beds_per_1000 * population / 1000

    # Estimate days of milestones.
    time_1_per_500 = max(0.0, np.log(population / 500 / current) / np.log(day_rate))
    time_1_per_3 = max(0.0, np.log(population / 3 / current) / np.log(day_rate))
    time_everyone = max(0.0, np.log(population / 1 / current) / np.log(day_rate))
    time_no_bed = max(0.0, np.log(beds / current) / np.log(day_rate))

    return [current, (day_rate - 1.0) * 100, rate_change, stat_update_time, time_1_per_500, time_1_per_3, time_everyone, time_no_bed]
