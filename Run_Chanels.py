import time
import h5py
import pandas as pd
import numpy as np
import McsPy
import matplotlib.pyplot as plt
import Chanels

file_path = "C:/Users/user/Desktop/bar ilan/Forth year/project/your_file.h5"

start_time = time.time()  # Record the start time
# Iterate over electrodes
for electrode in range(1, 3):
    # Initialize ChannelAnalyzer for the current electrode
    analyzer = Chanels.ChannelAnalyzer(file_path, electrode)

    # Find spikes for the current electrode
    analyzer.find_spikes()

    # Plot spikes for the current electrode
    plt.scatter(analyzer.spikes_samples_vec_time, [electrode] * len(analyzer.spikes_samples_vec_time), color='blue')
end_time = time.time()  # Record the end time

elapsed_time = end_time - start_time  # Calculate the elapsed time
print(f"Elapsed time: {elapsed_time} seconds")

# Set plot labels and grid
plt.xlabel('Time (s)')
plt.ylabel('Electrodes')
plt.grid(True)
plt.show()
