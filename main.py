from nicegui import ui, events
from hevy_to_graph import HevyGraphMaker

def handle_upload(event: events.UploadEventArguments):
    ui.notify(f'Uploaded {event.name}')
    text = event.content.read().decode('utf-8')
    HevyGraphMaker(text, upload)
    event.sender.reset()
    
ui.page_title('Hevy Graph Maker')
ui.label('Hevy graph demo')
upload = ui.upload(on_upload=handle_upload, auto_upload=True, on_rejected=lambda: ui.notify('Rejected!'), max_file_size=5_000_000).props('accept=.csv').classes('max-w-full')

ui.run()