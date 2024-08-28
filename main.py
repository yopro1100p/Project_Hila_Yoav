import os

import h5py
import matplotlib.pyplot as plt
import McsPy
import numpy as np
import pandas as pd
from McsPy.McsData import RawData

from Chanels import ChannelAnalyzer

# Prompt the user to select an HDF5 file
# raw_data_path = "C:/Users/user/Desktop/bar ilan/Forth year/project/your_file.h5" # YOAV'S LINK
raw_data_path = r"C:\Users\dvirg\OneDrive\Desktop\toar1\year4\project\CODE\recorders\2024-06-13T17-31-24McsRecording_MEA23414_predictable_baseline_A-00020.h5"

# Define parameters
sampling_rate = 10000  # sample rate in Hz
channel_id = 40  # Example channel ID

# Initialize the ChannelAnalyzer for the selected channel
channel_analyzer = ChannelAnalyzer(raw_data_path, channel_id, sampling_rate)


print(f"Number of spikes in Channel {channel_id}: {channel_analyzer.num_of_spikes}")
print(f"Spike Rate: {channel_analyzer.Spikes_rate}")
print(f"Number of Bursts: {channel_analyzer.Num_Of_Bursts}")
print(f"Burst Rate: {channel_analyzer.burst_rate}")
print(f"Average Spike Amplitude: {channel_analyzer.Average_Spikes}")

# Plotting the results
#channel_analyzer.plot(record_type=True)

# Further analysis if needed, using data from ChannelAnalyzer
Group_Of_Spikes = channel_analyzer.group_of_spikes
max_values = channel_analyzer.max_values
Spikes_Samples_Vec_Time = channel_analyzer.spikes_samples_vec_time


channel_analyzer.plot_spikes_and_bursts(record_type=True)
