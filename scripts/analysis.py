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

# Analyse data for the given name.
def Analyse(name, covid_path, population_path, beds_path):
    # Load database.
    update_time = time.localtime(os.path.getmtime(covid_path))
    cases = pd.read_csv(covid_path)
    populations = pd.read_csv(population_path)
    beds = pd.read_csv(beds_path)

    # Extract common names.
    names = set(cases.name.unique()).intersection(set(populations.name).intersection(beds.name))
    names = sorted(names)

    # Calculate increasing ratio from past 7 days. 
    dates = cases.date.unique()[-DATA_RANGE:]
    aweek = ExtractAWeek(name, cases)
    assert(set(aweek.date) == set(dates))
    day_rate = EstimateRate(aweek.total_cases)
    current = aweek.total_cases.iloc[-1]

    # Check if the rate is decreasing.
    dates = cases.date.unique()[-DATA_RANGE-1:-1]
    aweek_to_yesterday = ExtractAWeek(name, cases, 1)
    assert(set(aweek_to_yesterday.date) == set(dates))
    day_rate_yesterday = EstimateRate(aweek_to_yesterday.total_cases)
    rate_change = day_rate - day_rate_yesterday

    # Get populaiton data.
    print(populations)
    print(name)
    population = populations.loc[populations.name == name,'population'].values[0]

    # Get the number of hospital beds.
    beds_per_1000 = beds.loc[beds.name == name,'beds_per_1000'].values[0]
    beds = beds_per_1000 * population / 1000

    print(name)
    print(population)
    print(beds)
    print(current)
    print(day_rate)

    # Estimate days of milestones.
    time_1_per_500 = max(0.0, np.log(population / 500 / current) / np.log(day_rate))
    time_1_per_3 = max(0.0, np.log(population / 3 / current) / np.log(day_rate))
    time_everyone = max(0.0, np.log(population / 1 / current) / np.log(day_rate))
    time_no_bed = max(0.0, np.log(beds / current) / np.log(day_rate))

    return [names, current, (day_rate - 1.0) * 100, rate_change, update_time, time_1_per_500, time_1_per_3, time_everyone, time_no_bed]
