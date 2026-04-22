# Q4:
# Implement Feature Construction (homeprices dataset)
# 1. Dummy coding categorical (nominal) variables
# 2. Encoding categorical (ordinal) variables
# 3. Transform numeric (continuous) features to categorical

import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv("homeprices.csv")

# ------------------------------------------------------
# 1. Dummy coding (Nominal variables)

# Create dummy variables
dummies = pd.get_dummies(df['town'])

# Drop one column to avoid dummy variable trap
dummies = dummies.drop(['west windsor'], axis=1)

# Merge with original dataset
df = pd.concat([df, dummies], axis=1)

# Drop original column
df = df.drop(['town'], axis=1)


# ------------------------------------------------------
# 2. Encoding categorical (Ordinal variables)

# Example: encode a categorical column
le = LabelEncoder()
df['town_encoded'] = le.fit_transform(df['town'])


# ------------------------------------------------------
# 3. Convert numeric (continuous) to categorical

# Convert price into categories
df['price_category'] = pd.cut(
    df['price'],
    bins=[0, 300000, 600000, 1000000],
    labels=['Low', 'Medium', 'High']
)

print(df)
