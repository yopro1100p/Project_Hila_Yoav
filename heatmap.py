import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Load spike counts from Excel file
# Replace 'example.xlsx' with the actual path to your Excel file
excel_file = 'example.xlsx'
df = pd.read_excel(excel_file)

# Assuming the Excel file has columns 'Electrode' and 'num_of_spikes'
spike_counts = dict(zip(df['Electrode'], df['num_of_spikes']))

# Channel dictionary (keep as it is)
channels_dict = {
    120: "G8", 119: "G12", 118: "G11", 117: "G10", 116: "G9", 115: "H12", 114: "H11", 113: "H10",
    112: "H9", 111: "J12", 110: "J11", 109: "J10", 108: "H8", 107: "K11", 106: "K10", 105: "L10",
    104: "J9", 103: "K9", 102: "L9", 101: "M9", 100: "J8", 99: "K8", 98: "L8", 97: "M8", 96: "J7",
    95: "K7", 94: "L7", 93: "M7", 92: "H7", 91: "G7", 90: "H6", 89: "M6", 88: "L6", 87: "K6", 86: "J6",
    85: "M5", 84: "L5", 83: "K5", 82: "J5", 81: "M4", 80: "L4", 79: "K4", 78: "H5", 77: "L3", 76: "K3",
    75: "K2", 74: "J4", 73: "J3", 72: "J2", 71: "J1", 70: "H4", 69: "H3", 68: "H2", 67: "H1", 66: "G4",
    65: "G3", 64: "G2", 63: "G1", 62: "G5", 61: "G6", 60: "F5", 59: "F1", 58: "F2", 57: "F3", 56: "F4",
    55: "E1", 54: "E2", 53: "E3", 52: "E4", 51: "D1", 50: "D2", 49: "D3", 48: "E5", 47: "C2", 46: "C3",
    45: "B3", 44: "D4", 43: "C4", 42: "B4", 41: "A4", 40: "D5", 39: "C5", 38: "B5", 37: "A5", 36: "D6",
    35: "C6", 34: "B6", 33: "A6", 32: "E6", 31: "F6", 30: "E7", 29: "A7", 28: "B7", 27: "C7", 26: "D7",
    25: "A8", 24: "B8", 23: "C8", 22: "D8", 21: "A9", 20: "B9", 19: "C9", 18: "E8", 17: "B10", 16: "C10",
    15: "C11", 14: "D9", 13: "D10", 12: "D11", 11: "D12", 10: "E9", 9: "E10", 8: "E11", 7: "E12", 6: "F9",
    5: "F10", 4: "F11", 3: "F12", 2: "F8", 1: "F7"
}

# Create a grid to match the MEA layout
grid_size = (12, 12)  # Adjust grid size to match your actual layout
heatmap = np.full(grid_size, np.nan)  # Initialize with NaN

# Fill the heatmap with spike counts
for idx, location in channels_dict.items():
    row = location[0]  # Extract row character (e.g., 'G')
    col = int(location[1:])  # Extract column number (e.g., '8')
    
    # Convert row character to index (assuming 'A' = 0, 'B' = 1, etc.)
    row_idx = ord(row) - ord('A')
    
    # Adjust for your specific grid layout if necessary
    if row_idx >= 8:
        row_idx -= 1
    
    # Set the spike count in the heatmap
    if 0 <= row_idx < grid_size[0] and 0 <= col - 1 < grid_size[1]:
        heatmap[row_idx, col - 1] = spike_counts.get(idx, 0)

# Custom colormap
colors = [(1, 1, 1), (1, 0, 0)]  # White to Red
n_bins = 1000  # Discretizes the interpolation into bins
cmap_name = 'dark_red'
cm = mcolors.LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)

# Plot the Heatmap
plt.figure(figsize=(12, 12))
cax = plt.imshow(heatmap, cmap=cm, interpolation='nearest', vmin=0, vmax=np.nanmax(heatmap))
plt.colorbar(cax, label='Spike Count')
plt.title('Heatmap of Electrode Spike Counts')

# Set labels for each electrode location
for i in range(grid_size[0]):
    for j in range(grid_size[1]):
        if not np.isnan(heatmap[i, j]):
            plt.text(j, i, f'{int(heatmap[i, j])}', ha='center', va='center', color='blue', fontsize=8)
plt.gca().invert_yaxis()  # Invert y-axis to match typical heatmap orientation
plt.show()
