# Q6:
# Implement Feature Extraction using:
# 1. PCA (Principal Component Analysis)
# 2. LDA (Linear Discriminant Analysis)
# 3. SVD (Singular Value Decomposition)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

# Load dataset
iris = datasets.load_iris()
X = iris.data
y = iris.target


# ------------------------------------------------------
# 1. PCA (Principal Component Analysis)

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

plt.scatter(X_pca[:,0], X_pca[:,1], c=y)
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title("PCA")
plt.show()


# ------------------------------------------------------
# 2. LDA (Linear Discriminant Analysis)

lda = LinearDiscriminantAnalysis(n_components=2)
X_lda = lda.fit(X, y).transform(X)

plt.scatter(X_lda[:,0], X_lda[:,1], c=y)
plt.xlabel("LD1")
plt.ylabel("LD2")
plt.title("LDA")
plt.show()


# ------------------------------------------------------
# 3. SVD (Singular Value Decomposition)

df = pd.DataFrame(X)

U, S, Vt = np.linalg.svd(df, full_matrices=False)

# Plot first two components
plt.scatter(U[:,0], U[:,1], c=y)
plt.xlabel("Component 1")
plt.ylabel("Component 2")
plt.title("SVD")
plt.show()


# 4. Feature subset selection

import pandas as pd
from sklearn.datasets import load_iris

df = pd.DataFrame(load_iris().data)

print(df.corr())
# for correlation matrix, use below code. 
import seaborn as sns
import matplotlib.pyplot as plt
sns.heatmap(df.corr(method='pearson'),annot=True)
plt.show()
