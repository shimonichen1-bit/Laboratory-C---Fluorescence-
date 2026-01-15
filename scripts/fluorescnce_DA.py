#!/usr/bin/env python
# coding: utf-8

# In[336]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import re  # Added for finding the number correctly

#settings:
csv_path = r"C:\Users\ASUS\Desktop\fluorescence\partB\data\data_rhod_b\b_0.001_results.csv"
save_folder = r"C:\Users\ASUS\Desktop\fluorescence\partB\output\linear_output_rhod_b"

if not os.path.exists(save_folder):
    os.makedirs(save_folder)

#cons extract:
file_base = os.path.basename(csv_path)

#naming using file name:
match = re.search(r"(\d+\.\d+|\d+)", file_base)
if match:
    concentration = match.group(0)
else:
    concentration = "Unknown" # Fallback if no number is found
#concentration = 8e-4

#data loading:
df = pd.read_csv(csv_path)
x = df['Distance_cm'].values
y_raw = df['Intensity'].values

#log scale:
y_log = np.log(y_raw + 1e-6) 
slope, intercept = np.polyfit(x, y_log, 1)
y_fit = slope * x + intercept
residuals = y_log - y_fit

plt.figure(figsize=(10, 8))

#linear plot:
ax1 = plt.subplot(2, 1, 1)
ax1.scatter(x, y_log, color='darkblue', s=6, label='Data (Log Intensity)')
ax1.plot(x, y_fit, color='red', linewidth=2, label=f'Linear Fit: y = {slope:.4f}x + {intercept:.4f}')
ax1.set_ylabel('Intensity [Log AU]', fontsize = 14)

#title:
ax1.set_title(f'Linear fit and Residuals - \nIntensity over Distance (Rhodamine b,concentration: {concentration})', fontsize = 16)
ax1.legend()
ax1.grid(True, linestyle='--', alpha=0.6)

#residuals plot:
ax2 = plt.subplot(2, 1, 2, sharex=ax1)
ax2.scatter(x, residuals, color='darkblue', s=6, label='Residuals')
ax2.axhline(0, color='red', linestyle='--')
ax2.set_xlabel('Distance [cm]', fontsize = 14)
ax2.set_ylabel('Residuals', fontsize = 14)
ax2.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()

#saving:
save_filename = f'Linear_fit_{concentration}.png'
save_path = os.path.join(save_folder, save_filename)
plt.savefig(save_path)

print(f"Graph for concentration {concentration} saved successfully!")
plt.show()


# In[337]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import re 

#settings:
csv_path = r"C:\Users\ASUS\Desktop\fluorescence\partB\data\data_rhod_b\b_0.001_results.csv"
save_folder = r"C:\Users\ASUS\Desktop\fluorescence\partB\output\poly_rhod_b"
degree = 5

if not os.path.exists(save_folder):
    os.makedirs(save_folder)

#cons extract:
file_base = os.path.basename(csv_path)
match = re.search(r"(\d+\.\d+|\d+)", file_base)
concentration = match.group(0) if match else "Unknown"
#concentration = 8e-4

#data loading:
df = pd.read_csv(csv_path)
x = df['Distance_cm'].values
y_raw = df['Intensity'].values

#log scale:
y_log = np.log(y_raw + 1e-6) 

#poly fit:
coeffs = np.polyfit(x, y_log, degree)
poly_func = np.poly1d(coeffs) # Creates a function from coefficients
y_fit = poly_func(x)

residuals = y_log - y_fit

plt.figure(figsize=(10, 8))

#poly plot:
ax1 = plt.subplot(2, 1, 1)
ax1.scatter(x, y_log, color='darkblue', s=6, label='Data (Log Intensity)')
ax1.plot(x, y_fit, color='red', linewidth=2, label=f'Polynomial Fit (deg={degree})')
ax1.set_ylabel('Intensity [Log AU]', fontsize=14)
ax1.set_title(f'Polynomial Fit and Residuals - \nIntensity over Distance (Rhodamine b,concentration: {concentration})', fontsize=16)
ax1.legend()
ax1.grid(True, linestyle='--', alpha=0.6)

#residuals plot:
ax2 = plt.subplot(2, 1, 2, sharex=ax1)
ax2.scatter(x, residuals, color='darkblue', s=6, label='Residuals')
ax2.axhline(0, color='red', linestyle='--')
ax2.set_xlabel('Distance [cm]', fontsize=14)
ax2.set_ylabel('Residuals', fontsize=14)
ax2.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()

#saving:
save_filename = f'Polynomial_fit_deg{degree}_{concentration}.png'
save_path = os.path.join(save_folder, save_filename)
plt.savefig(save_path)

print(f"Polynomial (degree {degree}) graph for concentration {concentration} saved!")
plt.show()


# In[ ]:




