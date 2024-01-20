import pandas as pd

# Read CSV into DataFrame
df = pd.read_csv('workouts.csv')


# Calculate volume (weight_kg x reps)
df['best_set_volume'] = df['weight_kg'] * df['reps']
df['total_volume'] = df['weight_kg'] * df['reps']
df['1rm'] = df['weight_kg'] * (1 + (df['reps'] / 30))

# Make new DF where the exercises are grouped by date, we keep the best 1RM and best volume and we sum the total volume for each exercise
df = df.groupby(['start_time','exercise_title']).agg({'1rm': 'max', 'best_set_volume': 'max', 'total_volume': 'sum', 'weight_kg': 'max', 'reps': 'sum'}).reset_index()
df = df.rename(columns={'weight_kg' : 'heaviest_weight', 'reps' : 'total_reps'})

# Convert start_time to datetime
df['start_time'] = pd.to_datetime(df['start_time'], format='%d %b %Y, %H:%M')

# Sort df by number of occurrences of each exercise
df['exercise_numinstances'] = df.groupby('exercise_title')['exercise_title'].transform('count')
df = df.sort_values(by=['exercise_numinstances'], ascending=False)