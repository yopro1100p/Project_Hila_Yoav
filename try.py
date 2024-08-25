import random
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from openpyxl import load_workbook

from Chanels import ChannelAnalyzer

#file_path1 = "C:/Users/dvirg/OneDrive/Desktop/toar1/year4/project/CODE/2024-02-01T14-33-39McsRecording_MEA21009_baseline_A-00020.h5"   # baseline - yoav link
#file_path2 = "C:/Users/dvirg/OneDrive/Desktop/toar1/year4/project/CODE/2024-02-01T14-54-37McsRecording_MEA21009_predictable_aferstim_A-00020.h5"   # stimulus 


# Step 1: Load existing Excel file (if any)

try:
    df = pd.read_excel('example.xlsx')
except FileNotFoundError:
    # If file doesn't exist, create a new DataFrame
    data = {
        'Electrode': [f'Electrode_{i + 1}' for i in range(120)],
        'num_of_spikes': [0.0] * 120,
        'num_of_bursts': [0.0] * 120,
        'average_absolute_spikes': [0.0] * 120,
        'Spikes_rate': [0.0] * 120,
        'spikes_per_bursts': [0.0] * 120,
        'stim': [None] * 120,
        'num_of_spikes_stim': [0.0] * 120,
        'num_of_bursts_stim': [0.0] * 120,
        'average_absolute_spikes_stim': [0.0] * 120,
        'Spikes_rate_stim': [0.0] * 120,
        'spikes_per_bursts_stim': [0.0] * 120,
        'diff': [None] * 120,
        'num_of_spikes_diff': [0.0] * 120,
        'num_of_bursts_diff': [0.0] * 120,
        'average_absolute_spikes_diff': [0.0] * 120,
        'Spikes_rate_diff': [0.0] * 120,
        'spikes_per_bursts_diff': [0.0] * 120,
        'active': [None] * 120  # New column to track updates
    }
    df = pd.DataFrame(data)

# Step 2: Ensure the columns are of type float
df = df.astype({'num_of_spikes': 'float64', 'num_of_bursts': 'float64',
                'average_absolute_spikes': 'float64', 'Spikes_rate': 'float64',
                'spikes_per_bursts': 'float64', 'num_of_spikes_stim': 'float64', 'num_of_bursts_stim': 'float64',
                'average_absolute_spikes_stim': 'float64', 'Spikes_rate_stim': 'float64',
                'spikes_per_bursts_stim': 'float64', 'num_of_spikes_diff': 'float64', 'num_of_bursts_diff': 'float64',
                'average_absolute_spikes_diff': 'float64', 'Spikes_rate_diff': 'float64',
                'spikes_per_bursts_diff': 'float64'})

# Step 3: Perform calculations and update the DataFrame
for electrode_num in range(3, 10):
    if df.at[electrode_num, 'active'] is None:
        analyzer1 = ChannelAnalyzer(file_path1, electrode_num)
        analyzer1.plot(1)  # baseline
        analyzer2 = ChannelAnalyzer(file_path2, electrode_num)
        analyzer2.plot(0)  # stimulus
        df.at[electrode_num, 'active'] = analyzer1.active  # Check if the Electrode is active
        df.at[electrode_num, 'num_of_spikes'] = analyzer1.num_of_spikes
        df.at[electrode_num, 'average_absolute_spikes'] = analyzer1.Average_Spikes
        df.at[electrode_num, 'Spikes_rate'] = analyzer1.Spikes_rate
        if analyzer1.Num_Of_Bursts != 0:
            df.at[electrode_num, 'num_of_bursts'] = analyzer1.Num_Of_Bursts
            df.at[electrode_num, 'spikes_per_bursts'] = analyzer1.spikes_per_burst

        df.at[electrode_num, 'num_of_spikes_stim'] = analyzer2.num_of_spikes
        df.at[electrode_num, 'average_absolute_spikes_stim'] = analyzer2.Average_Spikes
        df.at[electrode_num, 'Spikes_rate_stim'] = analyzer2.Spikes_rate
        if analyzer2.Num_Of_Bursts != 0:
            df.at[electrode_num, 'num_of_bursts_stim'] = analyzer2.Num_Of_Bursts
            df.at[electrode_num, 'spikes_per_bursts_stim'] = analyzer2.spikes_per_burst

        df.at[electrode_num, 'num_of_spikes_diff'] = analyzer2.num_of_spikes - analyzer1.Num_Of_Bursts
        df.at[electrode_num, 'average_absolute_spikes_diff'] = analyzer2.Average_Spikes - analyzer1.Average_Spikes
        df.at[electrode_num, 'Spikes_rate_diff'] = analyzer2.Spikes_rate - analyzer1.Spikes_rate
        if analyzer2.Num_Of_Bursts != 0:
            df.at[electrode_num, 'num_of_bursts_diff'] = analyzer2.Num_Of_Bursts - analyzer1.Num_Of_Bursts
            df.at[electrode_num, 'spikes_per_bursts_diff'] = analyzer2.spikes_per_burst - analyzer1.spikes_per_burst

# Step 3: Write the updated DataFrame back to the Excel file
df.to_excel('example.xlsx', index=False)

print('Data successfully updated and written to electrode_data.xlsx')
