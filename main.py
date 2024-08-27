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
raw_data_path = "C:/Users/dvirg/OneDrive/Desktop/toar1/year4/project/CODE/2024-02-01T14-33-39McsRecording_MEA21009_predictable_baseline_A-00020.h5"  # hilla's link

# Define parameters
sampling_rate = 10000  # sample rate in Hz
channel_id = 13  # Example channel ID

# Initialize the ChannelAnalyzer for the selected channel
channel_analyzer = ChannelAnalyzer(raw_data_path, channel_id, sampling_rate)


print(f"Number of spikes in Channel {channel_id}: {channel_analyzer.num_of_spikes}")
print(f"Spike Rate: {channel_analyzer.Spikes_rate}")
print(f"Number of Bursts: {channel_analyzer.Num_Of_Bursts}")
print(f"Burst Rate: {channel_analyzer.burst_rate}")
print(f"Average Spike Amplitude: {channel_analyzer.Average_Spikes}")

# Plotting the results
channel_analyzer.plot(record_type=True)

# Further analysis if needed, using data from ChannelAnalyzer
Group_Of_Spikes = channel_analyzer.group_of_spikes
max_values = channel_analyzer.max_values
Spikes_Samples_Vec_Time = channel_analyzer.spikes_samples_vec_time

# Example of additional burst analysis
min_spkies = 3
max_dist = 3
bursts = channel_analyzer.find_burst(max_dist, min_spkies)
if bursts:
    print("Bursts found:", bursts)

spike_times = [100, 150, 200, 250]  # Example spike times
burst_times = [130, 180, 230]       # Example burst times
channel_analyzer.plot_spikes_and_bursts(spike_times, burst_times, electrode_number=1)
