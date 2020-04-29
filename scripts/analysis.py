import pandas as pd
import numpy as np
from sklearn import linear_model
from datetime import datetime
import time
import os
import json

DATA_RANGE = 7

# Extract data for the last 7 days.
# If offset is given, 7 days data up to [today - offset] day.
def ExtractAWeek(name, cases, offset = 0):
    if offset == 0:
        return cases.loc[cases.name == name].iloc[-DATA_RANGE:]
    else:
        return cases.loc[cases.name == name].iloc[-DATA_RANGE-offset:-offset]

# Estimate daily increase ratio.
# This function applys lnear regression in logarithmic space.
def EstimateRate(cases):
    # Apply linear regression in log space.
    X = np.arange(DATA_RANGE).reshape(-1, 1)
    Y = cases.values.reshape(-1, 1)
    linear_regressor = linear_model.LinearRegression()
    linear_regressor.fit(X, np.log(Y))
    # Convert the result to rate/day.
    rate = np.exp(linear_regressor.coef_[0,0])
    return rate

# Analyze data for the given name.
def Analyze(name, covid_path, population_path, beds_path):
    # Load database.
    cases = pd.read_csv(covid_path)
    populations = pd.read_csv(population_path)
    beds = pd.read_csv(beds_path)

    # Extract common names.
    names = set(cases.name.unique()).intersection(set(populations.name).intersection(beds.name))
    names = sorted(names)

    # Calculate increasing ratio from past 7 days. 
    aweek = ExtractAWeek(name, cases)
    try:
        assert(len(aweek.date) == DATA_RANGE)
    except AssertionError:
        print('not enough data for:' + name)
        return None
    day_rate = EstimateRate(aweek.total_cases)
    current = aweek.total_cases.iloc[-1]
    update_time = datetime.strptime(aweek.date.iloc[-1], '%Y-%m-%d')

    # Check if the rate is decreasing.
    aweek_to_yesterday = ExtractAWeek(name, cases, 1)
    try:
        assert(len(aweek_to_yesterday.date) == DATA_RANGE)
    except AssertionError:
        print('not enough data for:' + name)
        return None
    day_rate_yesterday = EstimateRate(aweek_to_yesterday.total_cases)
    rate_change = day_rate - day_rate_yesterday

    # Get populaiton data.
    population = populations.loc[populations.name == name,'population'].values[0]

    # Get the number of hospital beds.
    beds_per_1000 = beds.loc[beds.name == name,'beds_per_1000'].values[0]
    beds = beds_per_1000 * population / 1000

    # Estimate days of milestones.
    time_1_per_500 = max(0.0, np.log(population / 500 / current) / np.log(day_rate))
    time_1_per_3 = max(0.0, np.log(population / 3 / current) / np.log(day_rate))
    time_everyone = max(0.0, np.log(population / 1 / current) / np.log(day_rate))
    time_no_bed = max(0.0, np.log(beds / current) / np.log(day_rate))

    return [aweek.date, aweek.total_cases, names, current, (day_rate - 1.0) * 100, rate_change, update_time, time_1_per_500, time_1_per_3, time_everyone, time_no_bed]
