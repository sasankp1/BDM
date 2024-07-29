import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols

# Load dataset
file_path = '/Users/sasankchowdary/Downloads/walmart-sales-dataset-of-45stores.csv'
data = pd.read_csv(file_path)

# Display basic info
print(data.info())
print(data.describe())

# Example 1: Independent t-test on Weekly_Sales for Holiday vs Non-Holiday
def t_test(data, group_col, value_col):
    group1 = data[data[group_col] == 0][value_col]
    group2 = data[data[group_col] == 1][value_col]
    t_stat, p_val = stats.ttest_ind(group1, group2)
    return t_stat, p_val

# Example 2: ANOVA test for Weekly_Sales across different stores
def anova_test(data, dependent_var, independent_var):
    model = ols(f'{dependent_var} ~ C({independent_var})', data=data).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    return anova_table

# Example 3: Correlation test between Weekly_Sales and other variables
def correlation_test(data, value_col, *args):
    correlations = {}
    for col in args:
        corr, p_val = stats.pearsonr(data[value_col], data[col])
        correlations[col] = (corr, p_val)
    return correlations

# Perform tests
t_stat, t_p_val = t_test(data, 'Holiday_Flag', 'Weekly_Sales')
anova_table = anova_test(data, 'Weekly_Sales', 'Store')
correlations = correlation_test(data, 'Weekly_Sales', 'Temperature', 'Fuel_Price', 'CPI', 'Unemployment')

# Print results
print(f'T-test: t_stat = {t_stat}, p_val = {t_p_val}')
print(f'ANOVA test:\n{anova_table}')
print(f'Correlations:')
for var, (corr, p_val) in correlations.items():
    print(f'{var}: correlation = {corr}, p_val = {p_val}')

# Visualization
sns.set(style="whitegrid")

# Boxplot for Weekly_Sales by Holiday_Flag
plt.figure(figsize=(10, 6))
sns.boxplot(x='Holiday_Flag', y='Weekly_Sales', data=data)
plt.title('Weekly Sales by Holiday Flag')
plt.xlabel('Holiday Flag')
plt.ylabel('Weekly Sales')
plt.show()

# Boxplot for Weekly_Sales by Store
plt.figure(figsize=(14, 8))
sns.boxplot(x='Store', y='Weekly_Sales', data=data)
plt.title('Weekly Sales by Store')
plt.xlabel('Store')
plt.ylabel('Weekly Sales')
plt.xticks(rotation=90)
plt.show()

# Pairplot to visualize correlations
plt.figure(figsize=(12, 8))
sns.pairplot(data[['Weekly_Sales', 'Temperature', 'Fuel_Price', 'CPI', 'Unemployment']])
plt.suptitle('Pairplot of Key Factors', y=1.02)
plt.show()

# Heatmap of Correlations
plt.figure(figsize=(10, 6))
corr_matrix = data[['Weekly_Sales', 'Temperature', 'Fuel_Price', 'CPI', 'Unemployment']].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Heatmap of Correlations')
plt.show()
