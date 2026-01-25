# Fluorescence Experiment - Physics Lab C

## Overview
This repository contains the data analysis, visualization, and source code for the Fluorescence experiment conducted as part of the Advanced Physics Laboratory C. 

This project investigates the limits of the Beer-Lambert law in high-concentration molecular systems. While standard theory predicts a linear relationship between concentration and fluorescence, this study uses spectral and spatial analysis to quantify how inter-molecular interactions cause significant deviations from this ideal behavior.

The research focuses on three primary fluorophores: Fluorescein, Rhodamine B, and Rhodamine 6G. Experimental MethodologyThe experiment was divided into two distinct analytical phases:

  1. Phase A: Spectral Characterization – Measurement of total integrated emission intensity across concentrations ranging from $10^{-4}$ M to $10^{-1}$ M using a fiber-optic spectrometer assembly.
  2. Phase B: Spatial Attenuation Mapping – Digital imaging of the fluorescence "track" in a 10 cm cuvette to observe the non-uniform distribution of excited states along the path length.

## Project Structure
* [scripts/](scripts/): Contains the core analysis code.
* [data/](data/): Raw `.csv` files.
* [output/](output/): Final high-resolution graphs.
* [report/](report/): https://www.overleaf.com/read/ytwpfnbtzgqh#6df9f4.

## Requirements
To run the scripts, you will need:
* Python 3.x
* MATLAB
* NumPy, pandas, Matplotlib, os and re 

## How to Use
1. Clone the repository.
2. Run `scripts/fit_lifetime.py` to process raw decay data.
