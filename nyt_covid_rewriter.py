import matplotlib.pyplot as plt

import numpy as np

import pandas as pd

import os

from datetime import datetime as dt

import xlsxwriter

# Hard coded in the file location and name
folder = 'C:\\Users\\Anubis\\Documents\\GitHub\\covid-19-data\\'

file_name = 'us-states'

file_to_graph = folder + file_name + '.csv'

now = dt.now()

save_file = file_name + ' ' + now.strftime("%m.%d.%Y %H-%M") + '.xlsx'

# Creates a dataframe from the .csv
df = pd.read_csv(file_to_graph, usecols=[0, 1, 2, 3, 4])

# Creates a non-duplicate list of state names - note there are 55 entries because it includes US territories and
# Washington DC
state_names = list(set(df.iloc[:, 1]))

# Sorts the list of state names alphabetically
sorted_state_names = sorted(state_names, key=str.lower)

# Finds the first date and last date in the file
first_date = df.iloc[1, 0]
last_date = df.iloc[df.shape[0]-1, 0]

# Creates a list of dates
dates = pd.date_range(first_date, last_date)

# Create an Excel workbook to save all the data in
workbook = xlsxwriter.Workbook(save_file)

# Add the date format to the workbook
format3 = workbook.add_format({'num_format': 'mm/dd/yy'})

# Add a worksheet for cases, a worksheet for deaths, and put column labels on both
worksheet1 = workbook.add_worksheet('Cases')
worksheet2 = workbook.add_worksheet('Deaths')

worksheet1.write(0, 0, 'State')
worksheet2.write(0, 0, 'State')

for a in range(0, len(dates)):
    worksheet1.write(0, a+1, dates[a], format3)
    worksheet2.write(0, a+1, dates[a], format3)

for b in range(0, len(sorted_state_names)):
    worksheet1.write(b + 1, 0, sorted_state_names[b])
    worksheet2.write(b + 1, 0, sorted_state_names[b])

date_good = 0
date_bad = 0
name_good = 0
name_bad = 0

# Iterates over the entire dataframe to see if there is data matching the state and date to save into the number of
# cases and deaths
for i in range(0, len(sorted_state_names)):

    state_deaths = []
    state_cases = []

    for j in range(0, len(dates)):

        temp_df = df[df['date'].str.match(str(dates[j]))]

        test = [sorted_state_names[i]]

        print("isin " + str(temp_df.isin(test)))

        if temp_df.shape[0] > 0:

            if temp_df.isin(test)[0]:

                state_deaths.append(df.iloc[df[df['date'].str.match(sorted_state_names[i]), 4]])
                state_cases.append(df.iloc[df[df['date'].str.match(sorted_state_names[i]), 3]])
            else:
                state_deaths.append(0)
                state_cases.append(0)

        else:
            state_deaths.append(0)
            state_cases.append(0)


        # for k in range(0, df.shape[0]-1):
        #
        #     # print(df.iloc[k, 0])
        #     # print(dates[j].strftime('%Y-%m-%d'))
        #     # print(df.iloc[k, 1])
        #     # print(sorted_state_names[i])
        #
        #     if df.iloc[k, 0] == dates[j].strftime('%Y-%m-%d'):
        #
        #         date_good = date_good + 1
        #
        #         if df.iloc[k, 1] == sorted_state_names[i]:
        #
        #             name_good = name_good + 1
        #
        #             state_deaths.append(df.iloc[k, 4])
        #             state_cases.append(df.iloc[k, 3])
        #
        #         else:
        #
        #             name_bad = name_bad + 1
        #
        #     else:
        #
        #         date_bad = date_bad + 1
        #
        #         state_deaths.append(0)
        #         state_cases.append(0)

    # Write the deaths/cases data for all dates to a single line with the state name
    for l in range(0, len(state_deaths)):
        worksheet1.write(i + 1, l + 1, state_cases[l])
        worksheet2.write(i + 1, l + 1, state_deaths[l])

workbook.close()

# print('Date Good')
# print('Date Bad')
# print('Name Good')
# print('Name Bad')
