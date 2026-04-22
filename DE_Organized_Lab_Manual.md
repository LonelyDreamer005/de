# Data Engineering Lab Manual (Organized)

This document organizes the DE folder content into a single week-wise guide.

## Folder Audit (Current Files)

| File | Purpose / Content |
|---|---|
| `DE_Revise.ipynb` | Consolidated notebook with multiple DE practice cells (data handling, stats, plotting, preprocessing, etc.). |
| `dummy.py` | Week-5 style feature construction: dummy coding, label encoding, binning. |
| `wk4.py` | Week-4 preprocessing on AutoMPG: missing values, outlier treatment, capping. |
| `pca.py` | Week-6 feature extraction: PCA, LDA, SVD, feature subset inspection. |
| `hdfs.txt` | Week-7 HDFS command notes and sample workflow. |
| `mongodb.txt` | Week-12/13 MongoDB command notes and examples. |
| `README.md` | External links and resources. |

---

## WEEK-1: Basic Data Handling Commands

Use Pandas for all tasks.

```python
import pandas as pd

# 1. Read data from csv file
df = pd.read_csv("data.csv")

# 2. Dimension of the data
print("Rows, Columns:", df.shape)

# 3. Display data (top 5 rows and total data)
print(df.head(5))
print(df)

# 4. List the column names
print(df.columns.tolist())

# 5. Change columns of a data frame
df.columns = ["col1", "col2", "col3"]  # same number as original columns

# 6. Display specific single or multiple columns
print(df["col1"])               # single column
print(df[["col1", "col2"]])   # multiple columns

# 7. Bind sets of rows of dataframes (row-wise)
df1 = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
df2 = pd.DataFrame({"A": [5, 6], "B": [7, 8]})
row_bind = pd.concat([df1, df2], axis=0, ignore_index=True)

# 8. Bind sets of columns of dataframes (column-wise)
col_bind = pd.concat([df1, df2], axis=1)

# 9. Find missing values in dataset
print(df.isnull().sum())
print(df[df.isnull().any(axis=1)])
```

---

## WEEK-2: Descriptive Statistics

```python
import pandas as pd

s = pd.Series([10, 20, 20, 30, 40, 50])

# 1. Measures of central tendency
print("Mean:", s.mean())
print("Median:", s.median())
print("Mode:", s.mode().tolist())

# 2. Measures of data spread
print("Min:", s.min())
print("Max:", s.max())
print("Range:", s.max() - s.min())

# 3. Dispersion: variance and standard deviation
print("Variance:", s.var())
print("Standard Deviation:", s.std())

# 4. Position: quartiles and IQR
q1 = s.quantile(0.25)
q2 = s.quantile(0.50)
q3 = s.quantile(0.75)
iqr = q3 - q1
print("Q1:", q1, "Q2:", q2, "Q3:", q3, "IQR:", iqr)
```

---

## WEEK-3: Basic Plots for Data Exploration (Iris Dataset)

```python
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
import pandas as pd

iris_raw = load_iris()
iris = pd.DataFrame(iris_raw.data, columns=iris_raw.feature_names)

# 1. Box plot for each of four predictors
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

Reference implementation exists in `wk4.py`.

Tasks covered:
1. Removing outliers / missing values
2. Imputing standard values
3. Capping values

Suggested execution order:
1. Load AutoMPG data
2. Replace placeholder missing values (`?`) with NaN
3. Convert numeric columns correctly
4. Impute missing values (mean/median)
5. Apply outlier handling (Percentile / Std Dev / IQR / Z-Score)
6. Cap extreme values using quantiles

---

## WEEK-5: Feature Construction

Reference implementation exists in `dummy.py`.

Tasks covered:
1. Dummy coding categorical (nominal) variables
2. Encoding categorical (ordinal) variables
3. Transforming numeric (continuous) to categorical features

Notes:
- Use `pd.get_dummies` for nominal columns.
- Use `LabelEncoder` or custom mappings for ordinal columns.
- Use `pd.cut` / `pd.qcut` for continuous-to-categorical conversion.

---

## WEEK-6: Feature Extraction

Reference implementation exists in `pca.py`.

Tasks covered:
1. PCA
2. SVD
3. LDA
4. Feature subset selection

Recommended package set:
- numpy
- pandas
- scikit-learn
- matplotlib
- seaborn

---

## WEEK-7: HDFS (Storage)

Reference command set exists in `hdfs.txt`.

### A. Hadoop Storage File System

1. Create directory structure in HDFS

```bash
hdfs dfs -mkdir /hadooplab
hdfs dfs -mkdir /hadooplab/input
```

2. Create local files and move to HDFS

```bash
echo "sample data" > sample.txt
hdfs dfs -put sample.txt /hadooplab/input
```

### B. View data, files, and directories

1. See files in HDFS directory

```bash
hdfs dfs -ls /hadooplab/input
```

2. View file contents in HDFS

```bash
hdfs dfs -cat /hadooplab/input/sample.txt
```

### C. Copy file from HDFS to local disk

```bash
hdfs dfs -copyToLocal /hadooplab/input/sample.txt ./sample_from_hdfs.txt
```

Lab objective:
- Move data from local to HDFS before processing.

---

## WEEK-8 & WEEK-9: Excluded

As requested, MapReduce week content is intentionally omitted.

---

## WEEK-10 & WEEK-11: Hive (NoSQL Query Language for Big Data)

Problem statement:
- Table: `user_data`
- Columns:
  - `data_date` string
  - `user_id` string
  - `properties` string
- Sample `properties` format:
  - `Age=21;state=CA;gender=M;`

### 1. Create table in Hive

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

### 3. Extract each property and compute min, max, unique-count

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

### 4. Generate a count per state

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

### 5. Number of records per state (alternate explicit extraction)

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

Reference command set exists in `mongodb.txt`.

### Core tasks
1. Create and switch database
2. Insert single and multiple documents
3. Query documents using filters
4. Update and upsert documents
5. Delete documents
6. Sort, limit, skip, project fields
7. Count documents
8. Drop collection and database

### Sample command flow

```javascript
use vin

db.students.insertOne({name: "vinay", age: 21})
db.students.insertMany([
  {name: "sagar", age: 22},
  {name: "vedh", age: 21}
])

db.students.find().pretty()
db.students.find({age: {$gt: 21}})

db.students.updateOne({name: "vinay"}, {$set: {age: 22}})
db.students.updateMany({age: 21}, {$inc: {age: 1}})

db.students.find().sort({age: -1}).limit(2)

db.students.countDocuments()

db.students.drop()
db.dropDatabase()
```

---

## Quick Run Checklist

1. Keep datasets in project root or set full paths explicitly.
2. Install required Python packages before running scripts.
3. Validate schema and missing values before preprocessing.
4. For Hive and HDFS labs, ensure Hadoop services are running.
5. For MongoDB labs, ensure `mongod` service is active.

---

## Where Existing Week Files Are Located

- Week-4: `wk4.py`
- Week-5: `dummy.py`
- Week-6: `pca.py`
- Week-7: `hdfs.txt`
- Week-12/13: `mongodb.txt`
