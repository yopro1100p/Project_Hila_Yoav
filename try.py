import re

import pandas as pd

from Chanels import ChannelAnalyzer

# Paths to the HDF5 files for the two recordings
file_path1 = "C:/Users/dvirg/OneDrive/Desktop/toar1/year4/project/CODE/2024-02-01T14-33-39McsRecording_MEA21009_baseline_A-00020.h5"  # Replace with the actual path to baseline file
file_path2 = "C:/Users/dvirg/OneDrive/Desktop/toar1/year4/project/CODE/2024-02-01T14-54-37McsRecording_MEA21009_predictable_aferstim_A-00020.h5"  # Replace with the actual path to stimulus file

# Extract the experiment number from the file path using regex
experiment_number = re.search(r'MEA(\d+)_', file_path1).group(1)

# Define the output file name based on the experiment number
output_file = f'{experiment_number}.xlsx'

# Step 1: Load existing Excel file (if any)
try:
    df = pd.read_excel(output_file)
except FileNotFoundError:
    # If file doesn't exist, create a new DataFrame
    data = {
        'Electrode': [f'{i + 1}' for i in range(120)],
        'num_of_spikes_baseline': [0.0] * 120,
        'num_of_bursts_baseline': [0.0] * 120,
        'average_absolute_spikes_baseline': [0.0] * 120,
        'Spikes_rate_baseline': [0.0] * 120,
        'spikes_per_bursts_baseline': [0.0] * 120,
        'comperable_baseline':[None]*120,
        'stim': [None] * 120,
        'num_of_spikes_stim': [0.0] * 120,
        'num_of_bursts_stim': [0.0] * 120,
        'average_absolute_spikes_stim': [0.0] * 120,
        'Spikes_rate_stim': [0.0] * 120,
        'spikes_per_bursts_stim': [0.0] * 120,
        'comperable_stim': [None] * 120,
        # Columns for the differences between the recordings
        'diff': [None] * 120,
        'num_of_spikes_diff': [0.0] * 120,
        'num_of_spikes_diff_precent': [0.0] * 120,
        'num_of_bursts_diff': [0.0] * 120,
        'num_of_bursts_diff_precent': [0.0] * 120,
        'average_absolute_spikes_diff': [0.0] * 120,
        'average_absolute_spikes_diff_precent': [0.0] * 120,
        'Spikes_rate_diff': [0.0] * 120,
        'Spikes_rate_diff_precent': [0.0] * 120,
        'spikes_per_bursts_diff': [0.0] * 120,
        'spikes_per_bursts_diff_precent': [0.0] * 120,
        'got_into_the_comper': [None] * 120,  # New column to track updates
        'negative_diff':[None]*120,
        'positive_diff':[None]*120,
    }
    df = pd.DataFrame(data)

# Step 2: Ensure the columns are of type float
df = df.astype({
    'num_of_spikes_baseline': 'float64',
    'num_of_bursts_baseline': 'float64',
    'average_absolute_spikes_baseline': 'float64',
    'Spikes_rate_baseline': 'float64',
    'spikes_per_bursts_baseline': 'float64',
    'num_of_spikes_stim': 'float64',
    'num_of_bursts_stim': 'float64',
    'average_absolute_spikes_stim': 'float64',
    'Spikes_rate_stim': 'float64',
    'spikes_per_bursts_stim': 'float64',
    'num_of_spikes_diff': 'float64',
    'num_of_bursts_diff': 'float64',
    'average_absolute_spikes_diff': 'float64',
    'Spikes_rate_diff': 'float64',
    'spikes_per_bursts_diff': 'float64'
})

