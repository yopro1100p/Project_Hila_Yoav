import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

import h5py
import matplotlib.pyplot as plt
import McsPy
import numpy as np
import pandas as pd
from McsPy.McsData import RawData
from PIL import Image, ImageTk  # Import Pillow for image handling

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


# Main application
class NeuralAnalysisApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Neural Data Analysis GUI")
        self.geometry("700x500")
        self.configure(bg="#00008B")  # Set screen background to dark blue

        # Show the welcome screen first
        self.show_welcome_screen()

    def show_welcome_screen(self):
        self.clear_window()

        # Load image (change 'welcome_image.png' to your image path)
        image = Image.open("welcome_image.jpeg")  # Make sure the image is in the same directory or provide full path
        image = image.resize((400, 200), Image.Resampling.LANCZOS)
        # Resize the image to fit the window
        photo = ImageTk.PhotoImage(image)

        # Add image to label
        image_label = tk.Label(self, image=photo, bg="#00008B")  # Set dark blue background for image
        image_label.image = photo  # Keep a reference to the image to avoid garbage collection
        image_label.pack(pady=20)

        welcome_label = tk.Label(
            self,
            text="Exploring the Impact of Electrical Stimuli on Neuronal Network Activity\nin Brain-Machine Interfaces",
            font=("Arial", 18, "bold"),
            fg="#FFFFFF",  # Set text color to white
            bg="#00008B",  # Set label background to dark blue (same as screen)
            wraplength=600,
            justify="center",
        )
        welcome_label.pack(pady=10)

        # Add the additional text in light blue and smaller size
        authors_label = tk.Label(
            self,
            text="Hilla Cohen and Yoav Gorman",
            font=("Arial", 14),  # Smaller font
            fg="#ADD8E6",  # Light blue color
            bg="#00008B",  # Set background color to dark blue (same as screen)
            justify="center",
        )
        authors_label.pack(pady=5)

        start_button = tk.Button(
            self,
            text="Start",
            command=self.show_main_menu,
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            width=10,
            height=2
        )
        start_button.pack(pady=20)

    def show_main_menu(self):
        self.clear_window()

        # Main menu
        self.sampling_rate = 10000
        self.raw_data_path = ""

        # Label styling
        label = tk.Label(self, text="Choose Action", font=("Arial", 14, "bold"), fg="#FFFFFF", bg="#00008B")  # Dark blue background
        label.pack(pady=20)

        # Radio buttons styling
        self.action_var = tk.IntVar()
        self.radio1 = self.create_radio_button("1: Plot Signal", 1)
        self.radio2 = self.create_radio_button("2: Plot Heatmap", 2)
        self.radio3 = self.create_radio_button("3: Raster Plot", 3)
        self.radio4 = self.create_radio_button("4: Electrode Comparison", 4)
        self.radio5 = self.create_radio_button("5: Statistical Test", 5)

        # Action button
        run_button = tk.Button(self, text="Run", command=self.run_action, font=("Arial", 12, "bold"),
                               bg="#4CAF50", fg="white", width=15, height=2)
        run_button.pack(pady=30)

    def create_radio_button(self, text, value):
        radio = tk.Radiobutton(self, text=text, variable=self.action_var, value=value, font=("Arial", 12),
                               bg="#00008B", activebackground="#D3D3D3", fg="#FFFFFF")  # Dark blue background, white text
        radio.pack(pady=5, anchor="w")
        return radio

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

    def clear_window(self):
        """Clears all widgets from the window."""
        for widget in self.winfo_children():
            widget.destroy()


# Run the app
if __name__ == "__main__":
    app = NeuralAnalysisApp()
    app.mainloop()
