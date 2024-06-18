"""
this main file is the original one, it is tiuta  do not delete things
"""
import h5py
import matplotlib.pyplot as plt
import McsPy
import numpy as np
import pandas as pd

import Chanels


def Grouping_Spikes_Samples(Spikes_Samples_Vec_Time_Differences, Spikes_Samples_Vec_Time, l):
    Group_Of_Spikes = []
    temp_array = []
    for i in range(0, Spikes_Samples_Vec_Time_Differences.size):
        temp_array.append(Spikes_Samples_Vec_Time[i])
        if Spikes_Samples_Vec_Time_Differences[i] != 1:
            Group_Of_Spikes.append(temp_array)
            temp_array = []

    if temp_array or Spikes_Samples_Differences[-1] == 1:
        temp_array.append(Spikes_Samples_Vec_Time[-1])
        Group_Of_Spikes.append(temp_array)

    k = 0
    for arr in Group_Of_Spikes:
        if k != l:
            print(arr)
            k = k + 1

    return Group_Of_Spikes


#
def find_Amplitud_Burst():
    return 1


def find_Spike_i(Spikes_Vec_Time, i, threshold_Value):
    return 1


def find_burst(max_dist, min_spkies, Group_Of_Spikes):
    count = 0
    i = 0
    temp = []
    Group_Of_Bursts = []
    for i in range(1, len(Group_Of_Spikes)-1):
        if len(Group_Of_Spikes) == 1:
            temp.append(Group_Of_Spikes[i])
            if (len(temp) >= min_spkies):
                Group_Of_Bursts.append(temp)
            return Group_Of_Bursts

        if (Group_Of_Spikes[i+1][0] - Group_Of_Spikes[i][-1]) <= max_dist:
            temp.append(Group_Of_Spikes[i])

        else:
            temp.append(Group_Of_Spikes[i])
            if (len(temp) >= min_spkies):
                Group_Of_Bursts.append(temp)
            temp = []
    # if len(Group_Of_Spikes) == 1:
    #     temp.append(Group_Of_Spikes[i])
    #     if (len(temp) >= min_spkies):
    #         Group_Of_Bursts.append(temp)
    #     temp = []
    return Group_Of_Bursts


# Finding Potential Spikes
def cells_with_high_std_deviation(array, threshold_factor=6):
    # Calculate the standard deviation of all the elements in the array
    overall_std_deviation = np.std(array)

    # Create a boolean mask where True represents cells with std deviation > threshold
    mask = np.abs(array - np.mean(array)) > (threshold_factor * overall_std_deviation)

    # Return the indices of cells where the condition is True
    return mask


# Prompt the user to select an HDF5 file
#raw_data_path = "C:/Users/user/Desktop/bar ilan/Forth year/project/your_file.h5"# YOAV'S LINK
raw_data_path = "C:/Users/dvirg/OneDrive/Desktop/toar1/year4/project/CODE/your_file.h5" #hilla's link


# load HDF5 file
data = McsPy.McsData.RawData(raw_data_path)

sampling_rate = 10000  # sample rate in Hz
dt = 1 / sampling_rate

# Access recordings from the HDF5 file


chan_MCS_filter = []

# Access the first recording, analog stream of electrodes (adjust indices as needed)
Data = data.recordings[0].analog_streams[2]
ChannelData = Data.channel_data

# showing the data is type of electrode
# print(Data.data_subtype)
# print(Data.channel_infos)


channel_id = 13
# Samples_Vec = Data.get_channel_in_range(channel_id, 0, 10000)[0]
# Time_Vec = Data.get_channel_sample_timestamps(channel_id, 0, 10000)[0]
Samples_Vec = Data.get_channel(channel_id)[0]
Time_Vec = np.arange(len(Samples_Vec)) / sampling_rate

# Standard Deviation
overall_std_deviation = np.std(Samples_Vec)
threshold_Value = 6 * overall_std_deviation

Spikes_Samples_Vec_Temp = cells_with_high_std_deviation(Samples_Vec, threshold_factor=6)

Spikes_Samples_Vec = Samples_Vec[np.argwhere(Spikes_Samples_Vec_Temp)].flatten()
# print("Spikes_Samples_Vec: ", Spikes_Samples_Vec)

Num_Of_Spikes_Samples = Spikes_Samples_Vec.size
print("\nNum_Of_Spikes: ", Num_Of_Spikes_Samples)

# time of spikes vector(indices)
Spikes_Samples_Vec_Time = np.argwhere(Spikes_Samples_Vec_Temp).flatten()
# print("\nSpikes_Vec_Time of the spikes: ", Spikes_Samples_Vec_Time)

# Average Spikes
Average_Spikes_Samples = np.mean(Spikes_Samples_Vec)
# print("\naverage of spikes: ", Average_Spikes_Samples)

# Amplitude of spikes
Spikes_Samples_Amp = np.mean(np.abs(Spikes_Samples_Vec))
# print("\nAmplitude of spikes: ", Spikes_Samples_Amp)

