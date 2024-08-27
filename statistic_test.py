import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu, shapiro, ttest_ind

# Load the data from the two experiments (predictable and controller)
data_predictable = pd.read_excel('predictable.xlsx')
data_controller = pd.read_excel('controller.xlsx')

# Define the columns you want to compare (e.g., standard deviations)
column_to_compare = 'std_dev'  # Replace with the actual column name

# Extract the relevant data
predictable_data = data_predictable[column_to_compare].values
controller_data = data_controller[column_to_compare].values

# Check for normality using the Shapiro-Wilk test
shapiro_predictable = shapiro(predictable_data)
shapiro_controller = shapiro(controller_data)

# Function to decide on the test to perform
def choose_statistical_test(data1, data2, shapiro1, shapiro2):
    alpha = 0.05  # Significance level for normality test
    
    if shapiro1.pvalue > alpha and shapiro2.pvalue > alpha:
        # Both datasets follow a normal distribution, use t-test
        t_stat, p_value = ttest_ind(data1, data2)
        test_name = "T-Test"
    else:
        # At least one dataset does not follow a normal distribution, use Mann-Whitney U test
        t_stat, p_value = mannwhitneyu(data1, data2)
        test_name = "Mann-Whitney U Test"
    
    return test_name, t_stat, p_value

# Perform the appropriate statistical test
test_name, test_statistic, p_value = choose_statistical_test(
    predictable_data, controller_data, shapiro_predictable, shapiro_controller
)

# Print the results
print(f"Statistical Test: {test_name}")
print(f"Test Statistic: {test_statistic}")
print(f"P-Value: {p_value}")

# Interpret the results
alpha = 0.05
if p_value < alpha:
    print("Reject the null hypothesis: There is a significant difference between the two groups.")
else:
    print("Fail to reject the null hypothesis: No significant difference between the two groups.")
