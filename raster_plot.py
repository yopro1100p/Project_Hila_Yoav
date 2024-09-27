import os
import re

import matplotlib.pyplot as plt

from Chanels import ChannelAnalyzer

# File path
#file_path = r"C:\Users\dvirg\OneDrive\Desktop\toar1\year4\project\CODE\recorders\2024-06-13T17-31-24McsRecording_MEA23414_predictable_baseline_A-00020.h5"
# Regex pattern to extract the date, MEA ID, and the last segment (predictable or control)

def create_raster_plot(file_path):
    pattern = r'(\d{4}-\d{2}-\d{2})T\d{2}-\d{2}-\d{2}McsRecording_MEA(\d+)_(predictable|control)_(afterstim|baseline)'

    # Search for the pattern in the file path
    match = re.search(pattern, file_path)
    if match:
        date_part = match.group(1)  # Extracts "2024-06-13"
        mea_id = '#' + match.group(2)  # Extracts "23414"
        last_segment = match.group(3) + '_' + match.group(4)  # Extracts "predictable" or "control"

        output_dir = 'raster_plot'
        os.makedirs(output_dir, exist_ok=True)

        # Initialize a list to collect all max_values_time for setting xlim
        all_max_values_time = []

        # Iterate over electrodes
        for electrode in range(0, 120):  # Assuming electrodes range from 1 to 120
            print(electrode)
            analyzer = ChannelAnalyzer(file_path, electrode)
            analyzer.get_channel_data(electrode)

            # Print max_values_time for debugging
            # print(f"Electrode {electrode+1}, max_values_time: {analyzer.max_values_time}")

            # Collect max_values_time for setting xlim
            all_max_values_time.extend(analyzer.max_values_time)

            # Plot spikes for the current electrode
            plt.scatter(analyzer.max_values_time, [electrode + 1] * len(analyzer.max_values_time), color='blue', s=1)

        # Check if we have collected any time values for setting xlim
        if all_max_values_time:
            plt.xlim(min(all_max_values_time), max(all_max_values_time))
        else:
            print("No max_values_time found.")

        # Set the title using the desired format
        plot_title = f"raster_plot_{date_part}_{mea_id}_{last_segment}"
        plt.title(plot_title)

        # Save the plot in the 'raster_plot' directory
        output_filename = os.path.join(output_dir, f"{plot_title}.png")

        # Show the plot
        plt.xlabel('Time (s)')
        plt.ylabel('Electrode')
        plt.savefig(output_filename)
        plt.show()
    else:
        print("The file path does not match the expected pattern.")
