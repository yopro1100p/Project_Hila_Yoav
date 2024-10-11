import os

import matplotlib.pyplot as plt
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

    # Plotting the mean and standard deviation for each metric
    plot_mean_std_for_each_metric(predictable_df, controller_df, std_columns, results_df)


def plot_mean_std_for_each_metric(predictable_df, controller_df, std_columns, results_df):
    # Create the output folder for plots if it doesn't exist
    output_folder = 'statistical_test_result'
    os.makedirs(output_folder, exist_ok=True)

    # Loop through each column to create a separate plot
    for col in std_columns:
        # Calculate the mean and standard deviation for the current column
        mean_predictable = predictable_df[col].mean()
        std_predictable = predictable_df[col].std()

        mean_controller = controller_df[col].mean()
        std_controller = controller_df[col].std()

        # Create the plot
        fig, ax = plt.subplots(figsize=(8, 5))

        # Bar positions
        bar_positions = np.arange(2)

        # Plot bars for predictable and controller data
        bars = ax.bar(bar_positions, [mean_predictable, mean_controller], 
                      yerr=[std_predictable, std_controller], 
                      capsize=5, color=['skyblue', 'lightgreen'], 
                      edgecolor='black')

        # Add labels and title
        ax.set_xlabel('Groups')
        ax.set_ylabel('Mean Values')
        ax.set_title(f'Mean and Standard Deviation for {col}')
        ax.set_xticks(bar_positions)
        ax.set_xticklabels(['Predictable', 'Control'])
        
        # Add grid
        ax.grid(True)

        # Check if the test result for this column was significant
        if results_df.loc[col, 'significance'] == 'Significant':
            # Draw a red line connecting the two bars
            max_height = max(mean_predictable + std_predictable, mean_controller + std_controller) + 0.05 * max(mean_predictable + std_predictable, mean_controller + std_controller)
            ax.plot([0, 1], [max_height, max_height], color='red', linewidth=2)
            ax.text(0.5, max_height + 0.02 * max_height, '*', ha='center', color='red', fontsize=12)

        # Add custom annotations to explain the significance markers
        #ax.text(1.05, 1, '* = Statistically Significant Difference', transform=ax.transAxes, fontsize=10, color='red')
        #ax.text(1.05, 0.95, 'Red Line = Connects bars with significant differences', transform=ax.transAxes, fontsize=10, color='red')
        #ax.text(1.05, 0.90, 'Black Lines = Standard Deviation', transform=ax.transAxes, fontsize=10, color='black')

        # Save the plot to a file in the 'statistical_test_result' folder
        plot_file_name = os.path.join(output_folder, f"{col}_mean_std_comparison_plot.png")
        plt.tight_layout()
        plt.savefig(plot_file_name)

        print(f"Plot saved to {plot_file_name}")
        plt.close(fig)  # Close the figure to avoid display


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
