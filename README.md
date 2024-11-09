<p align="center">
  <img src="https://capsule-render.vercel.app/api?text=YouTube%20Downloader%20Desktop&animation=fadeIn&type=soft&color=gradient&height=150"/>
</p>

### This project is a YouTube video downloader desktop application built using Python and CustomTkinter. It allows users to input a YouTube video URL or playlist and download the video(s) in available formats directly to their device. This README provides an overview of the project, setup instructions, usage guide, and potential areas for improvement.

⚠️ **Note:** Downloading copyrighted content from YouTube without proper authorization may violate YouTube's terms of service and copyright laws. This project is intended for educational purposes and personal use only. Be sure to respect content creators' rights and follow applicable laws.

## 🚀 Features 

🎉 Input a valid YouTube video or playlist URL.

📺 Choose from available formats (e.g., video or audio).

⬇️ Download selected videos or audio files to a specified location.

📂 Saves downloads to your default `Downloads` folder, with organized subfolders for playlists.

## ⚙️ Setup & Installation 

Follow these steps to set up and run the YouTube Downloader on your desktop:

1. Clone the repository:

    ```bash
    git clone https://github.com/EmileGreyling/YouTube-Downloader-Desktop.git
    ```
    
2. Navigate to the project directory:

    ```bash
    cd YouTube-Downloader-Desktop
    ```
    
3. Create a virtual environment:

    ```bash
    python3 -m venv env
    ```

4. Activate the virtual environment:
   - On Windows:
     ```bash
     env\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source env/bin/activate
     ```
     
5. Install required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

6. Run the application:

    ```bash
    python app.py
    ```

## 📝 Usage 

1. **Enter YouTube URL**: Input a valid YouTube video or playlist URL.
2. **Select Format**: Choose the desired download format (e.g., video or audio).
3. **Download**: Click the "Download" button and monitor progress.
4. **Access Downloaded Files**: Files are saved to your default `Downloads` location in organized folders.

## 🖥️ Compiling as an Executable

To compile the app into an executable:
1. Install **auto-py-to-exe**:
    ```bash
    pip install auto-py-to-exe
    ```

2. Run **auto-py-to-exe** and configure the `.py` script with necessary files (i.e, `logo.ico` for the icon) to create an executable for easier access.

## 🤝 Contributing 

Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make changes, test them, and submit a pull request with explanations.

## 🌟 Improvements 

Here are some potential areas for improvement in this project:

- [ ] **Enhanced User Interface**: Improve the GUI using additional styling and components in CustomTkinter.
- [ ] **Better Error Handling**: Add robust error handling for invalid URLs and unsupported formats.
- [ ] **Download Progress**: Show real-time download progress for each file.
- [ ] **Multi-Platform Support**: Expand support to download videos from other video platforms.
