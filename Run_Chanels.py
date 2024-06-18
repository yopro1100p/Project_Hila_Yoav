import time

import h5py
import matplotlib.pyplot as plt
import McsPy
import numpy as np
import pandas as pd

import Chanels

# file_path = "C:/Users/user/Desktop/bar ilan/Forth year/project/your_file.h5" #yoav's link 
file_path = "C:/Users/dvirg/OneDrive/Desktop/toar1/year4/project/CODE/your_file.h5" #hilla's link

start_time = time.time()  # Record the start time

# Initialize a list to collect all max_values_time for setting xlim
all_max_values_time = []

# Iterate over electrodes
for electrode in range(1, 6):
    analyzer = Chanels.ChannelAnalyzer(file_path, electrode)
    analyzer.find_spikes()
    analyzer.group_spikes()
    analyzer.find_max_in_groups()

    # Print max_values_time for debugging
    print(f"Electrode {electrode}, max_values_time: {analyzer.max_values_time}")

    # Collect max_values_time for setting xlim
    all_max_values_time.extend(analyzer.max_values_time)
    
    # Plot spikes for the current electrode
    plt.scatter(analyzer.max_values_time, [electrode] * len(analyzer.max_values_time), color='blue',s=1)

end_time = time.time()  # Record the end time

# Check if we have collected any time values for setting xlim
if all_max_values_time:
    plt.xlim(min(all_max_values_time), max(all_max_values_time))
else:
    print("No max_values_time found.")

elapsed_time = end_time - start_time  # Calculate the elapsed time
print(f"Elapsed time: {elapsed_time} seconds")

# Set plot labels and grid
plt.xlabel('Time (s)')
plt.ylabel('Electrodes')
plt.grid(True)

# Ensure plot is displayed
plt.show()
