import random
import time
from Chanels import ChannelAnalyzer
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from openpyxl import load_workbook

file_path = "C:/Users/user/Desktop/bar ilan/Forth year/project/your_file.h5"  # yoav's link

# Step 1: Load existing Excel file (if any)
#  you are starting with a new file, you can skip this step.


try:
    df = pd.read_excel('example.xlsx')
except FileNotFoundError:
    # If file doesn't exist, create a new DataFrame
    data = {
        'Electrode': [f'Electrode_{i + 1}' for i in range(120)],
        'num_of_spikes': [0.0] * 120,
        'num_of_bursts': [0.0] * 120,
        'average_absolute_spikes': [0.0] * 120,
        'total_rate_spikes': [0.0] * 120,
        'average_of_num_of_spikes': [0.0] * 120,
        'active': [None] * 120  # New column to track updates
    }
    df = pd.DataFrame(data)

# Step 2: Ensure the columns are of type float
df = df.astype({'num_of_spikes': 'float64', 'num_of_bursts': 'float64',
                'average_absolute_spikes': 'float64', 'total_rate_spikes': 'float64',
                'average_of_num_of_spikes': 'float64'})

# Step 3: Perform calculations and update the DataFrame
for electrode_num in range(10, 17):
    if df.at[electrode_num, 'active'] == None:
        analyzer = ChannelAnalyzer(file_path, electrode_num)
        df.at[electrode_num, 'active'] = analyzer.active  # Check if the Electrode is active
        df.at[electrode_num, 'num_of_spikes'] = analyzer.num_of_spikes
        df.at[electrode_num, 'num_of_bursts'] = analyzer.num_of_burst
        df.at[electrode_num, 'average_absolute_spikes'] = analyzer.Average_Spikes
        df.at[electrode_num, 'total_rate_spikes'] = analyzer.total_rate_spikes
        df.at[electrode_num, 'average_of_num_of_spikes'] = 4


# Step 3: Write the updated DataFrame back to the Excel file
df.to_excel('example.xlsx', index=False)

print('Data successfully updated and written to electrode_data.xlsx')
