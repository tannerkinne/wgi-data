import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

classes = ['PSW', 'PSO', 'PSA', 'PIW', 'PIO', 'PIA']
df = pd.read_csv('scores.csv')

df = df.drop(df[df['class'].isin(['PSCW','PSCO','PSCA'])].index)

df23 = df[df['year'] == 2023].sort_values(by = ['name', 'week', 'overall score'], ascending=[True, True, True]).drop_duplicates(subset=['name', 'week'], keep='last')
df24 = df[df['year'] == 2024].sort_values(by = ['name', 'week', 'overall score'], ascending=[True, True, True]).drop_duplicates(subset=['name', 'week'], keep='last')
df25 = df[df['year'] == 2025].sort_values(by = ['name', 'week', 'overall score'], ascending=[True, True, True]).drop_duplicates(subset=['name', 'week'], keep='last')
df26 = df[df['year'] == 2026].sort_values(by = ['name', 'week', 'overall score'], ascending=[True, True, True]).drop_duplicates(subset=['name', 'week'], keep='last')

df23.to_csv('scores23.csv', index=False)
df24.to_csv('scores24.csv', index=False)
df25.to_csv('scores25.csv', index=False)
df26.to_csv('scores26.csv', index=False)

years = [df23, df24, df25, df26]
file_names = []

for year in years:
    y = year['year'].iloc[0]

    for i in range(len(classes)):
        year[year['class'] == classes[i]].to_csv(f'{classes[i]}_{y}.csv', index=False)
        file_names.append(f'{classes[i]}_{y}.csv')

final_stats = pd.DataFrame(columns = ['name', 'class', 'year', 'shows', 'first week', 'final week', 'first score', 'final score', 'avg overall increase', 'avg me increase', 'avg ve increase', 'avg m increase', 'avg v increase'])

for f in file_names:
    file = pd.read_csv(f)
    names = file['name'].unique()
    for name in names:
        shows_attended = file[file['name'] == name].shape[0]
        if shows_attended > 1:
            school = file[file['name'] == name]

            year = file['year'].iloc[0]
            first_week = school['week'].iloc[0]
            final_week = school['week'].iloc[-1]
            first_score = school['overall score'].iloc[0]
            final_score = school['overall score'].iloc[-1]

            overall_increase = 0
            me_increase = 0
            ve_increase = 0
            m_increase = 0
            v_increase = 0

            for i in range(1, shows_attended):
                temp_overall_increase = school['overall score'].iloc[i] - school['overall score'].iloc[i-1]
                temp_me_increase = school['music effect'].iloc[i] - school['music effect'].iloc[i-1]
                temp_ve_increase = school['visual effect'].iloc[i] - school['visual effect'].iloc[i-1]
                temp_m_increase = school['music'].iloc[i] - school['music'].iloc[i-1]
                temp_v_increase = school['visual'].iloc[i] - school['visual'].iloc[i-1]

                overall_increase = round((overall_increase + temp_overall_increase) / 2, 3)
                me_increase = round((me_increase + temp_me_increase) / 2, 3)
                ve_increase = round((ve_increase + temp_ve_increase) / 2, 3)
                m_increase = round((m_increase + temp_m_increase) / 2, 3)
                v_increase = round((v_increase + temp_v_increase) / 2, 3)

            final_stats.loc[len(final_stats)] = [name, file['class'].iloc[0], year, shows_attended, first_week, final_week, first_score, final_score, overall_increase, me_increase, ve_increase, m_increase, v_increase]

final_stats.to_csv('final_stats.csv', index=False)





#Goal: For each school, find total shows attended. If multiple, find average increase(per WEEK) for overall and sub scores. Seperate by class.



