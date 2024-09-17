import os
import re

import matplotlib.pyplot as plt
import numpy as np
from McsPy.McsData import RawData

# File explanation
"""
    The ChannelAnalyzer class is designed to analyze neural signal data from specific channels in a multi-channel 
    recording system. It provides tools for loading data from HDF5 files (using McsPy), detecting spikes in the 
    signal, identifying bursts of spikes, and computing various statistics such as the number of spikes, average 
    spike amplitude, and burst rate.

    Attributes:
        file_path (str): The path to the HDF5 file containing the recording data.
        channel_id (int): The ID of the specific channel to analyze.
        sampling_rate (int): The sampling rate of the data (default is 10 kHz).
        dt (float): The time step between each sample, calculated from the sampling rate.
        data (McsPy.McsData.RawData): The raw data object loaded from the HDF5 file.
        analog_stream (McsPy.McsData.AnalogStream): The stream of analog data from the specified channel.
        channel_data (numpy array): The raw signal data for the specified channel.
        date (str): The recording date extracted from the HDF5 file.
        samples_vec (numpy array): The vector containing the signal samples for the selected channel.
        time_vec (numpy array): A time vector generated based on the length of the samples and the sampling rate.
        spikes_samples_vec (numpy array): A vector containing the spike values detected in the signal.
        spikes_samples_vec_time (numpy array): A vector containing the time indices of the spikes.
        group_of_spikes (list): A list grouping detected spikes together based on proximity in time.
        max_values (list): The maximum spike amplitude values in each detected group of spikes.
        max_values_time (list): The time indices corresponding to the maximum spike values.
        Average_Spikes (float): The average amplitude of spikes in the signal.
        Spikes_rate (float): The rate of spike occurrence relative to the total recording time.
        num_of_spikes (int): The total number of spikes detected in the signal.
        Group_Of_Bursts (list): Groups of spike bursts, where bursts are defined by a minimum number of spikes 
                                within a maximum time distance.
        active (bool): A flag indicating whether the channel contains enough spikes to be considered "active".
        spikes_per_burst (float): The average number of spikes per burst.
        burst_rate (float): The rate of burst occurrence relative to the total recording time.
        Num_Of_Bursts (int): The total number of bursts detected in the signal.
        comparable (bool): Indicates whether the channel can be compared to others (based on minimum spike count).
        burst_start_time (list): The time indices at which bursts begin.

    Methods:
        update_all(): Updates all class variables by calling various methods to find spikes, group them, compute 
                      statistics, and detect bursts.
        get_channel_data(channel_id): Retrieves the signal data for the specified channel.
        get_channel_data_time(channel_id): Retrieves the time stamps for the signal data of the specified channel.
        find_spikes(threshold_factor): Detects spikes in the signal by comparing the amplitude to a threshold 
                                       based on the standard deviation.
        grouping_samples_by_spikes(): Groups spikes together that occur close to each other in time.
        find_max_in_groups(): Identifies the maximum amplitude in each group of spikes.
        find_num_of_spikes(): Counts the total number of spikes in the signal.
        active_check(): Sets the 'active' flag based on the number of spikes detected.
        find_Average_Spikes(): Computes the average spike amplitude.
        find_burst(max_dist, min_spikes): Detects bursts of spikes based on proximity in time and a minimum number 
                                          of spikes.
        find_start_barst_time(): Identifies the start times of the detected bursts.
        plot_spikes_and_bursts(record_type): Generates a plot of the signal with vertical lines indicating the 
                                             positions of spikes and bursts, and saves the plot to a file.
    """


