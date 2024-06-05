import tkinter as tk
from tkinter import messagebox
import h5py
import pandas as pd
import numpy as np
import McsPy
import matplotlib.pyplot as plt


# Finding Potential Spikes
def cells_with_high_std_deviation(array, threshold_factor=6):
    # Calculate the standard deviation of all the elements in the array
    overall_std_deviation = np.std(array)

    # Create a boolean mask where True represents cells with std deviation > threshold
    mask = np.abs(array - np.mean(array)) > (threshold_factor * overall_std_deviation)

    # Return the indices of cells where the condition is True
    return np.argwhere(mask)


# Prompt the user to select an HDF5 file
raw_data_path = "C:/Users/user/Desktop/bar ilan/Forth year/project/your_file.h5"

# load HDF5 file
data = McsPy.McsData.RawData(raw_data_path)

# Access the first recording, analog stream of electrodes (adjust indices as needed)
Data = data.recordings[0].analog_streams[2]
ChannelData = Data.channel_data



def Show(signal_id):
    plt.xlabel('Micro Sec')
    plt.ylabel('Volt')
    plt.title(f'Signal for Channel {signal_id}')
    plt.grid(True)
    plt.show()

# Placeholder function for all_graph
def all_graph(Samples_Vec, Time_Vec, signal_id):
    print("hello")
    plt.plot(Time_Vec, Samples_Vec)
    Show(signal_id)

# Placeholder function for spikes_graph

def spikes_graph(signal_id, starting_sample, ending_sample):
    # Placeholder function
    print(f"Spike Graph: Signal ID: {signal_id}, Starting Sample: {starting_sample}, Ending Sample: {ending_sample}")


# Function to handle button click event
def submit():
    try:
        signal_id = int(signal_id_entry.get())
        starting_sample = int(starting_sample_entry.get())
        ending_sample = int(ending_sample_entry.get())
        Samples_Vec = Data.get_channel_in_range(signal_id, starting_sample, ending_sample)[0]
        Time_Vec = Data.get_channel_sample_timestamps(signal_id, starting_sample, ending_sample)[0]

        choice = messagebox.askquestion("Graph Choice", "Do you want to view all graphs?")
        if choice == "yes":
            all_graph(Samples_Vec, Time_Vec, signal_id)
        else:
            specific_spike_graph(signal_id, starting_sample, ending_sample)
    except ValueError:
        messagebox.showerror("Error", "Please enter valid integers for Signal ID, Starting Sample, and Ending Sample.")


# Function to handle specific spike graph selection
def specific_spike_graph(signal_id, starting_sample, ending_sample):
    spikes_graph(signal_id, starting_sample, ending_sample)
    choice = messagebox.askquestion("Next Spike", "Do you want to view the next specific spike graph?")
    if choice == "yes":
        # Placeholder function to move to next spike graph
        print("Moving to next specific spike graph...")
        specific_spike_graph(signal_id, starting_sample, ending_sample)
    else:
        # Placeholder function to return to previous options
        print("Returning to previous options...")


# Create main window
root = tk.Tk()
root.title("Graph Generator")

# Create labels
tk.Label(root, text="Signal ID:").grid(row=0, column=0, padx=5, pady=5)
tk.Label(root, text="Starting Sample:").grid(row=1, column=0, padx=5, pady=5)
tk.Label(root, text="Ending Sample:").grid(row=2, column=0, padx=5, pady=5)

# Create entry fields
signal_id_entry = tk.Entry(root)
signal_id_entry.grid(row=0, column=1, padx=5, pady=5)

starting_sample_entry = tk.Entry(root)
starting_sample_entry.grid(row=1, column=1, padx=5, pady=5)

ending_sample_entry = tk.Entry(root)
ending_sample_entry.grid(row=2, column=1, padx=5, pady=5)

# Create submit button
submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

# Run the main event loop
root.mainloop()
