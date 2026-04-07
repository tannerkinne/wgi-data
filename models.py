import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
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
from sklearn.metrics import mean_absolute_error


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

def gradient_boosting_regression(x_train, y_train, x_test, y_test):
    model = GradientBoostingRegressor(n_estimators=100, random_state=42)
    model.fit(x_train, y_train)

    print('Gradient Boosting Regressor Results:')
    print('R^2 Score:', model.score(x_test, y_test))

    return model

def mlp_regression(x_train, y_train, x_test, y_test):
    model = MLPRegressor(hidden_layer_sizes=(100,), max_iter=500, random_state=42)
    model.fit(x_train, y_train)

    print('MLP Regressor Results:')
    print('R^2 Score:', model.score(x_test, y_test))

    return model

def mega_predictor(models, x):
    predictions = np.array([model.predict(x) for model in models])
    return np.mean(predictions, axis=0)

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
    df = df.drop(df[df['show_count'] <= 1].index)
    df = df.drop(df[df['year'] == 2014].index)
    df = df.drop(df[df['year'] == 2020].index)
    df = df.drop(df[df['year'] == 2021].index)
    df = df.drop(df[df['show_count'] == 7].index)


    df_train= df[df['year'] < 2026]

    class_to_number = {'PSA': 0, 'PIA': 1, 'PSO':2, 'PIO':3, 'PSW':4, 'PIW': 5}
    df_train['class'] = df_train['class'].map(class_to_number)

    x = df_train.drop(['name', 'overall score', 'me score', 've score', 'm score', 'v score'], axis = 1)
    y = df_train['overall score']

    print(x.columns)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    lr_model = linear_regression(x_train, y_train, x_test, y_test)

    #Redesign above model: is predicting with average scores that include the finals score, so can easily just use slope


    this_year_x = df[df['year'] == 2026].drop(['name', 'class', 'year', 'overall score', 'me score', 've score', 'm score', 'v score'], axis = 1)
    this_year_names = df[df['year'] == 2026]['name']
    this_year_actuals = df[df['year'] == 2026]['overall score']

    # for idx, row in this_year_x.iterrows():
    #     name = this_year_names[idx]
    #     actual = this_year_actuals[idx]
    #     row_df = row.to_frame().T  # Transpose so it’s 1 row
    #     prediction = lr_model.predict(row_df)
    #     print(f"{name} prediction: {prediction[0]} actual: {actual}")

    print("----------------------------------------------------------------------------------------------")

    rf_model = random_forest_regression(x_train, y_train, x_test, y_test)

    # for idx, row in this_year_x.iterrows():
    #     name = this_year_names[idx]
    #     actual = this_year_actuals[idx]
    #     row_df = row.to_frame().T  # Transpose so it’s 1 row
    #     prediction = rf_model.predict(row_df)
    #     print(f"{name} prediction: {prediction[0]} actual: {actual}")

    print("----------------------------------------------------------------------------------------------")

    gb_model = gradient_boosting_regression(x_train, y_train, x_test, y_test)

    # for idx, row in this_year_x.iterrows():
    #     name = this_year_names[idx]
    #     actual = this_year_actuals[idx]
    #     row_df = row.to_frame().T
    #     prediction = gb_model.predict(row_df)
    #     print(f"{name} prediction: {prediction[0]} actual: {actual}")

    print("----------------------------------------------------------------------------------------------")

    mlp_model = mlp_regression(x_train, y_train, x_test, y_test)

    # for idx, row in this_year_x.iterrows():
    #     name = this_year_names[idx]
    #     actual = this_year_actuals[idx]
    #     row_df = row.to_frame().T
    #     prediction = mlp_model.predict(row_df)
    #     print(f"{name} prediction: {prediction[0]} actual: {actual}")


    print("----------------------------------------------------------------------------------------------")

    gb_residuals = y_test - gb_model.predict(x_test)

    # df["residual"] = gb_residuals
    # df.groupby("show_count")["residual"].apply(lambda x: np.abs(x).mean()).plot(kind="bar")
    # plt.title("MAE by show count")
    # plt.show()
    #
    # # 2. gb_residuals by class — is one class dragging you down?
    # df.groupby("class")["residual"].apply(lambda x: np.abs(x).mean()).plot(kind="bar")
    # plt.title("MAE by class")
    # plt.show()
    #
    # # 3. gb_residuals by year — model degrading over time?
    # df.groupby("year")["residual"].apply(lambda x: np.abs(x).mean()).plot(kind="bar")
    # plt.title("MAE by year")
    # plt.show()
    #
    # plt.scatter(lr_model.predict(x_test), gb_residuals)
    # plt.title("gb_residuals vs Predicted Values")
    # plt.show()
    #
    # plt.scatter(x_test['current_overall_average'], gb_residuals)
    # plt.title("gb_residuals vs Current Overall Average")
    # plt.show()
    #
    # plt.scatter(x_test['show_count'], gb_residuals)
    # plt.title("gb_residuals vs Show Count")
    # plt.show()
    #
    # plt.scatter(x_test['week'], gb_residuals)
    # plt.title("gb_residuals vs Week")
    # plt.show()

    print('For Gradient Boosting Regressor:')
    mae = mean_absolute_error(y_test, gb_model.predict(x_test))
    within_1 = np.mean(np.abs(y_test - gb_model.predict(x_test)) < 1.0)
    within_2 = np.mean(np.abs(y_test - gb_model.predict(x_test)) < 2.0)
    within_3 = np.mean(np.abs(y_test - gb_model.predict(x_test)) < 3.0)

    print(f"MAE:           {mae:.2f} pts")
    print(f"Within 1 pt:   {within_1:.1%}")
    print(f"Within 2 pts:  {within_2:.1%}")
    print(f"Within 3 pts:  {within_3:.1%}")

    mega_model = [lr_model, rf_model, gb_model, mlp_model]

    # print('For Mega Predictor:')
    # mae = mean_absolute_error(y_test, mega_predictor(mega_model, x_test))
    # within_1 = np.mean(np.abs(y_test - mega_predictor(mega_model, x_test)) < 1.0)
    # within_2 = np.mean(np.abs(y_test - mega_predictor(mega_model, x_test)) < 2.0)
    # within_3 = np.mean(np.abs(y_test - mega_predictor(mega_model, x_test)) < 3.0)
    #
    # print(f"MAE:           {mae:.2f} pts")
    # print(f"Within 1 pt:   {within_1:.1%}")
    # print(f"Within 2 pts:  {within_2:.1%}")
    # print(f"Within 3 pts:  {within_3:.1%}")

    east = pd.DataFrame([{
        'class': 0,
        'year': 2026,
        'week': 10,
        'weeks_since': 1,
        'show_count': 3,
        'current_overall_average': 83.867,
        'current_me_average': 25.225,
        'current_ve_average': 16.1,
        'current_m_average': 25.642,
        'current_v_average': 16.475,
        'last_show_overall_score': 85.55,
        'last_show_me_score': 25.35,
        'last_show_ve_score': 17.1,
        'last_show_m_score': 26.2,
        'last_show_v_score': 16.9,
        'last_overall_jump': 0.0,
        'last_me_jump': 0.0,
        'last_ve_jump': 0.0,
        'last_m_jump': 0.0,
        'last_v_jump': 0.0,
        'last_2_overall_average': 84.375,
        'last_2_me_average': 25.256,
        'last_2_ve_average': 16.6,
        'last_2_m_average': 25.831,
        'last_2_v_average': 16.688,
    }])


    print('-----------------------------------------------------------------------------------------------')
    print(f'Predictions for East week 10: {gb_model.predict(east)}')