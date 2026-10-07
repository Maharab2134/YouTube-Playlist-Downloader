import os
import sys
import yt_dlp


# ============================================================
# CONFIGURATION
# ============================================================

PLAYLIST_URL = (
    "https://www.youtube.com/playlist?list=PL8QbsxALagIye_7H3p97-UANM5pkN7EQN"
)

DOWNLOAD_DIR = "downloads"
ARCHIVE_FILE = os.path.join(DOWNLOAD_DIR, "downloaded.txt")


# ============================================================
# COLORS
# ============================================================

class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


# ============================================================
# PROGRESS HOOK
# ============================================================

def progress_hook(data):
    status = data.get("status")

    if status == "downloading":
        downloaded = data.get("downloaded_bytes", 0)
        total = data.get("total_bytes") or data.get(
            "total_bytes_estimate", 0
        )

        speed = data.get("speed")
        eta = data.get("eta")

        if total:
            percentage = downloaded / total * 100
        else:
            percentage = 0

        if speed:
            speed_mb = speed / 1024 / 1024
            speed_text = f"{speed_mb:.2f} MB/s"
        else:
            speed_text = "N/A"

        eta_text = f"{eta}s" if eta else "N/A"

        print(
            f"\r{Colors.CYAN}"
            f"Downloading: {percentage:6.2f}% "
            f"| {speed_text} "
            f"| ETA: {eta_text}"
            f"{Colors.RESET}",
            end="",
            flush=True,
        )

    elif status == "finished":
        print(
            f"\n{Colors.GREEN}"
            f"Download completed. Processing..."
            f"{Colors.RESET}"
        )

    elif status == "error":
        print(
            f"\n{Colors.RED}"
            f"Download error."
            f"{Colors.RESET}"
        )


# ============================================================
# DOWNLOAD TYPE
# ============================================================

def select_download_type():
    print()
    print(f"{Colors.BOLD}{Colors.CYAN}Download Type{Colors.RESET}")
    print("1. Video")
    print("2. Audio")

    while True:
        choice = input("\nSelect [1-2]: ").strip()

        if choice == "1":
            return "video"

        if choice == "2":
            return "audio"

        print(
            f"{Colors.RED}"
            "Invalid choice. Please select 1 or 2."
            f"{Colors.RESET}"
        )


# ============================================================
# VIDEO QUALITY
# ============================================================

def select_video_quality():
    print()
    print(f"{Colors.BOLD}{Colors.CYAN}Video Quality{Colors.RESET}")
    print("1. Best Available")
    print("2. 1080p")
    print("3. 720p")
    print("4. 480p")
    print("5. 360p")
    print("6. 240p")
    print("7. 144p")

    quality_map = {
        "1": None,
        "2": 1080,
        "3": 720,
        "4": 480,
        "5": 360,
        "6": 240,
        "7": 144,
    }

    while True:
        choice = input("\nSelect [1-7]: ").strip()

        if choice in quality_map:
            return quality_map[choice]

        print(
            f"{Colors.RED}"
            "Invalid choice. Please select 1-7."
            f"{Colors.RESET}"
        )


# ============================================================
# FORMAT SELECTOR
# ============================================================

def get_format_selector(download_type, quality=None):

    # --------------------------------------------------------
    # AUDIO
    # --------------------------------------------------------

    if download_type == "audio":
        return (
            "bestaudio[protocol=https]/"
            "bestaudio/best"
        )

    # --------------------------------------------------------
    # BEST AVAILABLE VIDEO
    # --------------------------------------------------------

    if quality is None:
        return (
            "bestvideo[protocol=https]+"
            "bestaudio[protocol=https]/"

            "bestvideo+bestaudio/"
            
            "best"
        )

    # --------------------------------------------------------
    # SPECIFIC QUALITY
    #
    # Example:
    # 1080p requested
    #
    # If 1080p exists -> 1080p
    # If 1080p doesn't exist -> 720p
    # If 720p doesn't exist -> 480p
    # etc.
    # --------------------------------------------------------

    return (
        f"bestvideo[height<={quality}][protocol=https]+"
        f"bestaudio[protocol=https]/"

        f"bestvideo[height<={quality}]+"
        f"bestaudio/"

        f"best[height<={quality}][protocol=https]/"
        f"best[height<={quality}]/"

        "best"
    )


# ============================================================
# POST PROCESSORS
# ============================================================

def get_postprocessors(download_type):

    if download_type == "audio":
        return [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ]

    return []


# ============================================================
# BUILD YT-DLP OPTIONS
# ============================================================