# Calculate the differences between neighboring elements
Spikes_Samples_Vec_Time_Differences = np.diff(Spikes_Samples_Vec_Time)
Spikes_Samples_Differences = np.diff(np.abs(Spikes_Samples_Vec))
# print("\nSpikes Samples Differences Vector Time: ", Spikes_Samples_Vec_Time_Differences)
# print("\nSpikes Samples Differences Vector: ", Spikes_Samples_Differences)


Spikes_Samples_rate = np.mean(Spikes_Samples_Differences)
# print("Spikes_rate: ", Spikes_rate, "us")

l = 6
Group_Of_Spikes = Grouping_Spikes_Samples(Spikes_Samples_Vec_Time_Differences, Spikes_Samples_Vec_Time, l)
l = len(Group_Of_Spikes)
max_values = []
k = 0

for arr in Group_Of_Spikes:
    if k != l:
        max_value_index = np.argmax(Samples_Vec[arr])

        max_values.append(arr[max_value_index])
        # print(arr[max_value_index])
        k += 1

min_spkies = 1
max_dist = 1
print("burst: ", find_burst(max_dist, min_spkies, Group_Of_Spikes))

for value in max_values:
    value = value / (10 ** 4)
    plt.axvline(x=value, ymin=0, ymax=0.06, color='r', linestyle='-')

plt.plot(Time_Vec, Samples_Vec)
plt.xlabel('Micro Sec')
plt.ylabel('Volt')
plt.title(f'Signal for Channel {channel_id}')
plt.grid(True)
plt.show()
"""
time_diffs = np.diff(Spikes_Vec_Time)
# Identify significant gaps (this threshold can be adjusted based on the data)
gap_threshold = 2
gaps = np.where(time_diffs > gap_threshold)[0]

# Define intervals based on gaps
intervals = []
start_idx = min(Spikes_Vec_Time)
for gap_idx in gaps:
    end_idx = gap_idx
    intervals.append((Spikes_Vec_Time[start_idx], Spikes_Vec_Time[end_idx]))
    start_idx = end_idx + 1
# Add the last interval
intervals.append((Spikes_Vec_Time[start_idx], Spikes_Vec_Time[-1]))

# Find maximum values in each interval
max_values = []
interval_centers = []

for start, end in intervals:
    mask = (Spikes_Vec_Time >= start) & (Spikes_Vec_Time <= end)
    max_value = np.max(Spikes_Vec[mask])
    max_values.append(max_value)

for value in max_value:
    value = value / (10 ** 4)
    plt.axvline(x=value, ymin=0, ymax=0.06, color='r', linestyle='-')

"""
"""
spike_min = 0
index = 0
for i in range(1, Num_Of_Spikes):
    if (Spikes_Vec[i] < 0):
        if (Spikes_Vec_Time[i] - Spikes_Vec_Time[i - 1]) == 1:
            spike_min = min(spike_min, Spikes_Vec_Time[i])
            index = spike_min / (10 ** 4)
        else:
            if(index != 0):
                plt.axvline(x=index, ymin=0, ymax=0.06, color='r', linestyle='-')
                spike_min = 0
                index = 0
            else:
                plt.axvline(x=Spikes_Vec[i], ymin=0, ymax=0.06, color='r', linestyle='-')
                spike_min = 0
                index = 0
"""

# print(Spikes_Samples_Vec_Time)


"""
# Iterate over the channels and filter the data
# for i in range(len(data.recordings[0].analog_streams[3].channel_data)):
# Filtered data (assuming filter applied during acquisition)
#  filtered_data = data.recordings[0].analog_streams[3].channel_data[i, :] * 1e-6
# chan_MCS_filter.append(filtered_data)

# Assuming all channels have the same length, get time vector
# t = np.arange(len(chan_MCS_filter[0])) / Fs

# Now chan_MCS_filter contains the filtered data for each channel, and t is the time vector
# You can proceed to save or further process the filtered data as needed


# Exel

# creating CSV of the data
# data_array = np.array(chan_MCS_filter)


# Create a Pandas DataFrame with the data
# df = pd.DataFrame(data_array.T)  # Transpose the array to have channels as columns

# Save the DataFrame to a CSV file
# csv_file_path = "C:/Users/user/Desktop/bar ilan/Forth year/project/output_data.csv"
# df.to_csv(csv_file_path, index=False)  # Set index=False to avoid writing ro
"""
"""
# Samples units = Volt
# timestamps units = microsecond
# Checking between all channels who have spikes
for channel_id in range(1, 120):
    Samples_Vec = Data.get_channel_in_range(channel_id, 0, 10000)[0]
    Time_Vec = Data.get_channel_sample_timestamps(channel_id, 0, 10000)[0]
    plt.plot(Time_Vec, Samples_Vec)
    plt.xlabel('Micro Sec')
    plt.ylabel('Volt')
    plt.title(f'Signal for Channel {channel_id}')
    plt.grid(True)
    plt.show()
    print("hey")
"""
