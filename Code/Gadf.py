import matplotlib.pyplot as plt
from pyts.image import GramianAngularField
import pandas as pd

# Load the CSV file into a pandas dataframe
df = pd.read_csv('2000-03-06_1_day_1.csv', parse_dates=['Date'])

# Get the values from the dataframe
X = df.iloc[:, 1:].values.T

# Compute Gramian angular fields
gasf = GramianAngularField(method='summation')
X_gasf = gasf.fit_transform(X)

gadf = GramianAngularField(method='difference')
X_gadf = gadf.fit_transform(X)

# Plot the Gramian angular fields
fig, ax = plt.subplots(ncols=2, figsize=(12, 6))
ax[0].imshow(X_gasf[0], cmap='rainbow', origin='lower')
#ax[1].imshow(X_gadf[0], cmap='rainbow', origin='lower')
plt.show()

'''
fig.savefig('2000-03-06_1_day_1_GAF.png', dpi=300, bbox_inches='tight')

# Load the CSV file into a pandas dataframe
df = pd.read_csv('2000-03-06_1_day_2.csv', parse_dates=['Date'])

# Get the values from the dataframe
X = df.iloc[:, 1:].values.T

# Compute Gramian angular fields
gasf = GramianAngularField(method='summation')
X_gasf = gasf.fit_transform(X)

gadf = GramianAngularField(method='difference')
X_gadf = gadf.fit_transform(X)

# Plot the Gramian angular fields
fig, ax = plt.subplots(ncols=2, figsize=(12, 6))
ax[0].imshow(X_gasf[0], cmap='rainbow', origin='lower')
ax[0].set_title('Gramian Angular Summation Field')
ax[1].imshow(X_gadf[0], cmap='rainbow', origin='lower')
ax[1].set_title('Gramian Angular Difference Field')
plt.show()

fig.savefig('2000-03-06_1_day_2_GAF.png', dpi=300, bbox_inches='tight')

# Load the CSV file into a pandas dataframe
df = pd.read_csv('2000-03-06_1_day_4.csv', parse_dates=['Date'])

# Get the values from the dataframe
X = df.iloc[:, 1:].values.T

# Compute Gramian angular fields
gasf = GramianAngularField(method='summation')
X_gasf = gasf.fit_transform(X)

gadf = GramianAngularField(method='difference')
X_gadf = gadf.fit_transform(X)

# Plot the Gramian angular fields
fig, ax = plt.subplots(ncols=2, figsize=(12, 6))
ax[0].imshow(X_gasf[0], cmap='rainbow', origin='lower')
ax[0].set_title('Gramian Angular Summation Field')
ax[1].imshow(X_gadf[0], cmap='rainbow', origin='lower')
ax[1].set_title('Gramian Angular Difference Field')
plt.show()

fig.savefig('2000-03-06_1_day_4_GAF.png', dpi=300, bbox_inches='tight')

# Load the CSV file into a pandas dataframe
df = pd.read_csv('2000-03-06_1_day_5.csv', parse_dates=['Date'])

# Get the values from the dataframe
X = df.iloc[:, 1:].values.T

# Compute Gramian angular fields
gasf = GramianAngularField(method='summation')
X_gasf = gasf.fit_transform(X)

gadf = GramianAngularField(method='difference')
X_gadf = gadf.fit_transform(X)

# Plot the Gramian angular fields
fig, ax = plt.subplots(ncols=2, figsize=(12, 6))
ax[0].imshow(X_gasf[0], cmap='rainbow', origin='lower')
ax[0].set_title('Gramian Angular Summation Field')
ax[1].imshow(X_gadf[0], cmap='rainbow', origin='lower')
ax[1].set_title('Gramian Angular Difference Field')
plt.show()

fig.savefig('2000-03-06_1_day_5_GAF.png', dpi=300, bbox_inches='tight')
'''