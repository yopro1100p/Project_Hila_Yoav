import os
import tkinter as tk
from tkinter import filedialog, messagebox

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
from statistic_test import combine_and_compare


# Functionality wrapper
def plot_signal_action(channel_id, raw_data_path, sampling_rate):
    channel_analyzer = ChannelAnalyzer(raw_data_path, channel_id, sampling_rate)
    channel_analyzer.plot_signal()

def plot_heatmap_action(ex_name):
    plot_heatmap(ex_name)

def raster_plot_action(raw_data_path):
    create_raster_plot(raw_data_path)

def comparison_action(file_path_compare1, file_path_compare2):
    recording_comparison(file_path_compare1, file_path_compare2)

def stat_test_action(predictable_directory, controller_directory):
    combine_and_compare(predictable_directory, controller_directory)

# GUI setup
class NeuralAnalysisApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Neural Data Analysis GUI")
        self.geometry("500x400")

        self.sampling_rate = 10000
        self.raw_data_path = ""

        # Action Selection
        self.label = tk.Label(self, text="Choose Action")
        self.label.pack(pady=10)

        self.action_var = tk.IntVar()
        self.radio1 = tk.Radiobutton(self, text="1: Plot Signal", variable=self.action_var, value=1)
        self.radio2 = tk.Radiobutton(self, text="2: Plot Heatmap", variable=self.action_var, value=2)
        self.radio3 = tk.Radiobutton(self, text="3: Raster Plot", variable=self.action_var, value=3)
        self.radio4 = tk.Radiobutton(self, text="4: Electrode Comparison", variable=self.action_var, value=4)
        self.radio5 = tk.Radiobutton(self, text="5: Statistical Test", variable=self.action_var, value=5)

        self.radio1.pack()
        self.radio2.pack()
        self.radio3.pack()
        self.radio4.pack()
        self.radio5.pack()

        # Action button
        self.run_button = tk.Button(self, text="Run", command=self.run_action)
        self.run_button.pack(pady=20)

    def run_action(self):
        action = self.action_var.get()
        if action == 1:
            self.plot_signal()
        elif action == 2:
            self.plot_heatmap()
        elif action == 3:
            self.raster_plot()
        elif action == 4:
            self.electrode_comparison()
        elif action == 5:
            self.stat_test()
        else:
            messagebox.showerror("Error", "Please select a valid action")

    # Action methods
    def plot_signal(self):
        # Get channel ID and file path
        channel_id = int(self.get_input("Enter Channel ID"))
        self.raw_data_path = filedialog.askopenfilename(title="Select H5 File", filetypes=[("H5 files", "*.h5")])
        if self.raw_data_path:
            plot_signal_action(channel_id, self.raw_data_path, self.sampling_rate)

    def plot_heatmap(self):
        ex_name = self.get_input("Enter File Name for Heatmap")
        if ex_name:
            plot_heatmap_action(ex_name)

    def raster_plot(self):
        self.raw_data_path = filedialog.askopenfilename(title="Select H5 File", filetypes=[("H5 files", "*.h5")])
        if self.raw_data_path:
            raster_plot_action(self.raw_data_path)

    def electrode_comparison(self):
        file1 = filedialog.askopenfilename(title="Select Baseline File", filetypes=[("H5 files", "*.h5")])
        file2 = filedialog.askopenfilename(title="Select Stimulus File", filetypes=[("H5 files", "*.h5")])
        if file1 and file2:
            comparison_action(file1, file2)

    def stat_test(self):
        predictable_dir = filedialog.askdirectory(title="Select Predictable Directory")
        control_dir = filedialog.askdirectory(title="Select Control Directory")
        if predictable_dir and control_dir:
            stat_test_action(predictable_dir, control_dir)

    def get_input(self, prompt):
        return simpledialog.askstring("Input", prompt)

# Run the app
if __name__ == "__main__":
    app = NeuralAnalysisApp()
    app.mainloop()
