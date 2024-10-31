# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the dataset
dataset = pd.read_csv("msleep.csv")

# Select columns 6 to 10 and handle missing values with mean imputation
subset = dataset.iloc[:, 6:11].values
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(missing_values=np.nan, strategy="mean")
imputer.fit(subset)
subset = imputer.transform(subset)
dataset.iloc[:, 6:11] = subset

# Define features (X) and target (y) variables
X = dataset.iloc[:, 6:11]
y = dataset.iloc[:, 5]

# Split data into training and testing sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a linear regression model
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# Make predictions on the test set
y_pred = regressor.predict(X_test)

# Create a DataFrame to analyze prediction errors
test_results = pd.DataFrame({
    "Animal_Species": dataset.iloc[X_test.index]["name"],
    "Actual_Sleep_Total": y_test.values,
    "Predicted_Sleep_Total": y_pred,
    "Error": abs(y_test.values - y_pred)
})

# Calculate average error by species
avg_error_by_species = test_results.groupby("Animal_Species")["Error"].mean().reset_index()

# Plot average error distribution by species
plt.figure(figsize=(15, 8))
plt.bar(avg_error_by_species["Animal_Species"], avg_error_by_species["Error"])
plt.title("Average Error Distribution by Animal Species (Test)")
plt.xlabel("Animal Species")
plt.ylabel("Average Error")
plt.xticks(rotation=90)
plt.show()
