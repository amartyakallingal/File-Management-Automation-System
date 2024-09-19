from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from time import sleep
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemHandler

source_dir = "Users/amartyakallingal/Downloads"
dest_dir_docs = "Users/amartyakallingal/Desktop/Downloaded Documents"
dest_dir_images = "Users/amartyakallingal/Desktop/Downloaded Images"
dest_dir_sound = "Users/amartyakallingal/Desktop/Downloaded Sound"
dest_dir_video = "Users/amartyakallingal/Desktop/Downloaded Video"

document_extensions = [".doc", ".docx", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]

image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw", ".k25",
                    ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai",
                    ".eps", ".ico"]

sound_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]

video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg", ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]

def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1
    return name

def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        old_name = join(dest, name)
        new_name = join(dest, unique_name)
        rename(old_name, new_name)
    move(entry, dest)

class MoverHandler(FileSystemEventHandler):
    def on_modified(self, name):
        with scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                self.check_document_files(entry, name)
                self.check_image_files(entry, name)
                self.check_sound_files(entry, name)
                self.check_video_files(entry, name)

    def check_document_files(self, entry, name):
        for document_extension in document_extensions:
            if name.endswith(document_extension) or name.endswith(document_extension.upper()):
                move_file(dest_dir_docs, entry, name)
                logging.info(f"Moved document file: {name}")
    
    def check_image_files(self, entry, name):
        for image_extension in image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                move_file(dest_dir_images, entry, name)
                logging.info(f"Moved image file: {name}")

    def check_sound_files(self, entry, name):
        for sound_extension in sound_extensions:
            if name.endswith(sound_extension) or name.endswith(sound_extension.upper()):
                move_file(dest_dir_sound, entry, name)
                logging.info(f"Moved sound file: {name}")

    def check_video_files(self, entry, name):
        for video_extension in video_extensions:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                move_file(dest_dir_video, entry, name)
                logging.info(f"Moved image file: {name}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%y-%m-%d %H:%M%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()