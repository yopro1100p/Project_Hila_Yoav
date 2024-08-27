import random
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from openpyxl import load_workbook

from Chanels import ChannelAnalyzer

# File paths
file_path = "C:/Users/dvirg/OneDrive/Desktop/toar1/year4/project/CODE/2024-02-01T14-33-39McsRecording_MEA21009_predictable_baseline_A-00020.h5"
output_file = "C:/Users/user/Desktop/bar ilan/Forth year/Project_Hila_Yoav/channel_analysis.xlsx"

# Initialize a list to collect all max_values_time for setting xlim
all_max_values_time = []

# Iterate over electrodes
for electrode in range(0, 120):  # Assuming electrodes range from 1 to 120
    analyzer = ChannelAnalyzer(file_path, electrode)
    analyzer.get_channel_data(electrode)
    
    # Print max_values_time for debugging
    print(f"Electrode {electrode+1}, max_values_time: {analyzer.max_values_time}")

    # Collect max_values_time for setting xlim
    all_max_values_time.extend(analyzer.max_values_time)

    # Plot spikes for the current electrode
    plt.scatter(analyzer.max_values_time, [electrode+1] * len(analyzer.max_values_time), color='blue', s=1)

# Check if we have collected any time values for setting xlim
if all_max_values_time:
    plt.xlim(min(all_max_values_time), max(all_max_values_time))
else:
    print("No max_values_time found.")

# Render the plot
plt.xlabel('Time (s)')
plt.ylabel('Electrode')
plt.title('Raster Plot of Electrode Spikes')
plt.show()