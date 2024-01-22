from hevy_data_parsing import parse_csv
from io import StringIO
from nicegui import ui, events

ui.page_title('Hevy Graph Maker')
ui.label('Hevy graph demo')

is_uploaded = False
v = ui.checkbox('Show upload', value=False)

def handle_upload(event: events.UploadEventArguments):
    ui.notify(f'Uploaded {event.name}')
    text = event.content.read().decode('utf-8')
    global df
    df = parse_csv(StringIO(text))
    global v, list_of_exercises, selected_exercise
    v.value = True
    list_of_exercises = df['exercise_title'].unique().tolist()
    selected_exercise = list_of_exercises[0]
    select.set_options(list_of_exercises, value=selected_exercise)
    update_chart()
    
def update_chart():
    get_exercise = df[df['exercise_title'] == selected_exercise]
    get_exercise = get_exercise.sort_values(by=['start_time'], ascending=True)
    times = get_exercise['start_time'].tolist()
    metric = get_exercise[toggled_metric].tolist()
    chart.options['series'][0]={'name': metric_dict[toggled_metric], 'data': list(zip(times, metric)), 'marker': {'symbol': 'diamond', 'enabled': True}}
    chart.update()

def selector_changed(event: events.ValueChangeEventArguments):
    name = type(event.sender).__name__
    if name == 'Select':
        global selected_exercise
        selected_exercise = event.value
    elif name == 'Toggle':
        global toggled_metric
        toggled_metric = event.value
    update_chart()
    

list_of_exercises = ['No exercises uploaded']
selected_exercise = list_of_exercises[0]
toggled_metric = 'heaviest_weight'
metric_dict = {'heaviest_weight':'Heaviest Weight','1rm':'One Rep Max', 'best_set_volume':'Best Set Volume', 'total_volume':'Session Volume', 'total_reps':'Total Reps'}

upload = ui.upload(on_upload=handle_upload, on_rejected=lambda: ui.notify('Rejected!'), max_file_size=5_000_000).props('accept=.csv').classes('max-w-full')

with ui.column().bind_visibility_from(v, 'value'):
    select = ui.select(list_of_exercises, value=list_of_exercises[0], on_change=selector_changed)
    ui.toggle(metric_dict, value='heaviest_weight', on_change=selector_changed)

    chart = ui.highchart({
            'title': False,
            'xAxis': {'type': 'datetime'},
            'yAxis': {'labels': {'format': '{value} kg'}},
            'series': [{}],
        })

ui.run()