# Step 3: Perform calculations and update the DataFrame
for electrode_num in range(120):
    print(f"The number of the electrode now is: {electrode_num}")
    analyzer1 = ChannelAnalyzer(file_path1, electrode_num)
    analyzer2 = ChannelAnalyzer(file_path2, electrode_num)

    # Update values for record1 (baseline)
    df.at[electrode_num, 'num_of_spikes_baseline'] = analyzer1.num_of_spikes
    df.at[electrode_num, 'average_absolute_spikes_baseline'] = analyzer1.Average_Spikes
    df.at[electrode_num, 'Spikes_rate_baseline'] = analyzer1.Spikes_rate
    df.at[electrode_num, 'comperable_baseline'] = analyzer1.comparable
    if analyzer1.Num_Of_Bursts != 0:
        df.at[electrode_num, 'num_of_bursts_baseline'] = analyzer1.Num_Of_Bursts
        df.at[electrode_num, 'spikes_per_bursts_baseline'] = analyzer1.spikes_per_burst

    # Update values for record2 (stimulus)
    df.at[electrode_num, 'num_of_spikes_stim'] = analyzer2.num_of_spikes
    df.at[electrode_num, 'average_absolute_spikes_stim'] = analyzer2.Average_Spikes
    df.at[electrode_num, 'Spikes_rate_stim'] = analyzer2.Spikes_rate
    df.at[electrode_num, 'comperable_stim'] = analyzer2.comparable
    if analyzer2.Num_Of_Bursts != 0:
        df.at[electrode_num, 'num_of_bursts_stim'] = analyzer2.Num_Of_Bursts
        df.at[electrode_num, 'spikes_per_bursts_stim'] = analyzer2.spikes_per_burst

    # Calculate the differences between the two recordings
    if (analyzer1.comparable == False) and (analyzer2.comparable == False):
        df.at[electrode_num, 'got_into_the_comper'] = 'False'
    else:
        df.at[electrode_num, 'num_of_spikes_diff'] = analyzer2.num_of_spikes - analyzer1.num_of_spikes
        if analyzer2.num_of_spikes - analyzer1.num_of_spikes > 0:
            df.at[electrode_num, 'positive_diff'] = 'True'
        else:
            if analyzer2.num_of_spikes - analyzer1.num_of_spikes < 0:
                df.at[electrode_num, 'negative_diff'] = 'try'
        if analyzer2.num_of_spikes != 0:
            df.at[electrode_num, 'num_of_spikes_diff_precent'] = (analyzer2.num_of_spikes - analyzer1.num_of_spikes) * 100 / analyzer2.num_of_spikes
        df.at[electrode_num, 'average_absolute_spikes_diff'] = analyzer2.Average_Spikes - analyzer1.Average_Spikes
        if analyzer2.Average_Spikes != 0:
            df.at[electrode_num, 'average_absolute_spikes_diff_precent'] = (analyzer2.Average_Spikes - analyzer1.Average_Spikes) * 100 / analyzer2.Average_Spikes
        df.at[electrode_num, 'Spikes_rate_diff'] = analyzer2.Spikes_rate - analyzer1.Spikes_rate
        if analyzer2.Spikes_rate != 0:
            df.at[electrode_num, 'Spikes_rate_diff_precent'] = (analyzer2.Spikes_rate - analyzer1.Spikes_rate) * 100 / analyzer2.Spikes_rate
        if analyzer2.Num_Of_Bursts != 0:
            df.at[electrode_num, 'num_of_bursts_diff'] = analyzer2.Num_Of_Bursts - analyzer1.Num_Of_Bursts
            df.at[electrode_num, 'num_of_bursts_diff_precent'] = (analyzer2.Num_Of_Bursts - analyzer1.Num_Of_Bursts) * 100 / analyzer2.Num_Of_Bursts
            df.at[electrode_num, 'spikes_per_bursts_diff'] = analyzer2.spikes_per_burst - analyzer1.spikes_per_burst
            df.at[electrode_num, 'spikes_per_bursts_diff_precent'] = (analyzer2.spikes_per_burst - analyzer1.spikes_per_burst) * 100 / analyzer2.spikes_per_burst
        df.at[electrode_num, 'got_into_the_comper'] = 'True'

# Step 4: Calculate averages and standard deviations
average_std_columns_baseline_stim = [
    'num_of_spikes_baseline', 'num_of_bursts_baseline', 'average_absolute_spikes_baseline', 
    'Spikes_rate_baseline', 'spikes_per_bursts_baseline',
    'num_of_spikes_stim', 'num_of_bursts_stim', 'average_absolute_spikes_stim', 
    'Spikes_rate_stim', 'spikes_per_bursts_stim'
]
average_std_columns_diff = [
    'num_of_spikes_diff', 'num_of_bursts_diff', 'average_absolute_spikes_diff', 
    'Spikes_rate_diff', 'spikes_per_bursts_diff'
]

# Initialize dictionaries to hold the results
averages = {}
std_devs = {}

# Calculate averages and standard deviations for baseline and stim columns (without any filtering)
for col in average_std_columns_baseline_stim:
    averages[col] = df[col].mean()
    std_devs[col] = df[col].std()

# Calculate averages and standard deviations for diff columns (only when 'got_into_the_comper' is True)
filtered_df = df[df['got_into_the_comper'] == 'True']  # Filter rows where 'got_into_the_comper' is 'True'

for col in average_std_columns_diff:
    averages[col] = filtered_df[col].mean()
    std_devs[col] = filtered_df[col].std()

# Create DataFrames for averages and standard deviations with labels
average_row = pd.DataFrame([averages], index=['Average'])
std_dev_row = pd.DataFrame([std_devs], index=['Std Dev'])

# Append the new rows to the end of the DataFrame
df_with_calculations = pd.concat([df, average_row, std_dev_row], ignore_index=True)

# Save the updated DataFrame to the Excel file
df_with_calculations.to_excel(output_file, index=False)

print(f'Data successfully updated and written to {output_file}')
