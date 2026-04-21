# TAST Calculator

A web-based calculator for estimating the **TAST score** from **AST** and **TSI** inputs.

## Overview

This application provides a simple interface for entering a patient’s AST value and TSI score, then computing the predicted TAST score using a locked ensemble machine learning model. The interface is designed for convenient browser-based use and is deployed through Streamlit.

## Features

- Input fields for **AST** and **TSI**
- Increment and decrement controls for quick value adjustment
- Automatic prediction of **TAST score**
- Clinical interpretation guide with threshold ranges:
  - **TAST ≤ 0.35**: Likely non-MASH
  - **0.35 < TAST < 0.67**: Intermediate zone
  - **TAST ≥ 0.67**: Likely MASH
- Clean browser-based interface without requiring local Python installation for end users

## Model

The calculator uses a pre-trained locked ensemble model stored in `model.pkl`.  
The deployed application loads this saved model directly and does not retrain during runtime.

## Deployment

The application is deployed with **Streamlit Community Cloud** and can be accessed through the live app link.


## Repository Contents

- `app.py` — main Streamlit application
- `model.pkl` — saved trained model
- `requirements.txt` — Python dependencies

## Live App

TAST Calculator:  
https://tast-calculator-trina.streamlit.app/
