import customtkinter as ctk
from tkinter import messagebox
from pytubefix import YouTube, Playlist, Stream
import os
import threading


def on_progress(stream: Stream, chunk: bytes, bytes_remaining: int) -> None:
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    progress_bar.set(int(percentage_of_completion))


def download_link():
    download_button.configure(state=ctk.DISABLED)
    link = link_entry.get()
    format_selected = format_combobox.get()

    if not link or link == "Enter YouTube Link":
        messagebox.showwarning("Invalid Link", "Please enter a valid YouTube link.")
        download_button.configure(state=ctk.NORMAL)
        return

    output_text.configure(state=ctk.NORMAL)
    output_text.delete("1.0", ctk.END)

    output_text.insert(ctk.END, f"Downloading from link: {link}\n")
    output_text.insert(ctk.END, f"Format selected: {format_selected}\n\n")
    output_text.configure(state=ctk.DISABLED)

    progress_bar.set(0)
    progress_bar.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    download_thread = threading.Thread(
        target=download_task, args=(link, format_selected)
    )
    download_thread.start()


def download_task(link, format_selected):
    try:
        if "playlist" in link.lower():
            playlist = Playlist(link)
            download_path = os.path.join(
                os.path.expanduser("~"), "Downloads", "YouTube", playlist.title
            )
            os.makedirs(download_path, exist_ok=True)
            total_videos = len(playlist.video_urls)
            downloaded_videos = 0
            for video in playlist.videos:
                download_playlist_with_progress(
                    video,
                    download_path,
                    format_selected,
                    total_videos,
                    downloaded_videos,
                )
                downloaded_videos += 1
                progress_bar.set((downloaded_videos / total_videos) * 100)
        else:
            video = YouTube(link, on_progress_callback=on_progress)
            download_video_with_progress(
                video,
                os.path.join(os.path.expanduser("~"), "Downloads", "YouTube"),
                format_selected,
            )

        messagebox.showinfo("Download Successful", "Download completed successfully.")
        link_entry.delete(0, ctk.END)
    except Exception as e:
        print("Error:", e)
        messagebox.showerror("Error", f"An error occurred while downloading: {e}")
    finally:
        download_button.configure(state=ctk.NORMAL)
        progress_bar.grid_forget()


def download_video_with_progress(video, download_path, format_selected):
    output_text.configure(state=ctk.NORMAL)

    if format_selected == "Video":
        stream = video.streams.get_highest_resolution()
        file_path = stream.download(download_path)
    elif format_selected == "Audio":
        stream = video.streams.get_audio_only()
        file_path = stream.download(download_path, mp3=True)
    else:
        raise ValueError("Invalid Format")

    output_text.insert(ctk.END, f"Video downloaded successfully to: {file_path}\n")
    output_text.configure(state=ctk.DISABLED)


def download_playlist_with_progress(
    video, download_path, format_selected, total_videos, downloaded_videos
):
    output_text.configure(state=ctk.NORMAL)

    if format_selected == "Video":
        stream = video.streams.get_highest_resolution()
        file_path = stream.download(
            download_path, filename_prefix=str(downloaded_videos + 1) + "_"
        )
    elif format_selected == "Audio":
        stream = video.streams.filter(only_audio=True).first()
        file_path = stream.download(
            download_path, mp3=True, filename_prefix=str(downloaded_videos + 1) + "_"
        )
    else:
        raise ValueError("Invalid Format")

    output_text.insert(ctk.END, f"Video downloaded successfully to: {file_path}\n")
    output_text.configure(state=ctk.DISABLED)
    video_progress_percentage = int((downloaded_videos + 1) / total_videos * 100)
    progress_bar.set(video_progress_percentage)


def main():
    global link_entry, format_combobox, output_text, download_button, progress_bar

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("YouTube Downloader")
    root.geometry("800x600")  # Set the window size to be larger

    root.iconbitmap(os.path.join(os.path.dirname(__file__), 'logo.ico'))

    frame = ctk.CTkFrame(root, width=750, height=550)  # Adjust frame size
    frame.pack(padx=10, pady=10, fill="both", expand=True)

    link_label = ctk.CTkLabel(frame, text="YouTube Link:", font=("Arial", 16, "bold"))
    link_label.grid(row=0, column=0, sticky="w")

    link_entry = ctk.CTkEntry(
        frame, width=650, font=("Arial", 14), text_color="white"
    )  # Set text color to white
    link_entry.insert(0, "Enter YouTube Link")
    link_entry.bind("<FocusIn>", on_entry_click)
    link_entry.bind("<FocusOut>", on_focusout)
    link_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
    link_entry.focus()

    format_label = ctk.CTkLabel(
        frame, text="Select Format:", font=("Arial", 16, "bold")
    )
    format_label.grid(row=2, column=0, sticky="w")

    format_combobox = ctk.CTkComboBox(
        frame, values=["Video", "Audio"], font=("Arial", 14)
    )
    format_combobox.set("Video")
    format_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    download_button = ctk.CTkButton(
        frame,
        text="Download",
        command=download_link,
        font=("Arial", 14),
        fg_color="#FF0000",  # Set to red color similar to YouTube
        hover_color="#CC0000",  # Darker shade for hover effect
    )
    download_button.grid(row=3, column=0, columnspan=2, pady=15, sticky="ew")

    # Enlarged output text area
    output_text = ctk.CTkTextbox(frame, height=20, width=650, font=("Arial", 12))
    output_text.configure(state=ctk.DISABLED)
    output_text.grid(row=4, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")

    # Enlarged progress bar
    progress_bar = ctk.CTkProgressBar(
        frame, orientation="horizontal", mode="determinate"
    )

    frame.grid_rowconfigure(4, weight=1)  # Allow output_text to expand vertically
    frame.grid_columnconfigure(0, weight=1)  # Allow widgets to expand horizontally

    root.mainloop()


def on_entry_click(event):
    if link_entry.get() == "Enter YouTube Link":
        link_entry.delete(0, ctk.END)
        link_entry.configure(text_color="white")  # Set to white when user types


def on_focusout(event):
    if not link_entry.get():
        link_entry.insert(0, "Enter YouTube Link")
        link_entry.configure(text_color="grey")  # Show grey placeholder text when empty


if __name__ == "__main__":
    main()
