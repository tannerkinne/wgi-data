# WGI Score Predictor & CompetitionSuite Scraper

A machine learning pipeline for predicting Winter Guard International (WGI) competition scores,
paired with a Selenium-based web scraper that collects structured scoring data from CompetitionSuite.

---

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Scraper](#scraper)
  - [How It Works](#how-it-works)
  - [Key Challenges](#key-challenges)
- [ML Pipeline](#ml-pipeline)
  - [Data](#data)
  - [Models](#models)
  - [Performance](#performance)
- [Requirements](#requirements)
- [Setup & Usage](#setup--usage)
- [Known Issues](#known-issues)
- [Future Work](#future-work)

---

## Overview

This project targets the WGI performing arts circuit and aims to predict how a group will score
at a given competition based on historical longitudinal data. It combines two major components:

1. **Scraper** — Automates collection of recap/scoring data from CompetitionSuite score widgets
2. **ML Pipeline** — Trains and evaluates multiple regression models on the collected tabular data

---

## Project Structure

```
wgi-predictor/
├── scraper.py              # Selenium scraper — collects raw scoring data from CompetitionSuite
├── data_cleaner.py         # Cleans and normalizes raw scraped data
├── data_standardizer.py    # Standardizes features for model input
├── models.py               # Trains and evaluates all regression models
├── requirements.txt
└── README.md
```

Scripts are designed to be run **in order** — each step produces output consumed by the next.

---

## Scraper

### How It Works

The scraper uses **Selenium** to navigate CompetitionSuite's nested hierarchy:

```
Season → Year → Event → Score Widget
```

Each level requires dynamic interaction — dropdowns, button clicks, and iframe context switches —
before the score widget's DOM is accessible. Recap links are extracted from within the iframe
after confirming full DOM synchronization. Work with iframes is done in get_iframe_links()

At times when scores were not created using iframe, we fall back to using selenium's mouse
capabilities to click on necessary buttons to reveal the recap data. This is done by finding 
the button element and clicking on it using `element.click()`. These features are executed
in mouse_finder()

### Key Challenges

| Challenge | Solution |
|---|---|
| Score data lives inside a sandboxed `<iframe>` | Switch driver context with `driver.switch_to.frame()` before querying |
| Stale element references after navigation | Re-locate elements after every page transition |
| DOM not ready after JS renders widget | Explicit `WebDriverWait` + `expected_conditions` instead of `time.sleep()` |
| JavaScript-driven content not in raw HTML | Execute queries via `driver.execute_script()` |
| Nested season/year/event hierarchy | Recursive traversal with state tracking to avoid duplicate scrapes |

---

## ML Pipeline

### Data

- **Type:** Longitudinal tabular data (multiple scores per group across seasons/events)
- **Target variable:** Overall competition score
- **Features:** Historical scores, caption breakdowns, event metadata, circuit classification

### Models

Four regression models are trained and compared:

| Model | Notes |
|---|---|
| Linear Regression | Baseline; interpretable coefficients |
| Random Forest | Handles non-linearity; robust to outliers |
| Gradient Boosting | Best single-model performance |
| MLP (Neural Network) | Captures complex feature interactions |

### Performance

| Metric | Value |
|---|---|
| Best R² | ~0.82 |
| Primary metric | R² (coefficient of determination) |

All models are evaluated on a held-out test set. Cross-validation is used during training to
reduce overfitting risk on the relatively small longitudinal dataset.

---

## Requirements

- Python 3.9+
- Google Chrome + matching `chromedriver`
- See `requirements.txt` for full list

```
selenium
scikit-learn
pandas
numpy
matplotlib
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Setup & Usage

Run the scripts in order from the project root:

### 1. Scrape data

```bash
python scraper.py
```

Navigates CompetitionSuite's season/year/event hierarchy and collects raw scoring data.

### 2. Clean data

```bash
python data_cleaner.py
```

Handles missing values, removes malformed entries, and normalizes raw scraped output.

### 3. Standardize features

```bash
python data_standardizer.py
```

Scales and encodes features to prepare the dataset for model input.

### 4. Train & evaluate models

```bash
python models.py
```

Trains all four regression models and outputs performance metrics.

---

## Known Issues

- **CompetitionSuite widget updates** may break iframe selectors — check for DOM structure changes
  if the scraper stops locating elements.
- **Stale element exceptions** can still occur under slow network conditions; add retry logic
  if scraping large event archives.
- MLP performance is sensitive to feature scaling — ensure `StandardScaler` is applied before
  passing data to the neural network.

---

## Future Work

- [ ] Add classification mode to predict placement (1st, 2nd, 3rd) in addition to raw score
- [ ] Expand feature set with caption-level sub-scores (e.g., Movement, Equipment, Design)
- [ ] Automate scraper scheduling for live season tracking
- [ ] Experiment with time-series models (LSTM) to better leverage longitudinal structure
- [ ] Build a simple dashboard to visualize predicted vs. actual scores by group

---

## Notes

This project is not affiliated with WGI or CompetitionSuite. Data is collected for
educational and research purposes only.