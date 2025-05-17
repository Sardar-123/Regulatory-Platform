# DORA Compliance Score Predictor

## Description
This project provides a platform for calculating DORA compliance scores and generating actionable recommendations to improve compliance. The platform leverages machine learning models and Azure OpenAI's LLM capabilities.

## Features
- Input application-specific ratings to calculate compliance scores.
- Generate personalized recommendations using GPT-4.
- Download recommendations as a PDF.

## Folder Structure
- `data/`: Pre-trained models, encoders, and data-related resources.
- `ml/`: ML-based scoring and recommendation logic.
- `ui/`: Streamlit UI components.
- `config/`: Global settings like API keys and configuration.
- `scripts/`: Utility scripts, e.g., for PDF generation.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Configure OpenAI API by adding your key in `.azure_openai_key.txt`.
3. Run the application: `streamlit run ui/main.py`
