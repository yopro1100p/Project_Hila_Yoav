import os

import numpy as np
from McsPy.McsData import RawData


class ChannelAnalyzer:
    def __init__(self, file_path, channel_id, sampling_rate=10000):
        self.file_path = file_path
        self.channel_id = channel_id
        self.sampling_rate = sampling_rate
        self.dt = 1 / sampling_rate

        # Load the data
        self.data = RawData(self.file_path)
        self.analog_stream = self.data.recordings[0].analog_streams[2]
        self.channel_data = self.analog_stream.channel_data
        self.date = self.data.date

        # Get the samples and time vectors
        self.samples_vec = self.get_channel_data(self.channel_id)
        if self.samples_vec is None:
            print(f"Warning: No data found for channel ID {self.channel_id}")
            self.active = False
            return

        self.time_vec = np.arange(len(self.samples_vec)) / self.sampling_rate

        # variables of class
        self.spikes_samples_vec = None
        self.spikes_samples_vec_time = None
        self.group_of_spikes = None
        self.max_values = None  # the max values of spikes in electrod
        self.max_values_time = []  # the max time of spikes in electrod
        self.Average_Spikes = 0  # average of the spikes - amplitude
        self.Spikes_rate = 0  # the rate of the spikes in the electrode
        self.num_of_spikes = 0  # nm of spikes that we have in the electrod
        self.Group_Of_Bursts = None  # the burst in the electrod you need to give min num of spike in the berst and the max dist
        self.active = True
        self.spikes_per_burst = 0
        self.burst_rate = 0
        self.Num_Of_Bursts = 0
        self.comparable = False
        self.num_of_spikes_in_berst=None
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
            if self.find_burst(3, 3):
                self.Num_Of_Bursts = len(self.Group_Of_Bursts)
                self.burst_rate = self.Num_Of_Bursts / len(self.time_vec)
            if self.num_of_spikes >= 10:
                self.comparable = True

    def get_channel_data(self, channel_id):
        channel_data = self.analog_stream.get_channel_in_range(channel_id, 0, self.analog_stream.channel_data.shape[1])
        if channel_data is None or len(channel_data) == 0:
            return None
        return channel_data[0]

    def find_spikes(self, threshold_factor=6):
        overall_std_deviation = np.std(self.samples_vec)
        threshold_value = threshold_factor * overall_std_deviation
        mask = np.abs(self.samples_vec - np.mean(self.samples_vec)) > threshold_value
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

    def find_burst(self, max_dist, min_spikes):
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

    def find_

    def plot(self, record_type):
        for value in self.max_values_time:
            value = value / (10 ** 4)
            plt.axvline(x=value, ymin=0, ymax=0.06, color='r', linestyle='-')

        plt.plot(self.time_vec, self.samples_vec)
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude (V)')
        if record_type:
            plt.title(f'Electrode: {self.channel_id}, {self.date}, baseline')
        else:
            plt.title(f'Electrode: {self.channel_id}, {self.date}, stimulus')
        plt.grid(True)
        plt.show()
