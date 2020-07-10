import pandas as pd

from datetime import datetime as dt

import xlsxwriter

def list_to_number_string(value):
    if isinstance(value, (list, tuple)):
        return str(value)[1:-1]
    else:
        return value

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

# Add a worksheet for cases, a worksheet for deaths
worksheet1 = workbook.add_worksheet('Cases')
worksheet2 = workbook.add_worksheet('Deaths')

# Adds first column label
worksheet1.write(0, 0, 'State')
worksheet2.write(0, 0, 'State')

# Adds all date column labels
for a in range(0, len(dates)):
    worksheet1.write(0, a+1, dates[a], format3)
    worksheet2.write(0, a+1, dates[a], format3)

for b in range(0, len(sorted_state_names)):
    worksheet1.write(b + 1, 0, sorted_state_names[b])
    worksheet2.write(b + 1, 0, sorted_state_names[b])

# Iterates through all the date/state combinations
for i in range(0, len(sorted_state_names)):

    for j in range(0, len(dates)):

        # Finds the row in the dataframe that matches the date and state combination -- if none, an empty dataframe
        # is returned
        cycle_df = df[df['date'].str.contains(dates[j].strftime('%Y-%m-%d')) &
                      df['state'].str.contains(sorted_state_names[i])]

        # This resets the index so that it's a known value each time
        cycle_df = cycle_df.reset_index()

        # If the dataframe isn't empty, then write the values in the dataframe
        if cycle_df.shape[0] > 0:

            worksheet1.write(i + 1, j + 1, str(cycle_df.iloc[cycle_df.shape[0]-1, 4]))
            worksheet2.write(i + 1, j + 1, str(cycle_df.iloc[cycle_df.shape[0]-1, 5]))

        # Otherwise it writes zeroes for convenience
        else:

            worksheet1.write(i + 1, j + 1, 0)
            worksheet2.write(i + 1, j + 1, 0)

# Closing the workbook is when it's actually written out, so this is pretty important
workbook.close()
