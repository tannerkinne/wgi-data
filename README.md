# WGI Project

## Overview
This project builds machine learning models to analyze and predict performance in Winter Guard International (WGI) competitions. The focus is on turning inconsistent, real-world competition data into structured inputs for classification and insight generation.

---

## Dataset

### Format


### Key Characteristics
- Schools compete in different numbers of weeks
- Scores are split into multiple judging categories
- Data is time-based but inconsistent
- Classes (e.g., PSA) separate competition groups

---

## Problem

### Objective
Predict team performance score based on competition data.


### Challenges
- Uneven number of performances per school
- Missing or incomplete data
- Feature consistency across samples

---

## Data Processing

### Steps
- Clean missing or invalid rows
- Encode categorical variables (class, school name)
- Normalize score features
- Engineer additional features

### Handling Uneven Data
- Treat each week as an independent sample  
or  
- Aggregate by school (averages, trends, progression)

---

## Features

### Base Features
- Overall score
- Music effect
- Visual effect
- Music score
- Visual score
- Week number

### Engineered Features
- Score improvement over time
- Rolling averages
- Consistency metrics

---

## Models

### Random Forest Classifier
- Handles nonlinear relationships well
- Robust to noisy data

### Logistic Regression
- Baseline model
- Interpretable results

---

## Pipeline
1. Load dataset  
2. Preprocess data  
3. Engineer features  
4. Split data (train/test)  
5. Train model  
6. Evaluate performance  
7. Save model  

---

## Evaluation

### Current Metric
- Linear Regression Results:
R^2 Score: 0.8172994408953083
- Random Forest Regressor Results:
R^2 Score: 0.8161793136298667
- Gradient Boosting Regressor Results:
R^2 Score: 0.8256396563097097
- MLP Regressor Results:
R^2 Score: 0.8054112712714496




---

## Notes
- Data inconsistency is the main challenge
- Model performance depends heavily on preprocessing
- Gradient Boosting Regressor currently performs best

---

## Goal
Turn raw WGI competition data into:
- Predictive performance models
- Actionable insights
- A scalable system (potential SaaS application)