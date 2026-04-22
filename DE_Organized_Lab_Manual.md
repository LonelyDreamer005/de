# Data Engineering Lab Manual (Simple and Complete)

This manual is written in a simple format and includes all required content directly in one place.
Week 8 and Week 9 are excluded as requested.

---

## WEEK-1: Basic Data Handling Commands

```python
import pandas as pd

# 1. Read data from csv file
df = pd.read_csv("data.csv")

# 2. Dimension of the data
print("Shape:", df.shape)

# 3. Display top 5 rows and full data
print(df.head())
print(df)

# 4. List column names
print(df.columns.tolist())

# 5. Change column names (count must match)
df.columns = ["col1", "col2", "col3"]

# 6. Display single and multiple columns
print(df["col1"])
print(df[["col1", "col2"]])

# 7. Bind rows of dataframes
df1 = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
df2 = pd.DataFrame({"A": [5, 6], "B": [7, 8]})
row_bind = pd.concat([df1, df2], axis=0, ignore_index=True)
print(row_bind)

# 8. Bind columns of dataframes
col_bind = pd.concat([df1, df2], axis=1)
print(col_bind)

# 9. Find missing values
print(df.isnull().sum())
print(df[df.isnull().any(axis=1)])
```

---

## WEEK-2: Measures and Statistics

```python
import pandas as pd

s = pd.Series([10, 20, 20, 30, 40, 50])

# 1. Central tendency
print("Mean:", s.mean())
print("Median:", s.median())
print("Mode:", s.mode().tolist())

# 2. Data spread
print("Min:", s.min())
print("Max:", s.max())
print("Range:", s.max() - s.min())

# 3. Dispersion
print("Variance:", s.var())
print("Standard Deviation:", s.std())

# 4. Quartiles and IQR
q1 = s.quantile(0.25)
q2 = s.quantile(0.50)
q3 = s.quantile(0.75)
iqr = q3 - q1
print("Q1:", q1)
print("Q2:", q2)
print("Q3:", q3)
print("IQR:", iqr)
```

---

## WEEK-3: Basic Plots for Iris Dataset

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris

iris_raw = load_iris()
iris = pd.DataFrame(iris_raw.data, columns=iris_raw.feature_names)

# 1. Box plot for each predictor
iris.plot(kind="box", subplots=True, layout=(2, 2), figsize=(10, 6), sharex=False, sharey=False)
plt.tight_layout()
plt.show()

# 2. Box plot for a specific feature
sns.boxplot(y=iris["sepal length (cm)"])
plt.title("Boxplot: Sepal Length")
plt.show()

# 3. Histogram for a specific feature
plt.hist(iris["petal length (cm)"], bins=15)
plt.title("Histogram: Petal Length")
plt.xlabel("Petal Length")
plt.ylabel("Frequency")
plt.show()

# 4. Scatter plot: petal length vs sepal length
plt.scatter(iris["petal length (cm)"], iris["sepal length (cm)"])
plt.title("Petal Length vs Sepal Length")
plt.xlabel("Petal Length")
plt.ylabel("Sepal Length")
plt.show()
```

---

## WEEK-4: Data Pre-Processing (AutoMPG)

Tasks:
1. Remove outliers / missing values
2. Impute standard values
3. Cap values

```python
import pandas as pd
import numpy as np
from scipy import stats

# Load data
df = pd.read_csv("auto-mpg.csv")

# Handle missing values
df.replace("?", np.nan, inplace=True)
df["horsepower"] = pd.to_numeric(df["horsepower"], errors="coerce")
df["horsepower"] = df["horsepower"].fillna(df["horsepower"].mean())

# 1A. Outlier removal using Percentiles (for mpg)
lower_p = df["mpg"].quantile(0.05)
upper_p = df["mpg"].quantile(0.95)
df_percentile = df[(df["mpg"] >= lower_p) & (df["mpg"] <= upper_p)]

# 1B. Outlier removal using Standard Deviation
mean = df["mpg"].mean()
std = df["mpg"].std()
df_std = df[(df["mpg"] >= mean - 3 * std) & (df["mpg"] <= mean + 3 * std)]

