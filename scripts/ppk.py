import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

# 1. LIST YOUR 3 EXCEL FILES
files_to_process = ["Fluorescein.xlsx", "Rho6G.xlsx", "RhoB.xlsx"]
pd.options.display.precision = 15
poly_degree = 4  # Degree for the polynomial fit

for file_name in files_to_process:
    if not os.path.exists(file_name):
        print(f"Skipping {file_name}: File not found.")
        continue

    print(f"\n>>> Processing Material: {file_name}")
    xls = pd.ExcelFile(file_name, engine='openpyxl')
    file_results = []

    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet)
        df = df.dropna(how='all').reset_index(drop=True)

        if df.shape[1] == 1:
            df_split = df.iloc[:, 0].astype(str).str.split(';', expand=True)
            if df_split.shape[1] >= 2:
                df = df_split
            else:
                continue

        # Clean and convert Wavelength/Intensity to numbers
        wave = pd.to_numeric(df.iloc[:, 0].astype(str).str.replace(',', '.'), errors='coerce')
        intensity = pd.to_numeric(df.iloc[:, 1].astype(str).str.replace(',', '.'), errors='coerce')

        valid_mask = wave.notna() & intensity.notna()
        wave, intensity = wave[valid_mask], intensity[valid_mask]

        if len(wave) < 2:
            continue

        # Calculate Integration (450-460nm)
        mask_range = (wave >= 450) & (wave <= 460)
        sub_wave, sub_int = wave[mask_range], intensity[mask_range]

        if len(sub_wave) > 1:
            func = getattr(np, 'trapezoid', getattr(np, 'trapz', None))
            integral_val = func(sub_int, x=sub_wave)
        else:
            integral_val = 0.0

        file_results.append({
            "Concentration_Label": sheet,
            "Integrated_Intensity": integral_val
        })

    # --- Create the Summary Table ---
    df_summary = pd.DataFrame(file_results)
    df_summary['Conc_Numeric'] = df_summary['Concentration_Label'].replace('e-4', '1e-4')
    df_summary['Conc_Numeric'] = pd.to_numeric(df_summary['Conc_Numeric'], errors='coerce')
    df_summary = df_summary.dropna(subset=['Conc_Numeric', 'Integrated_Intensity']).sort_values(by='Conc_Numeric')

    material_name = file_name.split('.')[0]
    x = df_summary['Conc_Numeric'].values
    y = df_summary['Integrated_Intensity'].values

    # --- A. LINEAR FIT AND PLOT ---
    slope, intercept = np.polyfit(x, y, 1)
    y_fit_lin = slope * x + intercept
    res_lin = y - y_fit_lin

    fig_lin, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True, gridspec_kw={'height_ratios': [3, 1]})
    ax1.scatter(x, y, color='darkblue', s=25, label='Data')
    ax1.plot(x, y_fit_lin, color='red', linewidth=2, label=f'Linear: y={slope:.2e}x + {intercept:.2e}')
    ax1.set_title(f"Linear Fit - {material_name}", fontsize=14)
    ax1.set_ylabel("Integrated Intensity")
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.6)

    ax2.scatter(x, res_lin, color='darkblue', s=25)
    ax2.axhline(0, color='red', linestyle='--')
    ax2.set_xlabel("Concentration [mM]")
    ax2.set_ylabel("Residuals")
    ax2.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.savefig(f"Linear_Fit_{material_name}.png")
    plt.close()

    # --- B. POLYNOMIAL FIT AND PLOT ---
    coeffs = np.polyfit(x, y, poly_degree)
    poly_func = np.poly1d(coeffs)

    # Smooth line for plotting
    x_smooth = np.linspace(x.min(), x.max(), 200)
    y_fit_poly_smooth = poly_func(x_smooth)

    # Values at data points for residuals
    y_fit_poly_points = poly_func(x)
    res_poly = y - y_fit_poly_points

    fig_poly, (ax3, ax4) = plt.subplots(2, 1, figsize=(10, 8), sharex=True, gridspec_kw={'height_ratios': [3, 1]})
    ax3.scatter(x, y, color='darkblue', s=25, label='Data')
    ax3.plot(x_smooth, y_fit_poly_smooth, color='red', linewidth=2, label=f'Polynomial (deg={poly_degree})')
    ax3.set_title(f"Polynomial Fit (Degree {poly_degree}) - {material_name}", fontsize=14)
    ax3.set_ylabel("Integrated Intensity")
    ax3.legend()
    ax3.grid(True, linestyle='--', alpha=0.6)

    ax4.scatter(x, res_poly, color='darkblue', s=25)
    ax4.axhline(0, color='red', linestyle='--')
    ax4.set_xlabel("Concentration [mM]")
    ax4.set_ylabel("Residuals")
    ax4.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.savefig(f"Polynomial_Fit_{material_name}.png")
    plt.close()

    # --- SAVE CSV DATA ---
    df_summary['Linear_Resid'] = res_lin
    df_summary['Poly_Resid'] = res_poly
    df_summary.to_csv(f"Final_Results_{material_name}.csv", index=False)

    print(f"Plots saved for {material_name}.")