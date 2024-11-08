import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from pytubefix import YouTube, Playlist, Stream
import os
import threading

def on_progress(stream: Stream, chunk: bytes, bytes_remaining: int) -> None:
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining 
    percentage_of_completion = bytes_downloaded / total_size * 100
    progress_bar["value"] = int(percentage_of_completion)

def download_link():
    download_button.config(state=tk.DISABLED)  # Disable the download button
    link = link_entry.get()
    format_selected = format_combobox.get()

    if not link or link == "Enter YouTube Link":
        messagebox.showwarning("Invalid Link", "Please enter a valid YouTube link.")
        download_button.config(state=tk.NORMAL)  # Enable the download button
        return

    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)  # Clear previous output

    output_text.insert(tk.END, f"Downloading from link: {link}\n")
    output_text.insert(tk.END, f"Format selected: {format_selected}\n\n")
    output_text.config(state=tk.DISABLED)

    progress_bar["value"] = 0

    progress_bar.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    download_thread = threading.Thread(target=download_task, args=(link, format_selected))
    download_thread.start()

def download_task(link, format_selected):
    try:
        if 'playlist' in link.lower():
            playlist = Playlist(link)
            download_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'YouTube', playlist.title)
            os.makedirs(download_path, exist_ok=True)
            total_videos = len(playlist.video_urls)
            downloaded_videos = 0
            for video in playlist.videos:
                download_playlist_with_progress(video, download_path, format_selected, total_videos, downloaded_videos)
                downloaded_videos += 1
                progress_bar["value"] = (downloaded_videos / total_videos) * 100
        else:
            video = YouTube(link, on_progress_callback=on_progress)
            download_video_with_progress(video, os.path.join(os.path.expanduser('~'), 'Downloads', 'YouTube'), format_selected)

        messagebox.showinfo("Download Successful", "Download completed successfully.")
        link_entry.delete(0, tk.END)  # Clear the link entry field
    except Exception as e:
        print("Error:", e)
        messagebox.showerror("Error", f"An error occurred while downloading: {e}")
    finally:
        download_button.config(state=tk.NORMAL)  # Enable the download button
        progress_bar.grid_forget()  # Hide playlist progress bar after download

def download_video_with_progress(video, download_path, format_selected):
    global pbar
    output_text.config(state=tk.NORMAL)

    if format_selected == "Video":
        stream = video.streams.get_highest_resolution()
        file_path = stream.download(download_path)
    elif format_selected == "Audio":
        stream = video.streams.get_audio_only()
        file_path = stream.download(download_path, mp3=True)
    else:
        raise ValueError("Invalid Format")

    output_text.insert(tk.END, f"Video downloaded successfully to: {file_path}\n")
    output_text.config(state=tk.DISABLED)

def download_playlist_with_progress(video, download_path, format_selected, total_videos, downloaded_videos):
    output_text.config(state=tk.NORMAL)

    if format_selected == "Video":
        stream = video.streams.get_highest_resolution()
        file_path = stream.download(download_path, filename_prefix=str(downloaded_videos + 1) + '_')
    elif format_selected == "Audio":
        stream = video.streams.filter(only_audio=True).first()
        file_path = stream.download(download_path, mp3=True, filename_prefix=str(downloaded_videos + 1) + '_')
    else:
        raise ValueError("Invalid Format")

    output_text.insert(tk.END, f"Video downloaded successfully to: {file_path}\n")
    output_text.config(state=tk.DISABLED)

    # Calculate individual video progress percentage
    video_progress_percentage = int((downloaded_videos + 1) / total_videos * 100)
    progress_bar["value"] = video_progress_percentage

def main():
    global link_entry, format_combobox, output_text, download_button, progress_bar

    root = tk.Tk()
    root.title("YouTube Downloader")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    link_label = tk.Label(frame, text="YouTube Link:", font=("Arial", 14, "bold"))
    link_label.grid(row=0, column=0, sticky="w")

    link_entry = tk.Entry(frame, width=80, font=("Arial", 12), fg='grey')
    link_entry.insert(0, "Enter YouTube Link")
    link_entry.bind("<FocusIn>", on_entry_click)
    link_entry.bind("<FocusOut>", on_focusout)
    link_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
    link_entry.focus()

    format_label = tk.Label(frame, text="Select Format:", font=("Arial", 14, "bold"))
    format_label.grid(row=2, column=0, sticky="w")

    format_combobox = ttk.Combobox(frame, values=["Video", "Audio"], state="readonly", font=("Arial", 12))
    format_combobox.current(0)  # Set default value to "Video"
    format_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    download_button = tk.Button(frame, text="Download", command=download_link, font=("Arial", 12))
    download_button.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

    output_text = tk.Text(frame, height=10, width=80, font=("Arial", 10))
    output_text.config(state=tk.DISABLED)
    output_text.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    progress_bar = ttk.Progressbar(frame, orient="horizontal", length=200, mode="determinate")
    
    root.mainloop()

def on_entry_click(event):
    if link_entry.get() == "Enter YouTube Link":
        link_entry.delete(0, tk.END)
        link_entry.config(fg='black')

def on_focusout(event):
    if not link_entry.get():
        link_entry.insert(0, "Enter YouTube Link")
        link_entry.config(fg='grey')

if __name__ == "__main__":
    main()