# 1C. Outlier removal using IQR
q1 = df["mpg"].quantile(0.25)
q3 = df["mpg"].quantile(0.75)
iqr = q3 - q1
ll = q1 - 1.5 * iqr
ul = q3 + 1.5 * iqr
df_iqr = df[(df["mpg"] >= ll) & (df["mpg"] <= ul)]

# 1D. Outlier removal using Z-score
z = np.abs(stats.zscore(df["mpg"], nan_policy="omit"))
df_zscore = df[z < 3]

# 2. Impute standard values (mean and median example)
df["mpg"] = df["mpg"].fillna(df["mpg"].mean())
df["mpg"] = df["mpg"].fillna(df["mpg"].median())

# 3. Capping values (winsorization style)
lower_cap = df["mpg"].quantile(0.05)
upper_cap = df["mpg"].quantile(0.95)
df["mpg"] = np.where(df["mpg"] < lower_cap, lower_cap, df["mpg"])
df["mpg"] = np.where(df["mpg"] > upper_cap, upper_cap, df["mpg"])

print(df.head())
```

---

## WEEK-5: Feature Construction

Tasks:
1. Dummy coding categorical (nominal) variables
2. Encoding categorical (ordinal) variables
3. Transform numeric to categorical

```python
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Sample data
df = pd.DataFrame({
    "town": ["new york", "west windsor", "new york", "robinsville"],
    "size": ["small", "medium", "large", "medium"],
    "price": [250000, 550000, 700000, 400000]
})

# 1. Dummy coding for nominal variable: town
dummies = pd.get_dummies(df["town"], prefix="town")
df_dummy = pd.concat([df.drop(columns=["town"]), dummies], axis=1)

# 2A. Ordinal encoding using custom mapping
size_map = {"small": 1, "medium": 2, "large": 3}
df_dummy["size_encoded"] = df_dummy["size"].map(size_map)

# 2B. LabelEncoder example (usually for labels, not true ordinal meaning)
le = LabelEncoder()
df_dummy["size_label"] = le.fit_transform(df_dummy["size"])

# 3. Continuous to categorical
bins = [0, 300000, 600000, 1000000]
labels = ["Low", "Medium", "High"]
df_dummy["price_category"] = pd.cut(df_dummy["price"], bins=bins, labels=labels)

print(df_dummy)
```

---

## WEEK-6: Feature Extraction

Tasks:
1. PCA
2. SVD
3. LDA
4. Feature subset selection

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.feature_selection import SelectKBest, f_classif

# Load Iris data
iris = load_iris()
X = iris.data
y = iris.target

# 1. PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y)
plt.title("PCA")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.show()

# 2. SVD
U, S, Vt = np.linalg.svd(X, full_matrices=False)
plt.scatter(U[:, 0], U[:, 1], c=y)
plt.title("SVD")
plt.xlabel("Component 1")
plt.ylabel("Component 2")
plt.show()

# 3. LDA
lda = LinearDiscriminantAnalysis(n_components=2)
X_lda = lda.fit(X, y).transform(X)
plt.scatter(X_lda[:, 0], X_lda[:, 1], c=y)
plt.title("LDA")
plt.xlabel("LD1")
plt.ylabel("LD2")
plt.show()

# 4. Feature subset selection
selector = SelectKBest(score_func=f_classif, k=2)
X_selected = selector.fit_transform(X, y)
selected_indices = selector.get_support(indices=True)
print("Selected feature indices:", selected_indices)
print("Selected feature names:", [iris.feature_names[i] for i in selected_indices])
```

---

## WEEK-7: HDFS (Storage)

### A. Create directory structure in HDFS

```bash
hdfs dfs -mkdir /hadooplab
hdfs dfs -mkdir /hadooplab/input
```

### B. Create local file and move to HDFS

```bash
echo "sample text for hdfs" > sample.txt
hdfs dfs -put sample.txt /hadooplab/input
```

### C. View files and file contents in HDFS

```bash
hdfs dfs -ls /hadooplab/input
hdfs dfs -cat /hadooplab/input/sample.txt
```

### D. Copy file from HDFS to local disk

