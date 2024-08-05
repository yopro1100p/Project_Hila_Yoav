import random
import time
from Chanels import ChannelAnalyzer
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from openpyxl import load_workbook

file_path = "C:/Users/user/Desktop/bar ilan/Forth year/project/your_file.h5"  # yoav's link
# file_path = "C:/Users/dvirg/OneDrive/Desktop/toar1/year4/project/CODE/your_file.h5"  # hilla's link

# Initialize the Excel file
output_file = "C:/Users/user/Desktop/bar ilan/Forth year/Project_Hila_Yoav/channel_analysis.xlsx"



start_time = time.time()  # Record the start time

# Initialize a list to collect all max_values_time for setting xlim
all_max_values_time = []

# Iterate over electrodes
for channel_id in range(1, 3):
    analyzer = ChannelAnalyzer(file_path, channel_id)
    analyzer.get_channel_data(channel_id)
    print(analyzer.find_num_of_spikes())

print("Analysis complete. Results saved")
end_time = time.time()  # Record the end time
elapsed_time = end_time - start_time  # Calculate the elapsed time
print(f"Elapsed time: {elapsed_time} seconds")


"""
# Iterate over electrodes
for electrode in range(1, 120):
    analyzer = Chanels.ChannelAnalyzer(file_path, electrode)
    analyzer.find_max_in_groups()
    analyzer.save_to_excel()

    # Print max_values_time for debugging
    print(f"Electrode {electrode + 1}, max_values_time: {analyzer.max_values_time}", color="red")

    # Collect max_values_time for setting xlim
    all_max_values_time.extend(analyzer.max_values_time)

    # Plot spikes for the current electrode
    plt.scatter(analyzer.max_values_time, [electrode + 1] * len(analyzer.max_values_time), color='blue', s=1)


ChannelAnalyzer.get_channel_data()
# Check if we have collected any time values for setting xlim
if all_max_values_time:
    plt.xlim(min(all_max_values_time), max(all_max_values_time))
else:
    print("No max_values_time found.")
"""