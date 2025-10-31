import piplite
await piplite.install(['numpy'])
await piplite.install(['pandas'])
await piplite.install(['seaborn'])

# pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
#NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np
# Matplotlib is a plotting library for python and pyplot gives us a MatLab like plotting framework. We will use this in our plotter function to plot data.
import matplotlib.pyplot as plt
#Seaborn is a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics
import seaborn as sns

from js import fetch
import io

URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv"
resp = await fetch(URL)
dataset_part_2_csv = io.BytesIO((await resp.arrayBuffer()).to_py())
df=pd.read_csv(dataset_part_2_csv)
df.head(5)

sns.catplot(y="PayloadMass", x="FlightNumber", hue="Class", data=df, aspect = 5)
plt.xlabel("Flight Number",fontsize=20)
plt.ylabel("Pay load Mass (kg)",fontsize=20)
plt.show()

sns.catplot(y="LaunchSite", x="FlightNumber", hue="Class", data=df, aspect=2)
plt.xlabel("Flight Number", fontsize=12)
plt.ylabel("Launch Site", fontsize=12)
plt.show()

# Plot a scatter point chart with x axis to be Pay Load Mass (kg) and y axis to be the launch site, and hue to be the class value
sns.catplot(y="LaunchSite", x="PayloadMass", hue="Class", data=df, aspect=2)
plt.xlabel("Payload Mass (kg)", fontsize=12)
plt.ylabel("Launch Site", fontsize=12)
plt.show()

orbit_success = df.groupby('Orbit')['Class'].mean().reset_index()

plt.figure(figsize=(10,6))
sns.barplot(x='Orbit', y='Class', data=orbit_success)
plt.xlabel('Orbit Type', fontsize=12)
plt.ylabel('Success Rate', fontsize=12)
plt.title('Success Rate by Orbit Type')
plt.xticks(rotation=45)
plt.show()

sns.catplot(y="Orbit", x="FlightNumber", hue="Class", data=df, aspect=2)
plt.xlabel("Flight Number", fontsize=12)
plt.ylabel("Orbit", fontsize=12)
plt.show()

# Plot a scatter point chart with x axis to be Payload Mass and y axis to be the Orbit, and hue to be the class value
sns.catplot(y="Orbit", x="PayloadMass", hue="Class", data=df, aspect=2)
plt.xlabel("Payload Mass (kg)", fontsize=12)
plt.ylabel("Orbit", fontsize=12)
plt.show()

# A function to Extract years from the date 
year=[]
def Extract_year():
    for i in df["Date"]:
        year.append(i.split("-")[0])
    return year
Extract_year()
df['Date'] = year
df.head()
    

# Plot a line chart with x axis to be the extracted year and y axis to be the success rate
# Calculate yearly success rate
yearly_success = df.groupby('Date')['Class'].mean().reset_index()

# Plot line chart
plt.figure(figsize=(10,6))
plt.plot(yearly_success['Date'], yearly_success['Class'], marker='o', linewidth=2, markersize=8)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Success Rate', fontsize=12)
plt.title('Launch Success Rate Yearly Trend')
plt.grid(True)
plt.show()

features = df[['FlightNumber', 'PayloadMass', 'Orbit', 'LaunchSite', 'Flights', 'GridFins', 'Reused', 'Legs', 'LandingPad', 'Block', 'ReusedCount', 'Serial']]
features.head()

# HINT: Use get_dummies() function on the categorical columns
# Apply one-hot encoding to categorical columns
features_one_hot = pd.get_dummies(df, columns=['Orbit', 'LaunchSite', 'LandingPad', 'Serial'])

# Display the results
features_one_hot.head()

# Apply one-hot encoding to categorical columns
features_one_hot = pd.get_dummies(df, columns=['Orbit', 'LaunchSite', 'LandingPad', 'Serial'])

# Select only numeric columns and cast to float64
features_one_hot = features_one_hot.select_dtypes(include=['number']).astype('float64')

# Display the results
features_one_hot.head()
# Check number of unique values in each categorical column
print("Unique values in Orbit:", df['Orbit'].nunique())
print("Unique values in LaunchSite:", df['LaunchSite'].nunique()) 
print("Unique values in LandingPad:", df['LandingPad'].nunique())
print("Unique values in Serial:", df['Serial'].nunique())

# Calculate expected columns
original_columns = 12
orbit_dummies = df['Orbit'].nunique()
launchsite_dummies = df['LaunchSite'].nunique()
landingpad_dummies = df['LandingPad'].nunique()
serial_dummies = df['Serial'].nunique()

total_expected = original_columns - 4 + orbit_dummies + launchsite_dummies + landingpad_dummies + serial_dummies
print("Expected total columns:", total_expected)

