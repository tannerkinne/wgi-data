import pandas as pd

classes = ['PSW', 'PSO', 'PSA', 'PIW', 'PIO', 'PIA']

new_df = pd.DataFrame(columns = ['name', 'class', 'year', 'week', 'weeks_since', 'show_count', 'current_overall_average', 'current_me_average', 'current_ve_average', 'current_m_average', 'current_v_average', 'last_show_overall_score', 'last_show_me_score', 'last_show_ve_score', 'last_show_m_score', 'last_show_v_score','overall score', 'me score', 've score', 'm score', 'v score', 'last_overall_jump', 'last_me_jump', 'last_ve_jump', 'last_m_jump', 'last_v_jump', 'last_2_overall_average', 'last_2_me_average', 'last_2_ve_average', 'last_2_m_average', 'last_2_v_average'])
last_3_df = pd.DataFrame(columns = ['name', 'class', 'year', 'week', 'weeks_since', 'show_count', 'current_overall_average', 'current_me_average', 'current_ve_average', 'current_m_average', 'current_v_average', 'last_show_overall_score', 'last_show_me_score', 'last_show_ve_score', 'last_show_m_score', 'last_show_v_score','overall score', 'me score', 've score', 'm score', 'v score', 'last_overall_jump', 'last_me_jump', 'last_ve_jump', 'last_m_jump', 'last_v_jump', 'last_2_overall_average', 'last_2_me_average', 'last_2_ve_average', 'last_2_m_average', 'last_2_v_average'])

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

                current_avg = 0
                current_me_avg = 0
                current_ve_avg = 0
                current_m_avg = 0
                current_v_avg = 0

                last_overall_jump = 0
                last_me_jump = 0
                last_ve_jump = 0
                last_m_jump = 0
                last_v_jump = 0

                last_2_overall = []
                last_2_me = []
                last_2_ve = []
                last_2_m = []
                last_2_v = []

                last_2_overall_average = 0
                last_2_me_average = 0
                last_2_ve_average = 0
                last_2_m_average = 0
                last_2_v_average = 0

                for j in range(rows.shape[0]):
                    row = rows.iloc[j]

                    if row['overall score'] <= 60:
                        continue

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

                        last_2_overall.append(row['overall score'])
                        last_2_me.append(row['music effect'])
                        last_2_ve.append(row['visual effect'])
                        last_2_m.append(row['music'])
                        last_2_v.append(row['visual'])

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

                        if shows == 1:
                            last_2_overall.append(row['overall score'])
                            last_2_me.append(row['music effect'])
                            last_2_ve.append(row['visual effect'])
                            last_2_m.append(row['music'])
                            last_2_v.append(row['visual'])
                        else:
                            last_2_overall_holder = [last_2_overall[0], last_2_overall[1]]
                            last_2_me_holder = [last_2_me[0], last_2_me[1]]
                            last_2_ve_holder = [last_2_ve[0], last_2_ve[1]]
                            last_2_m_holder = [last_2_m[0], last_2_m[1]]
                            last_2_v_holder = [last_2_v[0], last_2_v[1]]

                            last_2_overall_average = round(sum(last_2_overall_holder) / 2, 3)
                            last_2_me_average = round(sum(last_2_me_holder) / 2, 3)
                            last_2_ve_average = round(sum(last_2_ve_holder) / 2, 3)
                            last_2_m_average = round(sum(last_2_m_holder) / 2, 3)
                            last_2_v_average = round(sum(last_2_v_holder) / 2, 3)

                            last_2_overall = [last_2_overall[1], row['overall score']]
                            last_2_me = [last_2_me[1], row['music effect']]
                            last_2_ve = [last_2_ve[1], row['visual effect']]
                            last_2_m = [last_2_m[1], row['music']]
                            last_2_v = [last_2_v[1], row['visual']]

                    if shows > 1:
                        last_overall_jump = round(rows['overall score'].iloc[shows - 1] - rows['overall score'].iloc[shows - 2], 3)
                        last_me_jump = round(rows['music effect'].iloc[shows - 1] - rows['music effect'].iloc[shows - 2], 3)
                        last_ve_jump = round(rows['visual effect'].iloc[shows - 1] - rows['visual effect'].iloc[shows - 2], 3)
                        last_m_jump = round(rows['music'].iloc[shows - 1] - rows['music'].iloc[shows - 2], 3)
                        last_v_jump = round(rows['visual'].iloc[shows - 1] - rows['visual'].iloc[shows - 2], 3)


                    last_show_overall_score = rows['overall score'].iloc[shows - 1] if shows > 0 else 0
                    last_show_me_score = rows['music effect'].iloc[shows - 1] if shows > 0 else 0
                    last_show_ve_score = rows['visual effect'].iloc[shows - 1] if shows > 0 else 0
                    last_show_m_score = rows['music'].iloc[shows - 1] if shows > 0 else 0
                    last_show_v_score = rows['visual'].iloc[shows - 1] if shows > 0 else 0

                    weeks_since = row['week'] - rows['week'].iloc[shows - 1] if shows > 0 else 0

                    new_df.loc[len(new_df)] = [name, cls, row['year'], row['week'], weeks_since, shows, current_avg, current_me_avg, current_ve_avg, current_m_avg, current_v_avg, last_show_overall_score, last_show_me_score, last_show_ve_score, last_show_m_score, last_show_v_score, row['overall score'], row['music effect'], row['visual effect'], row['music'], row['visual'], last_overall_jump, last_me_jump, last_ve_jump, last_m_jump, last_v_jump, last_2_overall_average, last_2_me_average, last_2_ve_average, last_2_m_average, last_2_v_average]


                    if row['overall score'] > 0:
                        shows += 1

            length = rows.shape[0]
            if length < 3:
                continue
            last_3 = new_df.iloc[-3:]
            if last_3['show_count'].iloc[0] == 0:
                continue
            for k in range(3):
                last_3_df.loc[len(last_3_df)] = last_3.iloc[k]







new_df.to_csv('standardized_data.csv', index=False)
last_3_df.to_csv('last_3_shows.csv', index=False)

