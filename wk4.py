# Q5:
# Implement Data Pre-Processing Methods (AutoMPG Dataset)
# 1. Remove outliers / missing values using:
#    Percentiles, Standard Deviation, IQR, Z-Score
# 2. Imputing standard values
# 3. Capping of values

import pandas as pd
import numpy as np
from scipy import stats

# Load dataset
df = pd.read_csv("auto-mpg.csv")

# ------------------------------------------------------
# Handle missing values

# Replace '?' with NaN
df.replace('?', np.nan, inplace=True)

# Convert to numeric
df['horsepower'] = pd.to_numeric(df['horsepower'])

# Fill missing values with mean (Imputing standard values)
df['horsepower'].fillna(df['horsepower'].mean(), inplace=True)


# ------------------------------------------------------
# 1A. Remove outliers using Percentiles

lower = df['mpg'].quantile(0.05)
upper = df['mpg'].quantile(0.95)

df_percentile = df[(df['mpg'] >= lower) & (df['mpg'] <= upper)]


# ------------------------------------------------------
# 1B. Remove outliers using Standard Deviation

mean = df['mpg'].mean()
std = df['mpg'].std()

df_std = df[(df['mpg'] >= mean - 3*std) & (df['mpg'] <= mean + 3*std)]


# ------------------------------------------------------
# 1C. Remove outliers using IQR

Q1 = df['mpg'].quantile(0.25)
Q3 = df['mpg'].quantile(0.75)

IQR = Q3 - Q1

LL = Q1 - 1.5 * IQR
UL = Q3 + 1.5 * IQR

df_iqr = df[(df['mpg'] >= LL) & (df['mpg'] <= UL)]


# ------------------------------------------------------
# 1D. Remove outliers using Z-Score

z = np.abs(stats.zscore(df['mpg']))
df_zscore = df[z < 3]


# ------------------------------------------------------
# 2. Imputing standard values (Mean / Median)

df['mpg'].fillna(df['mpg'].mean(), inplace=True)
df['mpg'].fillna(df['mpg'].median(), inplace=True)


# ------------------------------------------------------
# 3. Capping of values (Winsorization)

lower_cap = df['mpg'].quantile(0.05)
upper_cap = df['mpg'].quantile(0.95)

df['mpg'] = np.where(df['mpg'] < lower_cap, lower_cap, df['mpg'])
df['mpg'] = np.where(df['mpg'] > upper_cap, upper_cap, df['mpg'])

print(df.head())