class ChannelAnalyzer:
    def __init__(self, file_path, channel_id, sampling_rate=10000):
        self.file_path = file_path
        self.channel_id = channel_id
        self.sampling_rate = sampling_rate
        self.dt = 1 / sampling_rate

        # Load the data
        self.data = RawData(self.file_path)  # change this
        self.analog_stream = self.data.recordings[0].analog_streams[2]
        self.channel_data = self.analog_stream.channel_data
        self.date = self.data.date

        # Get the samples and time vectors
        self.samples_vec = self.get_channel_data(self.channel_id)
        if self.samples_vec is None:
            print(f"Warning: No data found for channel ID {self.channel_id}")
            self.active = False
            return

        # self.time_vec = self.get_channel_data_time(self.channel_id)
        self.time_vec = np.arange(len(self.samples_vec)) / self.sampling_rate

        # variables of class
        self.spikes_samples_vec = None
        self.spikes_samples_vec_time = None
        self.group_of_spikes = None
        self.max_values = None  # the max values of spikes in electrode
        self.max_values_time = []  # the max time of spikes in electrode
        self.Average_Spikes = 0  # average of the spikes - amplitude
        self.Spikes_rate = 0  # the rate of the spikes in the electrode
        self.num_of_spikes = 0  # nm of spikes that we have in the electrode
        self.Group_Of_Bursts = None  # the burst in the electrod you need to give min num of spike in the berst and the max dist
        self.active = True
        self.spikes_per_burst = 0
        self.burst_rate = 0
        self.Num_Of_Bursts = 0
        self.comparable = False
        self.burst_start_time = None
        self.update_all()

    # updates all variables of the class
    def update_all(self):
        if self.find_spikes() == 0:
            self.grouping_samples_by_spikes()
            self.find_max_in_groups()
            self.find_num_of_spikes()
            self.active_check()
            self.find_Average_Spikes()
            self.Spikes_rate = self.num_of_spikes / len(self.time_vec)
            if self.find_burst(3, 3):  # change this to be - the num of burst 50 milisec
                self.Num_Of_Bursts = len(self.Group_Of_Bursts)
                self.burst_rate = self.Num_Of_Bursts / len(self.time_vec)
            if self.num_of_spikes >= 10:
                self.comparable = True
            self.find_start_burst_time()

    def get_channel_data(self, channel_id):
        channel_data = self.analog_stream.get_channel_in_range(channel_id, 0, self.analog_stream.channel_data.shape[1])
        if channel_data is None or len(channel_data) == 0:
            return None
        return channel_data[0]

    def get_channel_data_time(self, channel_id):
        channel_data = self.analog_stream.get_channel_sample_timestamps(channel_id, 0,
                                                                        self.analog_stream.channel_data.shape[1])
        if channel_data is None or len(channel_data) == 0:
            return None
        return channel_data[0]

    def find_spikes(self, threshold_factor=6):  # change the formula to find spiks
        overall_std_deviation = np.std(self.samples_vec)
        threshold_value = threshold_factor * overall_std_deviation
        mask = np.abs(self.samples_vec) > threshold_value
        if np.all(~mask):
            self.spikes_samples_vec = np.array([])
            self.spikes_samples_vec_time = np.array([])
            return 1
        self.spikes_samples_vec = self.samples_vec[np.argwhere(mask)].flatten()
        self.spikes_samples_vec_time = np.argwhere(mask).flatten()
        return 0

    def grouping_samples_by_spikes(self):
        spikes_samples_vec_time_differences = np.diff(self.spikes_samples_vec_time)
        self.group_of_spikes = []
        temp_array = []

        for i in range(spikes_samples_vec_time_differences.size):
            temp_array.append(self.spikes_samples_vec_time[i])
            if spikes_samples_vec_time_differences[i] != 1:
                self.group_of_spikes.append(temp_array)
                temp_array = []

        if temp_array or (
                spikes_samples_vec_time_differences.size > 0 and spikes_samples_vec_time_differences[-1] == 1):
            temp_array.append(self.spikes_samples_vec_time[-1])
            self.group_of_spikes.append(temp_array)

    def find_max_in_groups(self):
        self.grouping_samples_by_spikes()
        self.max_values = []
        self.max_values_time = []
        for arr in self.group_of_spikes:
            max_value_index = np.argmax(np.abs(self.samples_vec[arr]))
            self.max_values_time.append(arr[max_value_index])
            self.max_values.append(self.samples_vec[arr[max_value_index]])

    def find_num_of_spikes(self):
        self.num_of_spikes = len(self.max_values)
        return self.num_of_spikes

    def active_check(self):
        if self.num_of_spikes < 10:
            self.active = False

    def find_Average_Spikes(self):
        self.Average_Spikes = 0
        if self.max_values != 0:
            self.Average_Spikes = np.mean([abs(x) for x in self.max_values])
        return self.Average_Spikes

    def find_burst(self, max_dist, min_spikes):  # the dist is milisec?
        count = 0
        sum = 0
        temp = []
        self.Group_Of_Bursts = []
        for i in range(1, len(self.max_values_time) - 1):
            if len(self.max_values_time) == 1:
                temp.append(self.max_values_time[i])
                if len(temp) >= min_spikes:
                    self.Group_Of_Bursts.append(temp)
                    self.spikes_per_burst = 1
                return self.Group_Of_Bursts

            if (self.max_values_time[i + 1] - self.max_values_time[i]) <= max_dist:
                temp.append(self.max_values_time[i])
            else:
                temp.append(self.max_values_time[i])
                if len(temp) >= min_spikes:
                    self.Group_Of_Bursts.append(temp)
                    sum += len(temp)
                temp = []
        if len(self.Group_Of_Bursts) != 0:
            self.spikes_per_burst = sum / len(self.Group_Of_Bursts)
            return 1

        return 0

    def find_start_burst_time(self):
        self.burst_start_time = []
        for i in range(1, len(self.Group_Of_Bursts) - 1):
            self.burst_start_time.append(self.Group_Of_Bursts[1][1])
        return 0

    def plot_signal(self, record_type):
        output_dir = 'spikes_and_barst'
        os.makedirs(output_dir, exist_ok=True)
        for value in self.max_values_time:
            value = value / (10 ** 4)
            plt.axvline(x=value, ymin=0, ymax=0.06, color='r', linestyle='-')

        for v in self.burst_start_time:
            v = v / (10 ** 4)
            plt.axvline(x=value, ymin=0.94, ymax=1, color='b', linestyle='-')

        pattern = r'(\d{4}-\d{2}-\d{2})T\d{2}-\d{2}-\d{2}McsRecording_MEA(\d+)_(predictable|control)_(afterstim|baseline)'

        # Search for the pattern in the file path
        match = re.search(pattern, self.file_path)
        if match:
            date_part = match.group(1)  # Extracts "2024-06-13"
            mea_id = '#' + match.group(2)  # Extracts "23414"
            last_segment = match.group(3) + '_' + match.group(4)  # Extracts "predictable" or "control"

        # Generate graph name
        try:
            graph_name = f"{date_part}_{mea_id}_{last_segment}_electrd_{self.channel_id}"
        except Exception:
            graph_name = "dug"
        plt.plot(self.time_vec, self.samples_vec)
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude (microV)')
        plt.title(graph_name)
        plt.grid(True)
        plt.savefig(graph_name)
        plt.show()
