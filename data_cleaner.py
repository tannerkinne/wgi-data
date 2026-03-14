import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

df = pd.read_csv('scores.csv')

print(df.head())

for year in df['year'].unique():
    for name in df['name'].unique():
        subset = df[(df['year'] == year) & (df['name'] == name)]


