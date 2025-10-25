# 16.03.25
# 4) Fourth file to edit

import logging


# External libraries
from bs4 import BeautifulSoup


# Internal utilities
from StreamingCommunity.Util.headers import get_userAgent
from StreamingCommunity.Util.http_client import create_client
from StreamingCommunity.Api.Player.Helper.Vixcloud.util import SeasonManager


class GetSerieInfo:
    def __init__(self, url):
        """
        Initialize the GetSerieInfo class for scraping TV series information.
        
        Args:
            - url (str): The URL of the streaming site.
        """
        self.headers = {'user-agent': get_userAgent()}
        self.url = url
        self.seasons_manager = SeasonManager()

    # ========================================================================
    # CUSTOMIZABLE SECTION: Parse seasons and episodes structure
    # ========================================================================
    # This method must be completely customized based on your site's HTML structure
    # The goal is to populate self.seasons_manager with seasons and their episodes
    # Each site has a different structure, so adapt the parsing logic accordingly
    # ========================================================================
    
    def collect_season(self) -> None:
        """
        Retrieve all episodes for all seasons.
        
        This method should:
        1. Make HTTP request to self.url
        2. Parse the HTML response
        3. Extract series name (optional)
        4. Find all seasons and their episodes
        5. Populate self.seasons_manager with the data
        
        Customize the entire logic based on your site's structure.
        """
        
        # Make HTTP request to the series page
        response = create_client(headers=self.headers).get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # --- Extract series name (optional) ---
        # TODO: Adjust selector based on your site's title structure
        self.series_name = soup.find("YOUR_TITLE_SELECTOR").get_text(strip=True)

        # --- Find season container ---
        # TODO: Replace with your site's season container selector
        seasons_container = soup.find('YOUR_SEASON_CONTAINER_SELECTOR')
        if not seasons_container:
            return

        # --- Get all season items ---
        # TODO: Replace with selector that returns all individual season elements
        season_items = seasons_container.find_all('YOUR_SEASON_ITEM_SELECTOR')
        
        # --- Iterate through each season ---
        for season_item in season_items:
            
            # TODO: Extract season number from the season element
            season_num = int(season_item['YOUR_SEASON_NUMBER_ATTRIBUTE'])
            
            # TODO: Extract season name from the season element
            season_name = season_item.get_text(strip=True)
            
            # Create a new season in the manager
            current_season = self.seasons_manager.add_season({
                'number': season_num,
                'name': season_name
            })
            
            # --- Find episodes container for this season ---
            # TODO: Replace with selector that finds episodes for current season
            episodes_container = soup.find('YOUR_EPISODES_CONTAINER_SELECTOR', {
                'YOUR_SEASON_ATTRIBUTE': str(season_num)
            })
            
            if not episodes_container:
                continue
            
            # --- Get all episode elements for this season ---
            # TODO: Replace with selector that returns all episode elements
            episode_elements = episodes_container.find_all('YOUR_EPISODE_ITEM_SELECTOR')
            
            # --- Iterate through each episode ---
            for episode_element in episode_elements:
                
                # TODO: Extract episode number from the episode element
                ep_num = int(episode_element['YOUR_EPISODE_NUMBER_ATTRIBUTE'])
                
                # TODO: Extract episode URL or video source from the episode element
                episode_url = episode_element.get('YOUR_URL_ATTRIBUTE')
                
                # TODO: Extract episode name (or use default format)
                episode_name = f"Episode {ep_num}"
                
                # Add episode to the current season
                if current_season:
                    current_season.episodes.add({
                        'number': ep_num,
                        'name': episode_name,
                        'url': episode_url
                    })

    def getNumberSeason(self) -> int:
        """
        Get the total number of seasons available for the series.
        """
        if not self.seasons_manager.seasons:
            self.collect_season()
            
        return len(self.seasons_manager.seasons)
    
    def getEpisodeSeasons(self, season_number: int) -> list:
        """
        Get all episodes for a specific season.
        """
        if not self.seasons_manager.seasons:
            self.collect_season()
            
        # Get season directly by its number
        season = self.seasons_manager.get_season_by_number(season_number)
        return season.episodes.episodes if season else []
        
    def selectEpisode(self, season_number: int, episode_index: int) -> dict:
        """
        Get information for a specific episode in a specific season.
        """
        episodes = self.getEpisodeSeasons(season_number)
        if not episodes or episode_index < 0 or episode_index >= len(episodes):
            logging.error(f"Episode index {episode_index} is out of range for season {season_number}")
            return None
            
        return episodes[episode_index]