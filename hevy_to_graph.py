from hevy_data_parsing import parse_csv
from io import StringIO
from nicegui import ui, events

class HevyGraphMaker:

    def __init__(self, file: str, upload) -> None:
        self.df = parse_csv(StringIO(file))
        self.upload = upload
        upload.visible = False
        self.list_of_exercises = self.df['exercise_title'].unique().tolist()
        self.selected_exercise = self.list_of_exercises[0]
        self.toggled_metric = 'heaviest_weight'
        self.metric_dict = {'heaviest_weight':'Heaviest Weight','1rm':'One Rep Max', 'best_set_volume':'Best Set Volume', 'total_volume':'Session Volume', 'total_reps':'Total Reps'}

        
        self.select =ui.select(self.list_of_exercises, value=self.list_of_exercises[0], on_change=self.selector_changed)
        self.toggle = ui.toggle(self.metric_dict, value='heaviest_weight', on_change=self.selector_changed)

        self.chart = ui.highchart({
                'title': False,
                'xAxis': {'type': 'datetime'},
                'yAxis': {'labels': {'format': '{value} kg'}},
                'series': [{}],
            }).classes('max-w-full sm:w-6/12')
        
        self.reset_button = ui.button('Reset', on_click=self.reset)
        
        self.update_chart()

    def update_chart(self):
        get_exercise = self.df[self.df['exercise_title'] == self.selected_exercise]
        get_exercise = get_exercise.sort_values(by=['start_time'], ascending=True)
        times = get_exercise['start_time'].tolist()
        metric = get_exercise[self.toggled_metric].tolist()
        self.chart.options['series'][0]={'name': self.metric_dict[self.toggled_metric], 'data': list(zip(times, metric)), 'marker': {'symbol': 'diamond', 'enabled': True}}
        self.chart.update()

    def selector_changed(self, event: events.ValueChangeEventArguments):
        name = type(event.sender).__name__
        if name == 'Select':
            self.selected_exercise = event.value
        elif name == 'Toggle':
            self.toggled_metric = event.value
        self.update_chart()

    def reset(self):
        print('resetting')
        self.upload.visible = True
        self.select.delete()
        self.toggle.delete()
        self.chart.delete()
        self.reset_button.delete()