def build_ydl_options(download_type, quality=None):

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    options = {
        # ----------------------------------------------------
        # FORMAT
        # ----------------------------------------------------

        "format": get_format_selector(
            download_type,
            quality
        ),

        # ----------------------------------------------------
        # OUTPUT
        # ----------------------------------------------------

        "outtmpl": os.path.join(
            DOWNLOAD_DIR,
            "%(playlist)s",
            "%(playlist_index)02d - %(title)s.%(ext)s"
        ),

        # ----------------------------------------------------
        # PLAYLIST
        # ----------------------------------------------------

        "noplaylist": False,

        # ----------------------------------------------------
        # RETRIES
        # ----------------------------------------------------

        "retries": 10,
        "fragment_retries": 10,
        "file_access_retries": 5,

        # ----------------------------------------------------
        # CONTINUE PARTIAL DOWNLOAD
        # ----------------------------------------------------

        "continuedl": True,
        "nopart": False,

        # ----------------------------------------------------
        # DOWNLOAD ARCHIVE
        # Prevent duplicate downloads
        # ----------------------------------------------------

        "download_archive": ARCHIVE_FILE,

        # ----------------------------------------------------
        # ERROR HANDLING
        # ----------------------------------------------------

        "ignoreerrors": True,

        # ----------------------------------------------------
        # PROGRESS
        # ----------------------------------------------------

        "progress_hooks": [
            progress_hook
        ],

        # ----------------------------------------------------
        # POST PROCESSING
        # ----------------------------------------------------

        "postprocessors": get_postprocessors(
            download_type
        ),

        # ----------------------------------------------------
        # LOGGING
        # ----------------------------------------------------

        "quiet": False,
        "no_warnings": False,

        # ----------------------------------------------------
        # Network
        # ----------------------------------------------------

        "socket_timeout": 30,

        # ----------------------------------------------------
        # Playlist item order
        # ----------------------------------------------------

        "playliststart": 1,

        # ----------------------------------------------------
        # Clean filenames
        # ----------------------------------------------------

        "windowsfilenames": True,
    }

    # --------------------------------------------------------
    # VIDEO MERGING
    # --------------------------------------------------------

    if download_type == "video":
        options["merge_output_format"] = "mp4"

    return options


# ============================================================
# GET PLAYLIST INFORMATION
# ============================================================

def get_playlist_info():

    print()
    print(
        f"{Colors.YELLOW}"
        "Reading playlist information..."
        f"{Colors.RESET}"
    )

    options = {
        "extract_flat": True,
        "quiet": True,
        "ignoreerrors": True,
    }

    try:

        with yt_dlp.YoutubeDL(options) as ydl:

            info = ydl.extract_info(
                PLAYLIST_URL,
                download=False
            )

        if not info:
            return None

        return info

    except Exception as error:

        print(
            f"{Colors.RED}"
            f"Failed to read playlist: {error}"
            f"{Colors.RESET}"
        )

        return None


# ============================================================
# SHOW PLAYLIST INFORMATION
# ============================================================

def show_playlist_info(info):

    if not info:
        return

    title = info.get(
        "title",
        "Unknown Playlist"
    )

    entries = info.get("entries") or []

    valid_entries = [
        item
        for item in entries
        if item
    ]

    print()
    print(
        f"{Colors.BOLD}"
        f"{Colors.GREEN}"
        "Playlist Information"
        f"{Colors.RESET}"
    )

    print(f"Title : {title}")
    print(f"Videos: {len(valid_entries)}")


# ============================================================
# DOWNLOAD PLAYLIST
# ============================================================

def download_playlist(download_type, quality=None):

    options = build_ydl_options(
        download_type,
        quality
    )

    print()
    print(
        f"{Colors.BOLD}{Colors.BLUE}"
        "Download Configuration"
        f"{Colors.RESET}"
    )

    print(
        f"Type   : "
        f"{download_type.capitalize()}"
    )

    if download_type == "video":

        quality_text = (
            "Best Available"
            if quality is None
            else f"{quality}p or lower"
        )

        print(
            f"Quality: {quality_text}"
        )

    print(
        f"Format : "
        f"{options['format']}"
    )

    print(
        f"Output : "
        f"{DOWNLOAD_DIR}/"
    )

    print()

    confirm = input(
        "Start download? [Y/n]: "
    ).strip().lower()

    if confirm not in ("", "y", "yes"):

        print(
            f"{Colors.YELLOW}"
            "Download cancelled."
            f"{Colors.RESET}"
        )

        return

    print()
    print(
        f"{Colors.BOLD}{Colors.GREEN}"
        "Starting playlist download..."
        f"{Colors.RESET}"
    )

    print()

    try:

        with yt_dlp.YoutubeDL(options) as ydl:

            result = ydl.download(
                [PLAYLIST_URL]
            )

        print()

        if result == 0:

            print(
                f"{Colors.GREEN}"
                f"{Colors.BOLD}"
                "Playlist download completed successfully."
                f"{Colors.RESET}"
            )

        else:

            print(
                f"{Colors.YELLOW}"
                "Playlist finished with some errors."
                f"{Colors.RESET}"
            )

    except KeyboardInterrupt:

        print()
        print(
            f"{Colors.YELLOW}"
            "Download interrupted by user."
            f"{Colors.RESET}"
        )

    except Exception as error:

        print()
        print(
            f"{Colors.RED}"
            f"Download failed: {error}"
            f"{Colors.RESET}"
        )


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print(
        f"{Colors.BOLD}{Colors.CYAN}"
        "=============================================="
        f"{Colors.RESET}"
    )

    print(
        f"{Colors.BOLD}"
        "       YouTube Playlist Downloader"
        f"{Colors.RESET}"
    )

    print(
        f"{Colors.BOLD}{Colors.CYAN}"
        "=============================================="
        f"{Colors.RESET}"
    )

    # --------------------------------------------------------
    # Playlist information
    # --------------------------------------------------------

    info = get_playlist_info()

    if not info:

        print(
            f"{Colors.RED}"
            "Unable to load playlist."
            f"{Colors.RESET}"
        )

        sys.exit(1)

    show_playlist_info(info)

    # --------------------------------------------------------
    # Download type
    # --------------------------------------------------------

    download_type = select_download_type()

    # --------------------------------------------------------
    # Quality
    # --------------------------------------------------------

    quality = None

    if download_type == "video":

        quality = select_video_quality()

    # --------------------------------------------------------
    # Download
    # --------------------------------------------------------

    download_playlist(
        download_type,
        quality
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()