```bash
hdfs dfs -copyToLocal /hadooplab/input/sample.txt ./sample_from_hdfs.txt
```

### Lab objective
Move data from local system to HDFS before processing.

---

## WEEK-8 & WEEK-9: Excluded

MapReduce section intentionally omitted as requested.

---

## WEEK-10 & WEEK-11: Hive

Problem:
- Table name: user_data
- Fields: data_date, user_id, properties
- properties format example: Age=21;state=CA;gender=M;

### 1. Create table

```sql
CREATE TABLE IF NOT EXISTS user_data (
  data_date STRING,
  user_id STRING,
  properties STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;
```

### 2. Load sample data

```sql
LOAD DATA INPATH '/hadooplab/input/user_data.csv' INTO TABLE user_data;
```

### 3. List each property with min, max, unique count

```sql
WITH kv AS (
  SELECT
    regexp_extract(prop, '([^=]+)', 1) AS property_name,
    regexp_extract(prop, '=(.*)', 1) AS property_value
  FROM user_data
  LATERAL VIEW explode(split(properties, ';')) s AS prop
  WHERE prop <> ''
)
SELECT
  property_name,
  MIN(property_value) AS min_value,
  MAX(property_value) AS max_value,
  COUNT(DISTINCT property_value) AS unique_values
FROM kv
GROUP BY property_name;
```

### 4. Generate count per state

```sql
WITH states AS (
  SELECT regexp_extract(prop, 'state=([^;]+)', 1) AS state
  FROM user_data
  LATERAL VIEW explode(split(properties, ';')) s AS prop
  WHERE prop LIKE 'state=%'
)
SELECT state, COUNT(*) AS state_count
FROM states
GROUP BY state
ORDER BY state_count DESC;
```

### 5. Number of records per state

```sql
SELECT
  regexp_extract(properties, 'state=([^;]+)', 1) AS state,
  COUNT(*) AS records_per_state
FROM user_data
GROUP BY regexp_extract(properties, 'state=([^;]+)', 1)
ORDER BY records_per_state DESC;
```

---

## WEEK-12 & WEEK-13: MongoDB

Tasks:
1. Create database and run basic commands
2. Explore data types
3. Insert sample data and query with MQL

### Common MongoDB data types
- String
- Number (int, long, double, decimal)
- Boolean
- Date
- Array
- Object (embedded document)
- Null
- ObjectId

### Commands

```javascript
// Create/switch database
use de_lab

// Insert one document
db.students.insertOne({
  name: "Vinay",
  age: 21,
  active: true,
  joinedOn: new Date(),
  skills: ["python", "hadoop"],
  address: {city: "Hyderabad", pin: 500001}
})

// Insert many documents
db.students.insertMany([
  {name: "Sagar", age: 22, state: "TS"},
  {name: "Vedh", age: 21, state: "AP"},
  {name: "Nina", age: 23, state: "TS"}
])

// Read
db.students.find()
db.students.find().pretty()

// Filter
db.students.find({age: 21})
db.students.find({age: {$gt: 21}})
db.students.find({state: {$in: ["TS", "AP"]}})
db.students.find({name: {$regex: "^V"}})

// Projection
db.students.find({}, {name: 1, age: 1, _id: 0})

// Sort, limit, skip
db.students.find().sort({age: 1})
db.students.find().sort({age: -1}).limit(2)
db.students.find().skip(1)

// Update
db.students.updateOne({name: "Vinay"}, {$set: {age: 22}})
db.students.updateMany({state: "TS"}, {$inc: {age: 1}})
db.students.updateOne({name: "Ravi"}, {$set: {age: 24, state: "KA"}}, {upsert: true})

// Delete
db.students.deleteOne({name: "Vinay"})
db.students.deleteMany({age: {$gte: 30}})

// Count
db.students.countDocuments()

// Drop
db.students.drop()
db.dropDatabase()
```

---

## Quick Checklist

1. Install Python packages: pandas, numpy, scipy, scikit-learn, matplotlib, seaborn.
2. Keep datasets in correct path (or use full file path).
3. Start Hadoop and HDFS services before Week-7 and Hive tasks.
4. Start MongoDB service before Week-12 and Week-13 tasks.
