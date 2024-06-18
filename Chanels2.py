import matplotlib.pyplot as plt
import numpy as np
from McsPy.McsData import RawData


class ChannelAnalyzer:
    def __init__(self, file_path, channel_id, sampling_rate=10000):
        """
        Initialize the ChannelAnalyzer with the provided file path, channel ID, and sampling rate.
        """
        self.file_path = file_path
        self.channel_id = channel_id
        self.sampling_rate = sampling_rate
        self.dt = 1 / sampling_rate

        # Load the data
        self.data = RawData(self.file_path)
        self.analog_stream = self.data.recordings[0].analog_streams[2]
        self.channel_data = self.analog_stream.channel_data

        # Get the samples and time vectors
        self.samples_vec = self.get_channel_data(self.channel_id)
        self.time_vec = np.arange(len(self.samples_vec)) / self.sampling_rate

        # Initialize spikes and groups
        self.spikes_samples_vec = None
        self.spikes_samples_vec_time = None
        self.group_of_spikes = None
        self.max_values = []  # the max values of spikes in electrode
        self.max_values_time = []  # the max time of spikes in electrode
        self.Average_Spikes = None  # average of the spikes - amplitude
        self.Spikes_Samples_rate = None  # the rate of the spikes in the electrode
        self.num_of_spikes = None  # number of spikes that we have in the electrode
        self.Group_Of_Bursts = None  # the bursts in the electrode

    def get_channel_data(self, channel_id):
        """
        Get the data for the specified channel.
        """
        return self.analog_stream.get_channel_in_range(channel_id, 0, self.analog_stream.channel_data.shape[1])[0]

    def find_spikes(self, threshold_factor=6):
        """
        Detect spikes in the signal based on a threshold.
        The threshold is calculated as threshold_factor times the standard deviation of the signal.
        """
        overall_std_deviation = np.std(self.samples_vec)
        threshold_value = threshold_factor * overall_std_deviation
        mask = np.abs(self.samples_vec - np.mean(self.samples_vec)) > threshold_value
        self.spikes_samples_vec = self.samples_vec[np.argwhere(mask)].flatten()
        self.spikes_samples_vec_time = np.argwhere(mask).flatten()

    def group_spikes(self):
        """
        Group spikes based on the differences in their sample times.
        """
        spikes_samples_vec_time_differences = np.diff(self.spikes_samples_vec_time)
        self.group_of_spikes = []
        temp_array = []

        for i in range(spikes_samples_vec_time_differences.size):
            temp_array.append(self.spikes_samples_vec_time[i])
            if spikes_samples_vec_time_differences[i] != 1:
                self.group_of_spikes.append(temp_array)
                temp_array = []

        if temp_array or (spikes_samples_vec_time_differences.size > 0 and spikes_samples_vec_time_differences[-1] == 1):
            temp_array.append(self.spikes_samples_vec_time[-1])
            self.group_of_spikes.append(temp_array)
        return self.group_of_spikes

    def find_max_in_groups(self):
        """
        Identify the maximum values and their corresponding times in each group of spikes.
        """
        self.group_spikes()
        self.max_values = []
        self.max_values_time = []
        for arr in self.group_of_spikes:
            max_value_index = np.argmax(self.samples_vec[arr])
            self.max_values_time.append(arr[max_value_index])
            self.max_values.append(self.samples_vec[arr[max_value_index]])

    def find_Average_Spikes(self):
        """
        Calculate the average of the maximum spike values.
        """
        self.find_max_in_groups()
        self.Average_Spikes = np.mean(self.max_values)
        return self.Average_Spikes

    def finding_Spikes_Samples_rate(self):
        """
        Calculate the rate of the detected spikes.
        """
        self.Spikes_Samples_rate = np.diff(self.spikes_samples_vec_time)
        return self.Spikes_Samples_rate

    def find_num_of_spikes(self):
        """
        Count the number of detected spikes.
        """
        self.find_max_in_groups()
        self.num_of_spikes = len(self.max_values)
        return self.num_of_spikes

    def find_burst(self, max_dist, min_spikes):
        """
        Identify bursts of spikes based on the maximum allowable distance between spikes and 
        the minimum number of spikes required in a burst.
        """
        self.find_max_in_groups()
        temp = []
        self.Group_Of_Bursts = []
        for i in range(len(self.max_values_time)):
            if len(self.max_values_time) == 1:
                temp.append(self.max_values_time[i])
                if len(temp) >= min_spikes:
                    self.Group_Of_Bursts.append(temp)
                return self.Group_Of_Bursts

            if i < len(self.max_values_time) - 1 and (self.max_values_time[i + 1] - self.max_values_time[i]) <= max_dist:
                temp.append(self.max_values_time[i])
            else:
                temp.append(self.max_values_time[i])
                if len(temp) >= min_spikes:
                    self.Group_Of_Bursts.append(temp)
                temp = []
        return self.Group_Of_Bursts

    def plot(self):
        """
        Plot the signal and mark the detected spikes.
        """
        for value in self.max_values_time:
            plt.axvline(x=value, ymin=0, ymax=0.06, color='r', linestyle='-')

        plt.plot(self.time_vec, self.samples_vec)
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude (V)')
        plt.title(f'Signal for Channel {self.channel_id}')
        plt.grid(True)
        plt.show()

# Usage example
"""
file_path = "C:/Users/user/Desktop/bar ilan/Forth year/project/your_file.h5"
channel_id = 109

analyzer = ChannelAnalyzer(file_path, channel_id)
analyzer.find_spikes()
analyzer.group_spikes()
analyzer.find_max_in_groups()
bursts = analyzer.find_burst(max_dist=10, min_spikes=3)  # Example values for max_dist and min_spikes
print(f"Bursts: {bursts}")
analyzer.plot()
"""
