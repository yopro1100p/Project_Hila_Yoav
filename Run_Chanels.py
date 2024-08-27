import random
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from openpyxl import load_workbook

from Chanels import ChannelAnalyzer

# File paths
file_path ="C:/Users/dvirg/OneDrive/Desktop/toar1/year4/project/CODE/recorders/2024-06-13T17-53-27McsRecording_MEA23414_predictable_afterstim_A-00020.h5"

# Extract date and MEA ID from file path
date_part = file_path.split('/')[-1].split('T')[0]
mea_id = file_path.split('_')[3][3:8]  # Extract "23414" from "MEA23414"

# Initialize a list to collect all max_values_time for setting xlim
all_max_values_time = []

# Iterate over electrodes
for electrode in range(0, 3):  # Assuming electrodes range from 1 to 120
    print(electrode)
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

# Set the title using the desired format
plot_title = f"raster_plot_{date_part}_{mea_id}_"
plt.title(plot_title)

# Save the plot with the same name as the title
output_filename = f"{plot_title}.png"
plt.savefig(output_filename)

# Show the plot
plt.xlabel('Time (s)')
plt.ylabel('Electrode')
plt.show()