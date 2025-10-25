# 16.03.25
# 3) Third file to edit

import os


# External library
from rich.console import Console


# Internal utilities
from StreamingCommunity.Util.os import os_manager
from StreamingCommunity.Util.message import start_message
from StreamingCommunity.Util.config_json import config_manager


# Logic class
from StreamingCommunity.Api.Template.config_loader import site_constant
from StreamingCommunity.Api.Template.Class.SearchType import MediaItem


# Player
from StreamingCommunity import HLS_Downloader, DASH_Downloader, MP4_downloader, TOR_downloader


# Variable
console = Console()
extension_output = config_manager.get("M3U8_CONVERSION", "extension")


def download_film(select_title: MediaItem) -> str:
    """
    Downloads a film using the provided film ID, title name, and domain.

    Parameters:
        - select_title (MediaItem): The selected media item.

    Return:
        - str: output path if successful, otherwise None
    """
    
    # Display start message
    start_message()
    console.print(f"\n[bold yellow]Download:[/bold yellow] [red]{site_constant.SITE_NAME}[/red] → [cyan]{select_title.name}[/cyan] \n")
    
    # ========================================================================
    # CUSTOMIZABLE SECTION 1: Obtain the download URL
    # ========================================================================
    # This section retrieves the master playlist URL for the video
    # Modify this part based on your source's API or method to get the URL
    
    master_playlist = video_source.get_playlist()
    
    # ========================================================================
    
    # Generate sanitized filename with extension
    title_name = os_manager.get_sanitize_file(select_title.name, select_title.date) + extension_output
    
    # Create output directory path (without extension for folder)
    mp4_path = os.path.join(site_constant.MOVIE_FOLDER, title_name.replace(extension_output, ""))

    # ========================================================================
    # CUSTOMIZABLE SECTION 2: Download process and error handling
    # ========================================================================
    # This section handles the actual download using the appropriate downloader
    # Modify the downloader type (HLS, DASH, MP4, TOR) based on your needs
    # and adjust error handling logic as required
    
    # Start the HLS download process
    hls_process = HLS_Downloader(
        m3u8_url=master_playlist,
        output_path=os.path.join(mp4_path, title_name)
    ).start()

    # Handle download errors by removing incomplete files
    if hls_process['error'] is not None:
        try: 
            os.remove(hls_process['path'])
        except Exception: 
            pass

    # Return the path to the downloaded file
    return hls_process['path']