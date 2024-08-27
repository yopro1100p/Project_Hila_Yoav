import os

import numpy as np
import pandas as pd
import scipy.stats as stats

# Load the data from the two experiments (predictable and controller)
predictable_file = '2024-06-13_21009_predictable.xlsx'
controller_file = '2024-06-13_21432_control.xlsx'
predictable_df = pd.read_excel(predictable_file)
controller_df = pd.read_excel(controller_file)

# Extract standard deviations for relevant metrics
std_columns = [
    'num_of_spikes_diff', 'num_of_bursts_diff', 'average_absolute_spikes_diff',
    'Spikes_rate_diff', 'spikes_per_bursts_diff'
]

# Initialize a dictionary to hold test results
test_results = {}

# Perform statistical tests on the standard deviations
for col in std_columns:
    # Perform Shapiro-Wilk test for normality on both datasets
    predictable_normality_p = stats.shapiro(predictable_df[col]).pvalue
    controller_normality_p = stats.shapiro(controller_df[col]).pvalue

    # If both datasets are normally distributed, use the t-test
    if predictable_normality_p > 0.05 and controller_normality_p > 0.05:
        test_stat, p_value = stats.ttest_ind(predictable_df[col], controller_df[col], equal_var=False)
        test_type = "t-test"
    else:
        # If not normally distributed, use the Mann-Whitney U test
        test_stat, p_value = stats.mannwhitneyu(predictable_df[col], controller_df[col])
        test_type = "Mann-Whitney U"

    test_results[col] = {"test_type": test_type, "statistic": test_stat, "p_value": p_value}

# Display the results
for metric, result in test_results.items():
    print(f"{metric} - {result['test_type']} statistic: {result['statistic']}, p-value: {result['p_value']}")

# Convert test results to a DataFrame
results_df = pd.DataFrame.from_dict(test_results, orient='index')

# Create the folder if it doesn't exist
output_folder = 'statistical_test_result'
os.makedirs(output_folder, exist_ok=True)

# Save the results to an Excel file in the specified folder
output_file_name = os.path.join(output_folder, "statistical_test_results_" + predictable_file.replace('predictable', ''))
results_df.to_excel(output_file_name)

print(f"Results saved to {output_file_name}")
