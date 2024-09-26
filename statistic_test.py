import os

import numpy as np
import pandas as pd
import scipy.stats as stats


def perform_statistical_tests(predictable_df, controller_df):
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

        # Check if the result is statistically significant (p-value < 0.05)
        significance = "Significant" if p_value < 0.05 else "Not Significant"

        test_results[col] = {
            "test_type": test_type,
            "statistic": test_stat,
            "p_value": p_value,
            "significance": significance
        }

    # Convert test results to a DataFrame
    results_df = pd.DataFrame.from_dict(test_results, orient='index')

    # Create the folder if it doesn't exist
    output_folder = 'statistical_test_result'
    os.makedirs(output_folder, exist_ok=True)

    # Generate the output filename for the combined results
    output_file_name = os.path.join(output_folder, "statistical_test_results_combined_predictable_vs_controller.xlsx")
    results_df.to_excel(output_file_name)

    print(f"Results saved to {output_file_name}")


def combine_and_compare(predictable_dir, controller_dir):
    # List all predictable and controller files
    predictable_files = [f for f in os.listdir(predictable_dir) if f.endswith('.xlsx') and 'predictable' in f]
    controller_files = [f for f in os.listdir(controller_dir) if f.endswith('.xlsx') and 'control' in f]

    # Combine all predictable data
    combined_predictable_df = pd.concat([pd.read_excel(os.path.join(predictable_dir, f)) for f in predictable_files])

    # Combine all controller data
    combined_controller_df = pd.concat([pd.read_excel(os.path.join(controller_dir, f)) for f in controller_files])

    # Perform the statistical tests on the combined data
    perform_statistical_tests(combined_predictable_df, combined_controller_df)


if __name__ == "__main__":
    # Set your directories for predictable and controller files
    predictable_directory = './predictable_folder'  # Replace with the path to the folder with predictable files
    controller_directory = './controller_folder'    # Replace with the path to the folder with controller files

    # Combine and compare data from all files
    combine_and_compare(predictable_directory, controller_directory)
