import pandas as pd

classes = ['PSW', 'PSO', 'PSA', 'PIW', 'PIO', 'PIA']

df = pd.DataFrame(columns = ['name', 'class', 'year', 'week', 'show_count', 'current_average', 'last_show', 'overall score', 'me score', 've score', 'm score', 'v score', 'overall increase', 'me increase', 've increase', 'm increase', 'v increase'])

for i in range(2014, 2027):
    for cls in classes:
        df = pd.read_csv(f'class-year/{cls}_{i}.csv')

        names = df['name'].unique()

        for name in names:
            rows = df[df['name'] == name]

            if rows.shape[0] > 1:
                shows = 0

                total_overall_cumulative = 0
                for row in rows:

                    if shows == 0:
                        total_overall_cumulative = current_avg = row['overall score']
                    else:
                        current_avg = round((total_overall_cumulative + row['overall score']) / (shows + 1), 3)


                    if row['overall score'] > 0:
                        shows += 1





