from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import time
from datetime import datetime, timedelta
#from calculate_file_name import calculate_file_name
from calculate_file_name import calculate_file_name
from CheckHealth import (CheckHealth)

class Watcher:
    DIRECTORY_TO_WATCH = "/home/intech/INTECH-GNSS-/RawData"

    def __init__(self):
        self.observer = Observer()

    def print_initial_files(self):
        # List initial .txt files in the directory
        initial_files = [f for f in os.listdir(self.DIRECTORY_TO_WATCH) if f.endswith('.txt')]
        if initial_files:  # Check if the list is not empty
            print("Initial .txt files in directory:")
            for file in initial_files:
                print(file)
        else:
            print("No initial .txt files observed.")

    def run(self):
        self.print_initial_files()  # Print the initial list of files
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")
        self.observer.join()

class Handler(FileSystemEventHandler):
                        
    @staticmethod
    def extract_datetime_from_filename(filename):
        # Assuming the format is 'YYYY MM DD_HH MM.txt'
        try:
            datetime_part = filename[:-4]  # Remove the '.txt' extension
            return datetime.strptime(datetime_part, "%Y_%m_%d_%H_%M")
        except ValueError:
            return None

    @staticmethod
    def compile_recent_files(directory, output_file):
        all_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
        files_with_datetime = [(f, Handler.extract_datetime_from_filename(f)) for f in all_files if Handler.extract_datetime_from_filename(f) is not None]

        if not files_with_datetime:
            print("No valid files found.")
            return

        # Sort files by datetime, most recent first
        files_with_datetime.sort(key=lambda x: x[1], reverse=True)

        # The most recent file's datetime determines the two-hour window
        most_recent_time = files_with_datetime[0][1]
        two_hours_ago = most_recent_time - timedelta(hours=2)

        # Filter files within the last 2 hours and ensure they are not empty
        recent_files_with_content = []
        for filename, file_datetime in files_with_datetime:
            if file_datetime < two_hours_ago or len(recent_files_with_content) >= 8:
                break  # Stop if the file is outside the 2-hour window or we have enough files

            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                first_char = file.read(1)
                if first_char:  # File is not empty
                    file.seek(0)  # Rewind to start
                    content = first_char + file.read()  # Ensure we get all content
                    recent_files_with_content.append((filename, content))

        if not recent_files_with_content:
            print("No non-empty files found in the last 2 hours.")
            return

        # Files are already in reverse chronological order, but we limited selection by the two-hour window correctly this time
        with open(output_file, 'w') as outfile:
            print("Adding files to output in chronological order:")
            for fname, content in reversed(recent_files_with_content):  # Reverse to chronological order
                print(fname)
                outfile.write(content)
        
        # Insert into IR processing code here (compiled_file.txt)
        filename = "compiled_file.txt"
        QC_filename = '/home/intech/INTECH-GNSS-/settings.txt'
        dynamic = True
        interpolate = True
        printFailReasons = False
        showAllPlots = False

        calcedHeight, time = calculate_file_name(filename, QC_filename, dynamic, interpolate, printFailReasons, showAllPlots)
        
        if calcedHeight is not None:
            calcedHeight_string = f'{calcedHeight:.3f}'
        else:
            calcedHeight_string = str(calcedHeight)
        print(calcedHeight, time)
        health_string = CheckHealth(time)

        MessageLogPath = '/home/intech/INTECH-GNSS-/MessageLog.txt'
        messagelog = open(MessageLogPath, 'a')
        messagelog.write('N002' + '-' + time + '-' + calcedHeight_string + '-' + health_string + '\n')
        messagelog.close()

    def on_created(self, event):
        if event.is_directory:
            return None

        elif event.src_path.endswith('.txt'):
            print(f"New .txt file created: {event.src_path}")
            Handler.compile_recent_files(Watcher.DIRECTORY_TO_WATCH, 'compiled_file.txt')

if __name__ == "__main__":
    w = Watcher()
    w.run()
