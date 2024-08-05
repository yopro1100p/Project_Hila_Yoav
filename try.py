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
        'Electrode': [f'Electrode_{i + 1}' for i in range(20)],
        'num_of_spikes': [0.0] * 20,
        'num_of_bursts': [0.0] * 20,
        'average_absolute_spikes': [0.0] * 20,
        'total_rate_spikes': [0.0] * 20,
        'Feature_5': [0.0] * 20,
        'updated': [False] * 20  # New column to track updates
    }
    df = pd.DataFrame(data)

# Step 2: Ensure the columns are of type float
df = df.astype({'num_of_spikes': 'float64', 'num_of_bursts': 'float64',
                'average_absolute_spikes': 'float64', 'total_rate_spikes': 'float64',
                'Feature_5': 'float64'})

# Step 3: Perform calculations and update the DataFrame
for electrode_num in range(0, 3):
    if not df.at[electrode_num, 'updated']:
        df.at[electrode_num, 'updated'] = True  # Set 'updated' to True for this Electrode
        analyzer = ChannelAnalyzer(file_path, electrode_num)
        df.at[electrode_num, 'num_of_spikes'] = analyzer.num_of_spikes
        df.at[electrode_num, 'num_of_bursts'] = analyzer.num_of_burst
        df.at[electrode_num, 'average_absolute_spikes'] = analyzer.Average_Spikes
        df.at[electrode_num, 'total_rate_spikes'] = analyzer.total_rate_spikes
        df.at[electrode_num, 'Feature_5'] = 4

# Step 3: Write the updated DataFrame back to the Excel file
df.to_excel('example.xlsx', index=False)

print('Data successfully updated and written to electrode_data.xlsx')
