import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

classes = ['PSW', 'PSO', 'PSA', 'PIW', 'PIO', 'PIA']
df = pd.read_csv('scores_with_weeks.csv')

df = df.drop(df[df['class'].isin(['PSCW','PSCO','PSCA'])].index)
df = df.drop(df[df['overall score'] <=50].index)

df = df.drop_duplicates()

# df23 = df[df['year'] == 2023].sort_values(by = ['name', 'week', 'overall score'], ascending=[True, True, True]).drop_duplicates(subset=['name', 'week'], keep='last')
# df24 = df[df['year'] == 2024].sort_values(by = ['name', 'week', 'overall score'], ascending=[True, True, True]).drop_duplicates(subset=['name', 'week'], keep='last')
# df25 = df[df['year'] == 2025].sort_values(by = ['name', 'week', 'overall score'], ascending=[True, True, True]).drop_duplicates(subset=['name', 'week'], keep='last')
# df26 = df[df['year'] == 2026].sort_values(by = ['name', 'week', 'overall score'], ascending=[True, True, True]).drop_duplicates(subset=['name', 'week'], keep='last')
#
# df23.to_csv('scores23.csv', index=False)
# df24.to_csv('scores24.csv', index=False)
# df25.to_csv('scores25.csv', index=False)
# df26.to_csv('scores26.csv', index=False)
#
# years = [df23, df24, df25, df26]

years = []

for i in range(df['year'].min(), df['year'].max() + 1):
    df_year = df[df['year'] == i].sort_values(by = ['name', 'week', 'overall score'], ascending=[True, True, True]).drop_duplicates(subset=['name', 'week'], keep='last')

    df_year.to_csv(f'scores-year/scores{i}.csv', index=False)

    years.append(df_year)

file_names = []
year_show_max = []

for year in years:
    y = year['year'].iloc[0]
    year_show_max.append(year['week'].max().item())
    for i in range(len(classes)):
        year[year['class'] == classes[i]].to_csv(f'class-year/{classes[i]}_{y}.csv', index=False)
        file_names.append(f'class-year/{classes[i]}_{y}.csv')

print(year_show_max)

final_stats = pd.DataFrame(columns = ['name', 'class', 'year', 'shows', 'first week', 'final week', 'first score', 'final score', 'avg overall increase', 'avg me increase', 'avg ve increase', 'avg m increase', 'avg v increase'])

for f in file_names:
    file = pd.read_csv(f)
    names = file['name'].unique()
    for name in names:

        #shows_attended = file[file['name'] == name].shape[0]

        sub_file = file[file['name'] == name]
        shows_attended = sub_file['week'].nunique()

        if shows_attended > 1:

            year = file['year'].iloc[0]
            first_week = sub_file['week'].iloc[0]
            final_week = sub_file['week'].iloc[-1]
            first_score = sub_file['overall score'].iloc[0]
            final_score = sub_file['overall score'].iloc[-1]

            overall_increase = 0
            me_increase = 0
            ve_increase = 0
            m_increase = 0
            v_increase = 0

            for i in range(1, shows_attended):

                if sub_file['week'].iloc[i] != year_show_max[year - 2023]:

                    temp_overall_increase = sub_file['overall score'].iloc[i] - sub_file['overall score'].iloc[i-1]
                    temp_me_increase = sub_file['music effect'].iloc[i] - sub_file['music effect'].iloc[i-1]
                    temp_ve_increase = sub_file['visual effect'].iloc[i] - sub_file['visual effect'].iloc[i-1]
                    temp_m_increase = sub_file['music'].iloc[i] - sub_file['music'].iloc[i-1]
                    temp_v_increase = sub_file['visual'].iloc[i] - sub_file['visual'].iloc[i-1]

                    overall_increase = round((overall_increase + temp_overall_increase) / 2, 3)
                    me_increase = round((me_increase + temp_me_increase) / 2, 3)
                    ve_increase = round((ve_increase + temp_ve_increase) / 2, 3)
                    m_increase = round((m_increase + temp_m_increase) / 2, 3)
                    v_increase = round((v_increase + temp_v_increase) / 2, 3)

            if overall_increase > 0:
                final_stats.loc[len(final_stats)] = [name, file['class'].iloc[0], year, shows_attended, first_week, final_week, first_score, final_score, overall_increase, me_increase, ve_increase, m_increase, v_increase]

final_stats.to_csv('final_stats.csv', index=False)





#Goal: For each school, find total shows attended. If multiple, find average increase(per WEEK) for overall and sub scores. Seperate by class.



