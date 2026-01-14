#!/usr/bin/env python
# coding: utf-8

# In[92]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import re  # Added for finding the number correctly

# --- 1. PASTE YOUR PATH HERE ---
csv_path = r"C:\Users\ASUS\Desktop\fluorescence\b\graphs and data from matlab\e-4_results.csv"

# --- 2. SET THE SAVE LOCATION ---
save_folder = r'C:\Users\ASUS\Desktop\fluorescence\b\graphs and data from matlab\linear fit'

if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# --- 3. EXTRACT THE CONCENTRATION NUMBER USING REGEX ---
file_base = os.path.basename(csv_path)

# This finds any number (including decimals) in the filename
match = re.search(r"(\d+\.\d+|\d+)", file_base)
if match:
    concentration = match.group(0)
else:
    concentration = "Unknown" # Fallback if no number is found

# --- 4. LOAD AND PROCESS ---
df = pd.read_csv(csv_path)
x = df['Distance_cm'].values
y_raw = df['Intensity'].values

y_log = np.log(y_raw + 1e-6) 
slope, intercept = np.polyfit(x, y_log, 1)
y_fit = slope * x + intercept
residuals = y_log - y_fit

# --- 5. PLOTTING ---
plt.figure(figsize=(10, 8))

# Top Plot
ax1 = plt.subplot(2, 1, 1)
ax1.scatter(x, y_log, color='darkblue', s=6, label='Data (Log Intensity)')
ax1.plot(x, y_fit, color='red', linewidth=2, label=f'Linear Fit: y = {slope:.4f}x + {intercept:.4f}')
ax1.set_ylabel('Intensity [Log AU]', fontsize = 14)

# The title you requested
ax1.set_title(f'Linear fit and Residuals - Intensity over Distance for Fluorescein in a concentration of {concentration}', fontsize = 16)

ax1.legend()
ax1.grid(True, linestyle='--', alpha=0.6)

# Bottom Plot (Residuals)
ax2 = plt.subplot(2, 1, 2, sharex=ax1)
ax2.scatter(x, residuals, color='darkblue', s=6, label='Residuals')
ax2.axhline(0, color='red', linestyle='--')
ax2.set_xlabel('Distance [cm]', fontsize = 14)
ax2.set_ylabel('Residuals', fontsize = 14)
ax2.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()

# --- 6. SAVE WITH NEW NAME ---
save_filename = f'Linear_fit_{concentration}.png'
save_path = os.path.join(save_folder, save_filename)
plt.savefig(save_path)

print(f"Graph for concentration {concentration} saved successfully!")
plt.show()


# In[ ]:





# In[ ]:




