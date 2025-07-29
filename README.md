# Tech Challenge 4

## Overview
This repository contains the solution for Tech Challenge 4. It includes all necessary files and instructions to understand and run the project.

## Workflow

### Data Extraction
The dataset used in this project was sourced from yahoo finance. Key feature on the dataset

- `data`: Date and time
- `Close`: Stock Price at closing time

This dataset served as the foundation for building and evaluating the machine learning models in this project.

### Exploratory Data Analysis (EDA)
An in-depth analysis of the data was performed to understand its structure, identify patterns, and handle missing or inconsistent values. Details regarding the analysis can be found in the `TechChallenge_4_EDA.ipynb` file.


### Model Training
A LSTM machine learning models was trained and evaluated to predict stock prices.


### API Development
The final model was integrated into a FastAPI, allowing users to make predictions on daily fire risk by providing input data.

## How to Use

1. Clone the repository:
    ```bash
    git clone https://github.com/CarolineBarbosa/TechChallenge4.git
    cd TechChallenge4
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the API:
    ```bash
    python -m uvicorn app.main:app
    ```
4. Access the API documentation:
    Open your browser and navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to explore the interactive API interface.

### API Endpoints

#### GET Endpoints
Extracts data for sectos, stock codes and stock prices history.

#### POST Endpoint
Offers a comprehensive workflow:
1. Demands a Stock code to make a prediction of the next 30 days.
2. Fetches the data from the source website.
3. Applies data preparation steps.
4. Makes predictions for the next 30 days for the demanded stock option.

## Conclusion
This project demonstrates the end-to-end process of developing a machine learning solution, from data extraction and analysis to model deployment via an API. It showcases the practical application of machine learning in addressing real-world challenges.
