import time

import h5py
import matplotlib.pyplot as plt
import McsPy
import numpy as np
import pandas as pd

import Chanels

#file_path = "C:/Users/user/Desktop/bar ilan/Forth year/project/your_file.h5" #yoav's link 
file_path = "C:/Users/dvirg/OneDrive/Desktop/toar1/year4/project/CODE/your_file.h5"#hilla's link

start_time = time.time()  # Record the start time
# Iterate over electrodes
for electrode in range(1, 5):
    # Initialize ChannelAnalyzer for the current electrode
    analyzer = Chanels.ChannelAnalyzer(file_path, electrode)

    # Find spikes for the current electrode
    analyzer.find_spikes()
    analyzer.group_spikes()
    analyzer.find_max_in_groups()

    # Plot spikes for the current electrode
    # we plot the electrods spikes in function of time
    plt.scatter(analyzer.max_values_time, [electrode] * len(analyzer.max_values_time), color='blue')
end_time = time.time()  # Record the end time
plt.xlim(min(analyzer.time_vec), max(analyzer.time_vec))
elapsed_time = end_time - start_time  # Calculate the elapsed time
print(f"Elapsed time: {elapsed_time} seconds")

# Set plot labels and grid
plt.xlabel('Time (s)')
plt.ylabel('Electrodes')
plt.grid(True)
plt.show()
