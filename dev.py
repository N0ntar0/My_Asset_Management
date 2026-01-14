import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import signal

class ReloadHandler(FileSystemEventHandler):
    def __init__(self, command):
        self.command = command
        self.process = None
        self.restart()

    def restart(self):
        if self.process:
            # Send SIGTERM to the process group to ensure all children are killed
            try:
                os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
            except ProcessLookupError:
                pass
            self.process.wait() # Wait for process to terminate

        print(f"Starting application: {' '.join(self.command)}")
        # Start new process in a new process group
        self.process = subprocess.Popen(self.command, preexec_fn=os.setsid)

    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.py') or event.src_path.endswith('.json'):
            print(f"Detected change in {event.src_path}. Restarting...")
            self.restart()

if __name__ == "__main__":
    # Command to run the application
    command = [sys.executable, "src/main.py"]
    
    event_handler = ReloadHandler(command)
    observer = Observer()
    observer.schedule(event_handler, path="src", recursive=True)
    observer.start()

    print("Watching for changes in src/...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
