from nicegui import ui, events
from hevy_to_graph import HevyGraphMaker

@ui.page('/')
def main():
    def handle_upload(event: events.UploadEventArguments):
        ui.notify(f'Uploaded {event.name}')
        text = event.content.read().decode('utf-8')
        HevyGraphMaker(text, upload)
        event.sender.reset()
        
    ui.label('Hevy graph demo')
    upload = ui.upload(on_upload=handle_upload, auto_upload=True, on_rejected=lambda: ui.notify('Rejected!'), max_file_size=5_000_000).props('accept=.csv').classes('max-w-full')

ui.run(title='Hevy Graph Demo', favicon='https://www.hevyapp.com/wp-content/uploads/2019/06/cropped-Icon1024_Android-192x192.png')
# TO RUN ON FLY.IO :
# ui.run(host=0, port=80, title='Hevy Graph Demo', favicon='https://www.hevyapp.com/wp-content/uploads/2019/06/cropped-Icon1024_Android-192x192.png')
