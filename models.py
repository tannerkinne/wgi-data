import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.utils import resample
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    accuracy_score, confusion_matrix, classification_report,
    precision_score, recall_score, f1_score
)
import joblib
import random
import shap
from itertools import combinations


from sklearn.inspection import PartialDependenceDisplay

def linear_regression(x_train, y_train, x_test, y_test):
    model = LinearRegression()
    model.fit(x_train, y_train)

    print('Linear Regression Results:')
    print('R^2 Score:', model.score(x_test, y_test))

    return model

def random_forest_regression(x_train, y_train, x_test, y_test):
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(x_train, y_train)

    print('Random Forest Regressor Results:')
    print('R^2 Score:', model.score(x_test, y_test))

    return model

if __name__ == '__main__':
    #
    # df = pd.read_csv('final_stats.csv')
    #
    # df_train= df[df['year'] < 2026]
    #
    # x = df_train.drop(['name', 'class', 'year', 'final score'], axis = 1)
    # y = df_train['final score']
    #
    # x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    #
    # model = linear_regression(x_train, y_train, x_test, y_test)
    #
    # #Redesign above model: is predicting with average scores that include the finals score, so can easily just use slope
    #
    #
    # this_year_x = df[df['year'] == 2026].drop(['name', 'class', 'year', 'final score'], axis = 1)
    # this_year_names = df[df['year'] == 2026]['name']
    #
    # for idx, row in this_year_x.iterrows():
    #     name = this_year_names[idx]
    #     row_df = row.to_frame().T  # Transpose so it’s 1 row
    #     prediction = model.predict(row_df)
    #     print(f"{name} prediction: {prediction[0]}")

    df = pd.read_csv('standardized_data.csv')

    df = df.drop(df[df['current_overall_average'] <=50].index)

    df_train= df[df['year'] < 2026]

    x = df_train.drop(['name', 'class', 'year', 'overall score', 'me score', 've score', 'm score', 'v score'], axis = 1)
    y = df_train['overall score']

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    lr_model = linear_regression(x_train, y_train, x_test, y_test)

    #Redesign above model: is predicting with average scores that include the finals score, so can easily just use slope


    this_year_x = df[df['year'] == 2026].drop(['name', 'class', 'year', 'overall score', 'me score', 've score', 'm score', 'v score'], axis = 1)
    this_year_names = df[df['year'] == 2026]['name']
    this_year_actuals = df[df['year'] == 2026]['overall score']

    for idx, row in this_year_x.iterrows():
        name = this_year_names[idx]
        actual = this_year_actuals[idx]
        row_df = row.to_frame().T  # Transpose so it’s 1 row
        prediction = lr_model.predict(row_df)
        print(f"{name} prediction: {prediction[0]} actual: {actual}")

    print("----------------------------------------------------------------------------------------------")

    rf_model = random_forest_regression(x_train, y_train, x_test, y_test)

    for idx, row in this_year_x.iterrows():
        name = this_year_names[idx]
        actual = this_year_actuals[idx]
        row_df = row.to_frame().T  # Transpose so it’s 1 row
        prediction = rf_model.predict(row_df)
        print(f"{name} prediction: {prediction[0]} actual: {actual}")
