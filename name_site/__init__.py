# 16.03.25
# 1) Start to edit this file.

import sys
import subprocess


# External library
from rich.console import Console
from rich.prompt import Prompt


# Internal utilities
from StreamingCommunity.Api.Template import get_select_title
from StreamingCommunity.Api.Template.config_loader import site_constant
from StreamingCommunity.Api.Template.Class.SearchType import MediaItem


# Logic class
from .site import title_search, table_show_manager, media_search_manager
from .film import download_film
from .series import download_series


# Variable
indice = 2                      # Edit this value to set the new site index
_useFor = "Film_&_Serie"        # Edit this value to set the type of media the site supports (Anime | Film_&_serie | Serie | Torrent)
_priority = 0
_engineDownload = "hls"         # Edit this value to set the download engine (mp4 | hls | tor | dash)
_deprecate = False

msg = Prompt()
console = Console()


def get_user_input(string_to_search: str = None):
    """
    Asks the user to input a search term.
    Handles both Telegram bot input and direct input.
    If string_to_search is provided, it's returned directly (after stripping).
    """
    if string_to_search is not None:
        return string_to_search.strip()

    return msg.ask(f"\n[purple]Insert a word to search in [green]{site_constant.SITE_NAME}").strip()

def process_search_result(select_title, selections=None):
    """
    Handles the search result and initiates the download for either a film or series.
    
    Parameters:
        select_title (MediaItem): The selected media item
        selections (dict, optional): Dictionary containing selection inputs that bypass manual input
                                    {'season': season_selection, 'episode': episode_selection}

    Returns:
        bool: True if processing was successful, False otherwise
    """
    if not select_title:
        console.print("[yellow]No title selected or selection cancelled.")
        return False
    
    if select_title.type == 'tv':
        season_selection = None
        episode_selection = None

        if selections:
            season_selection = selections.get('season')
            episode_selection = selections.get('episode')
            
        download_series(select_title, season_selection, episode_selection)
        media_search_manager.clear()
        table_show_manager.clear()
        return True
    
    else:
        download_film(select_title)
        table_show_manager.clear()
        return True

# search("Game of Thrones", selections={"season": "1", "episode": "1-3"})
def search(string_to_search: str = None, get_onlyDatabase: bool = False, direct_item: dict = None, selections: dict = None):
    """
    Main function of the application for search.

    Parameters:
        string_to_search (str, optional): String to search for
        get_onlyDatabase (bool, optional): If True, return only the database object
        direct_item (dict, optional): Direct item to process (bypass search)
        selections (dict, optional): Dictionary containing selection inputs that bypass manual input
                                    {'season': season_selection, 'episode': episode_selection}
    """
    if direct_item:
        select_title = MediaItem(**direct_item)
        result = process_search_result(select_title, selections)
        return result
    
    # Get the user input for the search term
    actual_search_query = get_user_input(string_to_search)

    # Handle empty input
    if not actual_search_query:
        return False

    # Search on database
    len_database = title_search(actual_search_query)

    # If only the database is needed, return the manager
    if get_onlyDatabase:
        return media_search_manager
    
    if len_database > 0:
        select_title = get_select_title(table_show_manager, media_search_manager, len_database)
        result = process_search_result(select_title, selections)
        return result
    
    else:
        console.print(f"\n[red]Nothing matching was found for[white]: [purple]{actual_search_query}")
        return False