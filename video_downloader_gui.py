import os
import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Combobox
import traceback
import youtube_dl
import ffmpeg

def download_video():
    url = url_entry.get()
    download_path = filedialog.askdirectory()

    selected_quality = quality_var.get()
    quality_filter = 'bestvideo[height<={0}]+bestaudio/best'.format(
        selected_quality)

    ydl_opts = {
        'format': quality_filter,
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s')
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    output_label.config(text="Download completed!")


def merge_audio_video():
    video_file = filedialog.askopenfilename(
        filetypes=[("Video files", "*.mp4")])
    audio_file = filedialog.askopenfilename(
        filetypes=[("Audio files", "*.m4a")])

    output_file = os.path.splitext(video_file)[0] + "_merged.mp4"

    try:
        ffmpeg.input(video_file).output(
            output_file, vcodec="copy", acodec="copy").run()
        output_label.config(text="Merge completed!")
    except Exception as e:
        error_message = f"An error occurred while merging the video and audio: {str(e)}"
        print(traceback.format_exc())
        output_label.config(text=error_message)


# GUI setup
root = tk.Tk()
root.title("YouTube Video Downloader & Merger")

url_label = tk.Label(root, text="YouTube URL:")
url_label.pack()

url_entry = tk.Entry(root, width=50)
url_entry.pack()

quality_var = tk.StringVar()
quality_var.set('1080p')  # Default quality selection
quality_label = tk.Label(root, text="Video Quality:")
quality_label.pack()

quality_combobox = Combobox(
    root, textvariable=quality_var, values=['720p', '1080p'])
quality_combobox.pack()

download_button = tk.Button(
    root, text="Download Video", command=download_video)
download_button.pack()

# merge_button = tk.Button(
#     root, text="Merge Video and Audio", command=merge_audio_video)
# merge_button.pack()

output_label = tk.Label(root, text="")
output_label.pack()

root.mainloop()
