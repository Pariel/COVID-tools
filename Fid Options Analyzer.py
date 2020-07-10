import matplotlib.pyplot as plt

import numpy as np

import pandas as pd

import csv

from datetime import datetime as dt

import re

import math

debug = 1

folder = "D:\\Dropbox\\Financial planning\\Investing\\COVID-19 Positions\\"

file = "7.10.20 SPY Options-20.csv"

now = dt.now()

save_file = folder + "SPY Options " + now.strftime("%m.%d.%Y %H-%M")

df = pd.read_csv(folder + file, header=2)

with open(folder + file, newline='') as csvfile:
    temp_reader = csv.reader(csvfile, delimiter=',')
    data = list(temp_reader)
row_val, col_val = 0, 0
try:
    value = data[row_val][col_val]
    current_price = float(re.sub(r'[$]', '', value.split(" ")[7]))
except IndexError:
    print('No data found')

if debug > 0:
    print(current_price)

# Grabs all columns from the .csv
new_df = df.iloc[:, np.r_[0, 17, 5:7, 8:15, 22:24, 25:32]]

# Creates a list of rows to remove
rem_rows = []

# Finds the list of new dates and rows so that
for i in range(0, new_df.shape[0]):

    if new_df.iloc[i, 2] == '--':

        rem_rows.append(i)

new_date = []

for i in range(0, len(rem_rows)):
    new_date.append(rem_rows[i] - i)

rem_rows.append(new_df.shape[0]-1)

new_df = new_df.drop(labels=rem_rows, axis=0)

new_df.to_csv(save_file + '.csv', index=False)

new_df.reset_index(drop=True, inplace=True)

# Plot the cost of calls and puts versus the difference between present value
calls = pd.to_numeric(new_df.iloc[:, 2])
puts = pd.to_numeric(new_df.iloc[:, 11])
strike_dif = pd.to_numeric(new_df.iloc[:, 1]) - current_price

fig = plt.figure(figsize=(20, 9))
ax1 = plt.subplot(111)
plt.title('Option Cost Versus Present Value')
ax1.set_xlabel('Strike Dif')
ax1.set_ylabel('Option Cost')

for i in range(0, 3): #  len(new_date)-1

    date = str(new_df.iloc[new_date[i], 0])

    cycle_calls = calls[new_date[i]:new_date[i + 1]].sort_index(ascending=False)

    if i == len(new_date)-1:
        ax1.plot(strike_dif[new_date[i]:len(calls)], cycle_calls, label='Calls ' + date)
        plt.plot(strike_dif[new_date[i]:len(calls)], puts[new_date[i]:len(calls)], label='Puts ' + date)

    else:
        ax1.plot(strike_dif[new_date[i]:new_date[i+1]], cycle_calls, label='Calls ' + date)
        plt.plot(strike_dif[new_date[i]:new_date[i+1]], puts[new_date[i]:new_date[i+1]], label='Puts ' + date)

figure_name = 'Options Cost vs. Strike Difference ' + str(i) + " " + now.strftime("%m.%d.%Y %H-%M")

plt.legend(loc='best', shadow=True, ncol=1)  # bbox_to_anchor=(1.2, 0.5)
plt.savefig(folder + figure_name + ".png", bbox_inches="tight")
plt.close()

    # if i == len(new_date)-1:
    #     plot_setup('Option Cost Versus Present Value ' + date, 'Strike Dif', 'Option Cost')
    #     plot_plot(strike_dif[new_date[i]:len(calls)], calls[new_date[i]:len(calls)], 'Calls ' + date)
    #     finish_plot('Options Cost vs. Strike Difference ' + " " + str(i) + " " + now.strftime("%m.%d.%Y %H-%M"))
    #
    #     plot_setup('Option Cost Versus Present Value ' + date, 'Strike Dif', 'Option Cost')
    #     plot_plot(strike_dif[new_date[i]:len(calls)], puts[new_date[i]:len(calls)], 'Puts ' + date)
    #     finish_plot('Options Cost vs. Strike Difference ' + " " + str(i) + " " + now.strftime("%m.%d.%Y %H-%M"))
    #
    # else:
    #     plot_setup('Option Cost Versus Present Value ' + date + " calls", 'Strike Dif', 'Option Cost')
    #     plot_plot(strike_dif[new_date[i]:new_date[i+1]-1], calls[new_date[i]:new_date[i+1]-1], 'Calls ' + date)
    #     finish_plot('Options Cost vs. Strike Difference ' + 'calls' + " " + str(i) + " " + now.strftime("%m.%d.%Y %H-%M"))
    #
    #     plot_setup('Option Cost Versus Present Value ' + date + " puts", 'Strike Dif', 'Option Cost')
    #     plot_plot(strike_dif[new_date[i]:new_date[i+1]-1], puts[new_date[i]:new_date[i+1]-1], 'Puts ' + date)
    #     finish_plot('Options Cost vs. Strike Difference ' + 'calls' + str(i) + " " + now.strftime("%m.%d.%Y %H-%M"))