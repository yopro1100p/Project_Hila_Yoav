import os

import h5py
import matplotlib.pyplot as plt
import McsPy
import numpy as np
import pandas as pd
from McsPy.McsData import RawData

from Chanels import ChannelAnalyzer
from electrode_comparison_analysis import recording_comparison
from heatmap import plot_heatmap
from raster_plot import create_raster_plot
from statistic_test import perform_statistical_tests

# File explanation
"""
This script serves as the main execution point for various types of neural data analysis.
It allows the user to select actions based on the desired analysis, such as:
1. Plotting raw signals from a specified channel.
2. Creating heatmaps based on spike count data from electrodes.
3. Generating raster plots for visualizing spike trains.
4. Performing comparisons between two neural recordings (e.g., baseline vs. post-stimulus).
5. Running statistical tests to compare predictable and control datasets.
The user provides inputs, such as the channel ID and desired analysis type, to perform specific tasks.
"""



sampling_rate = 10000  # sample rate in Hz

# path to file that we want to run action 1-3
# raw_data_path = "C:/Users/user/Desktop/bar ilan/Forth year/project/your_file.h5"  # YOAV'S LINK
raw_data_path = r"C:\Users\dvirg\OneDrive\Desktop\toar1\year4\project\CODE\recorders\2024-05-21T15-43-17McsRecording_MEA21009_predictable_afterstim_A-00020.h5"
# Paths to the files thst we want to run action 4(compare between files)
file_path_compare1 = "C:/Users/dvirg/OneDrive/Desktop/toar1/year4/project/CODE/2024-06-13T14-15-16McsRecording_MEA21009_predictable_baseline_A-00020.h5"  # Replace with the actual path to baseline file
file_path_compare2 = "C:/Users/dvirg/OneDrive/Desktop/toar1/year4/project/CODE/2024-06-13T14-35-58McsRecording_MEA21009_predictable_afterstim_A-00020.h5"  # Replace with the actual path to stimulus file

# Files for static tests
predictable_file = '2024-02-01_21009_predictable.xlsx'
controller_file = '2024-02-01_20490_control.xlsx'


print("choose action: \n1: plot signal \n2: plot_heatmap\n3: raster_plot\n4: electrode_comparison_analysis")

# plot heatmap action
action = int(input())

# plot signal
if action == 1:
    print("choose channel id:")
    channel_id = int(input())  # Example channel ID

    # Initialize the ChannelAnalyzer for the selected channel
    channel_analyzer = ChannelAnalyzer(raw_data_path, channel_id, sampling_rate)
    print (channel_analyzer.Group_Of_Bursts)
    channel_analyzer.plot_signal()

# plot heat map
if action == 2:
    # Ensure the 'heatmap' directory exists
    output_dir = 'heatmap'
    os.makedirs(output_dir, exist_ok=True)

    # Load spike counts from Excel file
    excel_file = '2024-02-01_21009_predictable.xlsx'
    df = pd.read_excel(excel_file)

    # Plot and save the baseline heatmap
    spike_counts_baseline = dict(zip(df['Electrode'], df['num_of_spikes_baseline']))
    plot_heatmap(spike_counts_baseline, 'baseline', excel_file, output_dir)

    # Plot and save the afterstim heatmap
    spike_counts_stim = dict(zip(df['Electrode'], df['num_of_spikes_stim']))
    plot_heatmap(spike_counts_stim, 'afterstim', excel_file, output_dir)

# create raster plot
if action == 3:
    create_raster_plot(raw_data_path)

# add file electrode_comparison_analysis
if action == 4:
    recording_comparison(file_path_compare1, file_path_compare2)

if action == 5:
    perform_statistical_tests(predictable_file, controller_file)
