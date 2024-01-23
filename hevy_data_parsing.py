import pandas as pd
import locale

def parse_csv(data):
    # Read CSV into DataFrame
    df = pd.read_csv(data)

    # Calculate volume (weight_kg x reps)
    df['best_set_volume'] = df['weight_kg'] * df['reps']
    df['total_volume'] = df['weight_kg'] * df['reps']
    df['1rm'] = df['weight_kg'] * (1 + (df['reps'] / 30))

    # Make new DF where the exercises are grouped by date, we keep the best 1RM and best volume and we sum the total volume for each exercise
    df = df.groupby(['start_time','exercise_title']).agg({'1rm': 'max', 'best_set_volume': 'max', 'total_volume': 'sum', 'weight_kg': 'max', 'reps': 'sum'}).reset_index()
    df = df.rename(columns={'weight_kg' : 'heaviest_weight', 'reps' : 'total_reps'})

    locales = ['en_US.UTF-8','fr_FR.UTF-8','de_DE.UTF-8','es_ES.UTF-8','it_IT.UTF-8','pt_PT.UTF-8','tr_TR.UTF-8','zh_CN.UTF-8','ru_RU.UTF-8','ja_JP.UTF-8','ko_KR.UTF-8']
    
    for loc in locales:
        try:
            locale.setlocale(locale.LC_ALL, loc)
            if(loc == 'fr_FR.UTF-8'):
                df['start_time'] = df['start_time'].str.replace('avr.', 'avril')
            df['start_time'] = pd.to_datetime(df['start_time'], format='%d %b %Y, %H:%M')
            df['start_time'] = df['start_time'].apply(lambda x: x.timestamp()*1000)
            break
        except ValueError:
            pass

    # Sort df by number of occurrences of each exercise
    df['exercise_numinstances'] = df.groupby('exercise_title')['exercise_title'].transform('count')
    df = df.sort_values(by=['exercise_numinstances'], ascending=False)

    return df