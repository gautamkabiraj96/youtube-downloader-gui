import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox
import youtube_dl

def show_about_info():
    about_message = "Youtube Downloader v2023.07.24\n Developed by Gautam Kabiraj"
    messagebox.showinfo("About", about_message)


def download_progress_hook(d):
    if d['status'] == 'downloading':
        output_label.config(text="Downloading, please wait.")
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


# GUI setup
root = tk.Tk()
root.title("YouTube Video Downloader")

# Set the background color
root.configure(bg='#f0f0f0')

# Set the font
font = ('Arial', 12)

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
                            '360', '480', '720', '1080', '1440', '2160'], font=font)
quality_combobox.grid(row=1, column=1, padx=5, pady=5)

download_button = tk.Button(main_frame, text="Download Video",
                            font=font, bg='#ff0000', fg='#ffffff', borderwidth=0, 
                            padx=10, pady=5, 
                            activebackground='#000000', activeforeground='#ffffff',
                            command=download_video)
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

root.mainloop()