import sys
from pytube import YouTube
import threading
import os
import tkinter as tk
from tkinter import filedialog, ttk
from pytube. innertube import _default_clients

#to add: a download to mp3 button, clean up code and comment stuff, maybe make the window look nicer



#overrides innertube.py default clients
_default_clients[ "ANDROID"][ "context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients[ "ANDROID_EMBED"][ "context"][ "client"]["clientVersion"] = "19.08.35"
_default_clients[ "IOS_EMBED"][ "context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS_MUSIC"][ "context"]["client"]["clientVersion"] = "6.41"
_default_clients[ "ANDROID_MUSIC"] = _default_clients[ "ANDROID_CREATOR" ]

def download_video():
    url = url_entry.get() 
    save_path = save_path_var.get() 

    try: 
        yt = YouTube(url)

        title_label.config(text='Title:' + yt.title)

        #Populate the combobox with quality options
        streams = yt.streams.filter(progressive=True, file_extension="mp4").order_by('resolution')
        resolutions = [stream.resolution for stream in streams]
        quality_combobox['values'] = resolutions
        #set default quality
        quality_combobox.current(0)

        quality_choice = quality_combobox.get()
        stream = streams[resolutions.index(quality_choice)]

        file_size = stream.filesize
        download_progress['maximum'] = file_size

        def download_with_progress():
            stream.download(output_path=save_path, filename=yt.title + ".mp4")
            download_btn['state'] = 'normal' #re enable download button
            download_progress['value'] = 0 # reset progress bar
            status_label.config(text="video downloaded successfully!") 
            os.startfile(save_path) #open the download folder after completion
        
        download_thread = threading.Thread(target=download_with_progress)
        download_thread.start()
    except Exception as e: 
        print(e)
        status_label.config(text="Error downloading!")

root = tk.Tk() 
root.title("Youtube Video Downloader")

url_label = ttk.Label(root, text="Enter youtube URL: ")
url_label.grid(row = 0, column = 0, padx = 5, pady = 5)

url_entry = ttk.Entry(root, width = 50)
url_entry.grid(row = 0, column = 1, columnspan=2, padx=5, pady=5)

save_path_label = ttk.Label(root, text="Save to: ")
save_path_label.grid(row=1, column=0, padx=5, pady=5)

save_path_var = tk.StringVar()
save_path_entry = ttk.Entry(root, textvariable=save_path_var, width=40)
save_path_entry.grid(row=1, column=1, padx=5, pady=5)

browse_button = ttk.Button(root, text="Browse", command=lambda: save_path_var.set(filedialog.askdirectory()))
browse_button.grid(row=1, column=2, padx=5, pady=5)

quality_label = ttk.Label(root, text="Quality:")
quality_label.grid(row=2, column=0, padx=5, pady=5)

quality_combobox = ttk.Combobox(root, width=20)
quality_combobox.grid(row=2, column=1, columnspan=2, padx=5, pady=5)



download_btn = ttk.Button(root, text="Download", command=download_video)
download_btn.grid(row=3, column=0, columnspan=3, pady=10)

download_progress = ttk.Progressbar(root, orient='horizontal', mode='determinate')
download_progress.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky='ew')

title_label = ttk.Label(root, text="Title: ")
title_label.grid(row=5, column=0,columnspan=3)

status_label = ttk.Label(root, text="")
status_label.grid(row=6, column=0, columnspan=3)

root.mainloop()