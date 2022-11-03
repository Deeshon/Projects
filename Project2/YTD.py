import pytube
from pytube.cli import on_progress



def main():
    link = input("YouTube link: ")
    file_type = file_format(input("File format: "))
    downloader(link , file_type)


def downloader(link , file_type):
    yt = pytube.YouTube(link , on_progress_callback=on_progress)
    print("Downloading...")
    stream = yt.streams.get_by_itag(file_type)
    stream.download()
    print("\nVideo successfullly downloaded")


def file_format(type):
    extension = {"mp4":22 , "mp3":251}
    return extension[type]
   
main()
