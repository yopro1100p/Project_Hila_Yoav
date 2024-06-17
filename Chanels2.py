import matplotlib.pyplot as plt
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

        # Get the samples and time vectors
        self.samples_vec = self.get_channel_data(self.channel_id)
        self.time_vec = np.arange(len(self.samples_vec)) / self.sampling_rate

        # Initialize spikes and groups
        self.spikes_samples_vec = None
        self.spikes_samples_vec_time = None
        self.group_of_spikes = None
        self.max_values = None
        self.max_values_time = None
        self.average_spikes = None
        self.spikes_samples_rate = None

    def get_channel_data(self, channel_id):
        # Get the data for the specified channel
        return self.analog_stream.get_channel_in_range(channel_id, 0, self.analog_stream.channel_data.shape[1])[0]

    def find_spikes(self, threshold_factor=6):
        # Find spikes in the channel data based on a threshold
        overall_std_deviation = np.std(self.samples_vec)
        threshold_value = threshold_factor * overall_std_deviation
        mask = np.abs(self.samples_vec - np.mean(self.samples_vec)) > threshold_value
        self.spikes_samples_vec = self.samples_vec[np.argwhere(mask)].flatten()
        self.spikes_samples_vec_time = np.argwhere(mask).flatten()

    def group_spikes(self):
        # Group detected spikes based on their proximity
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

    def find_max_in_groups(self):
        # Find the maximum values in each group of spikes
        self.group_spikes()
        self.max_values = []
        self.max_values_time = []
        
        for arr in self.group_of_spikes:
            max_value_index = np.argmax(self.samples_vec[arr])
            self.max_values_time.append(arr[max_value_index])
            self.max_values.append(self.samples_vec[arr[max_value_index]])

    def find_average_spikes(self):
        # Calculate the average of the maximum spike values
        self.find_max_in_groups()
        self.average_spikes = np.mean(self.max_values)

    def find_spikes_samples_rate(self):
        # Calculate the rate of spikes in the electrode
        self.spikes_samples_rate = np.diff(self.spikes_samples_vec_time)

    def plot(self):
        # Plot the signal and mark the spikes
        for time in self.max_values_time:
            plt.axvline(x=time / self.sampling_rate, ymin=0, ymax=0.06, color='r', linestyle='-')

        plt.plot(self.time_vec, self.samples_vec)
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude (V)')
        plt.title(f'Signal for Channel {self.channel_id}')
        plt.grid(True)
        plt.show()

# Usage example (uncomment and adjust the file path and channel_id as needed):
# file_path = "path_to_your_file.h5"
# channel_id = 13
# analyzer = ChannelAnalyzer(file_path, channel_id)
# analyzer.find_spikes()
# analyzer.find_max_in_groups()
# analyzer.find_average_spikes()
# analyzer.find_spikes_samples_rate()
# analyzer.plot()
# Main script to demonstrate the ChannelAnalyzer functionality
