from hevy_data_parsing import df

from nicegui import ui
from nicegui.events import ValueChangeEventArguments

ui.page_title('Hevy Graph Maker')
ui.label('Hevy graph demo')

list_of_exercises = df['exercise_title'].unique().tolist()
selected_exercise = list_of_exercises[0]
toggled_metric = 'heaviest_weight'

def update_chart():
    get_exercise = df[df['exercise_title'] == selected_exercise]
    get_exercise = get_exercise.sort_values(by=['start_time'], ascending=True)
    times = get_exercise['start_time'].tolist()
    metric = get_exercise[toggled_metric].tolist()
    chart.options['series'][0]={'name': metric_dict[toggled_metric], 'data': list(zip(times, metric)), 'marker': {'symbol': 'diamond', 'enabled': True}}
    chart.update()

def selector_changed(event: ValueChangeEventArguments):
    name = type(event.sender).__name__
    if name == 'Select':
        global selected_exercise
        selected_exercise = event.value
    elif name == 'Toggle':
        global toggled_metric
        toggled_metric = event.value
    update_chart()
    
metric_dict = {'heaviest_weight':'Heaviest Weight','1rm':'One Rep Max', 'best_set_volume':'Best Set Volume', 'total_volume':'Session Volume', 'total_reps':'Total Reps'}

ui.select(list_of_exercises, value=list_of_exercises[0], on_change=selector_changed)
ui.toggle(metric_dict, value='heaviest_weight', on_change=selector_changed)

chart = ui.highchart({
        'title': False,
        'xAxis': {'type': 'datetime'},
        'yAxis': {'labels': {'format': '{value} kg'}},
        'series': [{}],
    })

update_chart()

ui.run()