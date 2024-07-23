import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from json_to_tml import json_to_tml
from thoughtspot_tml import Table
import json
import tempfile

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.json'):
            process_file(event.src_path)

def process_file(file_path):
    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in {file_path}: {str(e)}")
        return

    try:
        tml_content = json_to_tml(json_data)
        
        # Validate TML
        with tempfile.NamedTemporaryFile(mode='w', suffix='.tml', delete=False) as temp_file:
            temp_file.write(tml_content)
            temp_file_path = temp_file.name
        
        Table.load(temp_file_path)
        print(f"TML validation successful for {file_path}")
        
        # Save validated TML
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        tml_file_path = os.path.join('processed_files', f"{base_name}.tml")
        with open(tml_file_path, 'w') as tml_file:
            tml_file.write(tml_content)
        print(f"Validated TML saved to {tml_file_path}")
        
        os.remove(temp_file_path)
    except Exception as e:
        print(f"TML validation failed for {file_path}: {str(e)}")

    # Move processed JSON file
    processed_dir = 'processed_files'
    os.makedirs(processed_dir, exist_ok=True)
    new_path = os.path.join(processed_dir, os.path.basename(file_path))
    os.rename(file_path, new_path)

if __name__ == "__main__":
    path_to_watch = os.path.join(os.path.dirname(__file__), '..', 'incoming_json')
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, path_to_watch, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
