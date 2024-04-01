from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import time

class Watcher:
    DIRECTORY_TO_WATCH = r"C:\Users\backj\OneDrive\Documents\Python"

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
    def compile_recent_files(directory, output_file):
        files = [f for f in os.listdir(directory) if f.endswith('.txt')]
        files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True)
        recent_files = files[:min(len(files), 8)]
        with open(output_file, 'w') as outfile:
            print("Adding files to output:")
            for fname in recent_files:
                print(fname)
                with open(os.path.join(directory, fname)) as infile:
                    for line in infile:
                        outfile.write(line)

    def on_created(self, event):
        if event.is_directory:
            return None

        elif event.src_path.endswith('.txt'):
            print(f"New .txt file created: {event.src_path}")
            Handler.compile_recent_files(Watcher.DIRECTORY_TO_WATCH, r'C:\Users\backj\OneDrive\Documents\Python\check_append\compiled_file.txt')

if __name__ == "__main__":
    w = Watcher()
    w.run()