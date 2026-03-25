import pandas as pd

classes = ['PSW', 'PSO', 'PSA', 'PIW', 'PIO', 'PIA']

new_df = pd.DataFrame(columns = ['name', 'class', 'year', 'week', 'weeks_since', 'show_count', 'current_overall_average', 'current_me_average', 'current_ve_average', 'current_m_average', 'current_v_average', 'last_show_overall_score', 'last_show_me_score', 'last_show_ve_score', 'last_show_m_score', 'last_show_v_score','overall score', 'me score', 've score', 'm score', 'v score'])

for i in range(2014, 2027):
    for cls in classes:
        df = pd.read_csv(f'class-year/{cls}_{i}.csv')

        names = df['name'].unique()

        for name in names:
            rows = df[df['name'] == name]

            if rows.shape[0] > 1:
                shows = 0

                total_overall_cumulative = 0
                total_me_cumulative = 0
                total_ve_cumulative = 0
                total_m_cumulative = 0
                total_v_cumulative = 0

                current_overall_avg = 0
                current_me_avg = 0
                current_ve_avg = 0
                current_m_avg = 0
                current_v_avg = 0



                for j in range(rows.shape[0]):
                    row = rows.iloc[j]

                    if shows == 0:
                        total_overall_cumulative = row['overall score']
                        current_avg = 0
                        total_me_cumulative = row['music effect']
                        current_me_avg = 0
                        total_ve_cumulative = row['visual effect']
                        current_ve_avg = 0
                        total_m_cumulative = row['music']
                        current_m_avg = 0
                        total_v_cumulative = row['visual']
                        current_v_avg = 0

                    else:
                        # current_avg = round((total_overall_cumulative + row['overall score']) / (shows + 1), 3)
                        # current_me_avg = round((total_me_cumulative + row['music effect']) / (shows + 1), 3)
                        # current_ve_avg = round((total_ve_cumulative + row['visual effect']) / (shows + 1), 3)
                        # current_m_avg = round((total_m_cumulative + row['music']) / (shows + 1), 3)
                        # current_v_avg = round((total_v_cumulative + row['visual']) / (shows + 1), 3)
                        current_avg = round(total_overall_cumulative / (shows), 3)
                        current_me_avg = round(total_me_cumulative / (shows), 3)
                        current_ve_avg = round(total_ve_cumulative / (shows), 3)
                        current_m_avg = round(total_m_cumulative / (shows), 3)
                        current_v_avg = round(total_v_cumulative / (shows), 3)

                        total_overall_cumulative += row['overall score']
                        total_me_cumulative += row['music effect']
                        total_ve_cumulative += row['visual effect']
                        total_m_cumulative += row['music']
                        total_v_cumulative += row['visual']

                    last_show_overall_score = rows['overall score'].iloc[shows - 1] if shows > 0 else 0
                    last_show_me_score = rows['music effect'].iloc[shows - 1] if shows > 0 else 0
                    last_show_ve_score = rows['visual effect'].iloc[shows - 1] if shows > 0 else 0
                    last_show_m_score = rows['music'].iloc[shows - 1] if shows > 0 else 0
                    last_show_v_score = rows['visual'].iloc[shows - 1] if shows > 0 else 0

                    weeks_since = row['week'] - rows['week'].iloc[shows - 1] if shows > 0 else 0

                    new_df.loc[len(new_df)] = [name, cls, i, row['week'], weeks_since, shows, current_avg, current_me_avg, current_ve_avg, current_m_avg, current_v_avg, last_show_overall_score, last_show_me_score, last_show_ve_score, last_show_m_score, last_show_v_score, row['overall score'], row['music effect'], row['visual effect'], row['music'], row['visual']]



                    if row['overall score'] > 0:
                        shows += 1

new_df.to_csv('standardized_data.csv', index=False)


