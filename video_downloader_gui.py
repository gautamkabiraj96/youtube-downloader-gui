import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox
import traceback
import youtube_dl
import ffmpeg
import base64

# Import the base64_image variable from image_data.py
from image_data import base64_image


def show_about_info():
    about_message = "Youtube Downloader v2023.07.24\n Developed by Gautam Kabiraj"
    messagebox.showinfo("About", about_message)


def download_progress_hook(d):
    if d['status'] == 'downloading':
        output_label.config(text="Downloading...")
        root.update()


def download_video():
    url = url_entry.get()
    download_path = filedialog.askdirectory()

    selected_quality = quality_var.get()
    quality_filter = 'bestvideo[height<={0}]+bestaudio/best'.format(
        selected_quality)

    ydl_opts = {
        'format': quality_filter,
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'progress_hooks': [download_progress_hook],
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
root.title("YouTube Video Downloader")

# Set the background color
root.configure(bg='#f0f0f0')

# Set the font
font = ('Arial', 12)

# Create a frame for the logo
logo_frame = tk.Frame(root, bg='#f0f0f0')
logo_frame.pack(pady=10)

# Create a byte stream from the base64 string
image_data = base64_image.encode()

# Save the byte stream as an image file
with open("temp_image.png", "wb") as image_file:
    image_file.write(base64.b64decode(image_data))

# Load the image from the temporary image file
logo_img = tk.PhotoImage(file="temp_image.png")

# Remove the temporary image file
os.remove("temp_image.png")

logo_label = tk.Label(logo_frame, image=logo_img, bg='#f0f0f0')
logo_label.pack()

# Main frame
main_frame = tk.Frame(root, bg='#f0f0f0')
main_frame.pack(padx=20, pady=10, anchor='center')

url_label = tk.Label(main_frame, text="YouTube URL:", font=font, bg='#f0f0f0')
url_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

url_entry = tk.Entry(main_frame, width=50, font=font)
url_entry.grid(row=0, column=1, padx=5, pady=5)

quality_var = tk.StringVar()
quality_var.set('1080')  # Default quality selection
quality_label = tk.Label(
    main_frame, text="Video Quality:", font=font, bg='#f0f0f0')
quality_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')

quality_combobox = Combobox(main_frame, textvariable=quality_var, values=[
                            '360', '480', '720', '1080', '1440'], font=font)
quality_combobox.grid(row=1, column=1, padx=5, pady=5)

download_button = tk.Button(main_frame, text="Download Video",
                            font=font, bg='#ff0000', fg='#ffffff', command=download_video)
download_button.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

output_label = tk.Label(main_frame, text="", font=font, bg='#f0f0f0')
output_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Create a menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Add "File" menu to the menu bar
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)

# Add "About" option under the "File" menu
file_menu.add_command(label="About", command=show_about_info)

# merge_button = tk.Button(
#     root, text="Merge Video and Audio", command=merge_audio_video)
# merge_button.pack()

root.mainloop()

# Create a byte stream from the base64 string
image_data = base64_image.encode()

# Save the byte stream as an image file
with open("temp_image.png", "wb") as image_file:
    image_file.write(base64.b64decode(image_data))

# Load the image from the temporary image file
logo_img = tk.PhotoImage(file="temp_image.png")

# Remove the temporary image file
os.remove("temp_image.png")
