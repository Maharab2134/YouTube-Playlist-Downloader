# YouTube Playlist Downloader

This project is a Python script that downloads videos from a YouTube playlist using the `yt-dlp` library. It checks if the video has already been downloaded and skips downloading it again if it exists. The videos are saved using their titles as filenames.

## Features

- Downloads videos from a YouTube playlist.
- Skips downloading already existing videos.
- Renames the downloaded video files based on the video title.
- Sanitizes filenames to remove invalid characters.

## Prerequisites

1. **Python 3.6+**: Required for running the script.
2. **yt-dlp**: A powerful command-line program to download videos from YouTube and other sites.
3. **ffmpeg** (Optional but recommended): Used for merging video and audio streams.

## Installation

### 1. Clone the Repository

Start by cloning the repository to your local machine:

```bash
git clone https://github.com/Maharab2134/YouTube-Playlist-Downloader.git
cd YouTube-Playlist-Downloader
```

### 2. Create a Virtual Environment

Using a virtual environment ensures that the project’s dependencies do not interfere with your system’s Python packages.

On Debian/Ubuntu, install the venv package first if `python3 -m venv` reports that `ensurepip` is unavailable:

```bash
sudo apt install python3.13-venv
```

```bash
# On Linux/macOS
python3 -m venv myenv

# On Windows
python -m venv myenv
```

### 3. Activate the Virtual Environment

After creating the virtual environment, activate it:

```bash
# On Linux/macOS
source myenv/bin/activate

# On Windows
myenv\Scripts\activate
```

### 4. Install Dependencies

Once the virtual environment is activated, install the required dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 5. Install ffmpeg (Optional but recommended)

You can install ffmpeg using the following commands depending on your operating system:

```bash
# On Ubuntu/Debian-based systems
sudo apt install ffmpeg

# On macOS (using Homebrew)
brew install ffmpeg

# On Windows
# Download the ffmpeg installer from https://ffmpeg.org/download.html and follow the instructions to add it to your PATH.
```

### 6. Usage

Edit the `download_playlist.py` script: Replace the `playlist_url` variable with the URL of the YouTube playlist you want to download:

```python
playlist_url = 'https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID'
```

Run the script: After setting up the URL and installing the required libraries, you can run the script:

```bash
python download_playlist.py
```

### 7. Deactivate the Virtual Environment

After you are done, you can deactivate the virtual environment by running:

```bash
deactivate
```

## Troubleshooting

### Common Errors and Solutions

1. **`yt_dlp.utils.DownloadError`**:
   - Ensure that the `yt-dlp` library is up to date. Run `pip install --upgrade yt-dlp`.
2. **`ERROR: You have requested merging of multiple formats but ffmpeg is not installed`**:

   - Install ffmpeg as described in the installation section.

3. **File Already Exists**:
   - The script checks for existing files and skips downloading if the video is already downloaded.

## Example Output

When you run the script, you will see output similar to this:

```
Checking: Video Title 1
Downloading: Video Title 1
Downloaded: Video Title 1.mp4
Checking: Video Title 2
Already downloaded: Video Title 2.mp4
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
