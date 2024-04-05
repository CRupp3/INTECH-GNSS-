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

    # @staticmethod
    # def compile_recent_files(directory, output_file):
    #     files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    #     files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True)
    #     recent_files = files[:min(len(files), 8)]
    #     with open(output_file, 'w') as outfile:
    #         print("Adding files to output:")
    #         for fname in recent_files:
    #             print(fname)
    #             with open(os.path.join(directory, fname)) as infile:
    #                 for line in infile:
    #                     outfile.write(line)
                        
    @staticmethod
    def extract_datetime_from_filename(filename):
        # Assuming the format is 'YYYY MM DD_HH MM.txt'
        try:
            datetime_part = filename[:-4]  # Remove the '.txt' extension
            return datetime.strptime(datetime_part, "%Y %m %d_%H %M")
        except ValueError:
            return None

    @staticmethod
    def compile_recent_files(directory, output_file):
        all_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
        # Extract datetime information from filenames
        files_with_datetime = [(f, Handler.extract_datetime_from_filename(f)) for f in all_files]
        # Filter out files where the datetime could not be parsed
        files_with_datetime = [f for f in files_with_datetime if f[1] is not None]

        if not files_with_datetime:
            print("No valid files found.")
            return

        # Sort files by datetime, most recent first
        files_with_datetime.sort(key=lambda x: x[1], reverse=True)

        # Determine the 2-hour window based on the most recent file's datetime
        most_recent_time = files_with_datetime[0][1]
        two_hours_ago = most_recent_time - timedelta(hours=2)

        # Filter files within the last 2 hours
        recent_files = [f for f in files_with_datetime if f[1] >= two_hours_ago][:8]

        # Write the contents of the filtered files into the output file
        with open(output_file, 'w') as outfile:
            print("Adding files to output:")
            for fname, _ in recent_files:
                print(fname)
                with open(os.path.join(directory, fname)) as infile:
                    for line in infile:
                        outfile.write(line)
        # Insert into IR processing code here (compiled_file.txt)
        filename = "compiled_file.txt"
        QC_filename = '/home/intech/INTECH-GNSS-/Settings.txt'
        dynamic = True
        interpolate = True
        printFailReasons = False
        showAllPlots = False

        calcedHeight, time = calculate_file_name(filename, QC_filename, dynamic, interpolate, printFailReasons, showAllPlots)

        print(calcedHeight, time)
        health_string = CheckHealth(time)

        MessageLogPath = '/home/intech/INTECH-GNSS-/MessageLog.txt'
        messagelog = open(MessageLogPath, 'a')
        messagelog.write('N001' + '-' + time + '-' + calcedHeight + '-' + health_string + '\n')
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
