import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import linregress
import numpy as np

# Load data from CSV file
data = pd.read_csv("hysteresis_data.csv")

# Extract H and B values from the data
H = data['H']
B = data['B']

# Determine the maximum absolute values of H and B for setting axis limits
max_value_x = max(max(H), abs(min(H)))
max_value_y = max(max(B), abs(min(B)))

# Determine slope in order to find the paramagnetic component
slope, intercept, r_value, p_value, std_err = linregress(H, B)
h = H - H.mean()
b = B - B.mean()
slope1 = (h.dot(h))/(b.dot(b))
print(slope1)
# Create the hysteresis plot
plt.figure(figsize=(8, 6))
plt.plot(H, B, marker='o', linestyle='-', color='blue', label='Hysteresis Loop')
plt.plot(H, slope1 * H + intercept, color='red', label='Linear Fit')
plt.xlabel('Magnetic Field Strength (H)')
plt.ylabel('Magnetic Induction (B)')

# Set axis limits to ensure they go through (0, 0)
plt.xlim(-max_value_x, max_value_x)
plt.ylim(-max_value_y, max_value_y)


plt.title('Hysteresis Loop with Linear Fit')
plt.grid()
plt.legend()
plt.show()

# Calculate the predicted values based on the linear fit
predicted_B = slope * H + intercept

# Remove the linear trend by subtracting the predicted values
detrended_B = B - predicted_B

plt.figure(figsize=(8, 6))
plt.plot(H, detrended_B, marker='o', linestyle='-', color='blue', label='Detrended Data')
plt.xlabel('Magnetic Field Strength (H)')
plt.ylabel('Detrended Magnetic Induction (B)')


plt.title('Detrended Hysteresis Loop')
plt.grid()
plt.legend()
plt.show()

