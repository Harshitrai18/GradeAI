from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class QuizHandler(FileSystemEventHandler):

    def on_created(self,event):
        if event.src_path.endswith(".csv"):
            print(f"New Quiz Detected: {event.src_path}")

def start_monitoring():

    path="data/quizzes"

    observer=Observer()

    observer.schedule(
        QuizHandler(),
        path,
        recursive=False
    )

    observer.start()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()