# SC_Site_Template# Site Template Guide

## Overview

This template provides a standardized structure for adding new streaming sites to the StreamingCommunity project. By following this guide, you can quickly integrate a new site with minimal code changes.

## File Structure

```
StreamingCommunity/Api/Site/YOUR_SITE_NAME/
├── __init__.py
├── film.py          # Film download logic
├── serie.py         # Series download logic
├── search.py        # Search functionality
└── util/
    └── ScrapeSerie.py   # Series episode scraper
```

## Quick Start

### 1. Create Your Site Folder

Create a new folder in `StreamingCommunity/Api/Site/` with your site name:

```
StreamingCommunity/Api/Site/MySite/
```

### 2. Copy Template Files

Copy all template files from the template folder into your new site folder.

---

## File-by-File Customization Guide

## 📄 1. `search.py` - Search Functionality

### What to customize:

#### Section 1: Build the search URL (Line ~41)
```python
# Replace with your site's search endpoint
search_url = f"{site_constant.FULL_URL}/search?q={query}"
```

#### Section 2: Define result container selector (Line ~62)
```python
# Replace with the CSS selector for each search result
results_selector = "div.search-result"
```

#### Section 3: Extract data from results (Line ~76)
```python
# Extract title
title = element.select_one("h2.title").get_text(strip=True)

# Extract URL
url = element.select_one("a.link").get("href")

# Determine type (movie or TV series)
tipo = "tv" if "/series/" in url else "film"

# Extract image
img_tag = element.select_one("img.poster")
image = img_tag.get("src") if img_tag else None
```

---

## 📄 2. `film.py` - Film Download

### What to customize:

#### Section 1: Obtain the download URL (Line ~44)
```python
# Replace with your method to get the video URL
# This could involve:
# - API calls: response = api.get_video_url(select_title.id)
# - Page scraping: Parse select_title.url to extract video source
# - Direct URL: Use select_title.url directly if it's the video URL

master_playlist = YOUR_METHOD_TO_GET_VIDEO_URL()
```

#### Section 2: Download and error handling (Line ~56)
```python
# Choose the appropriate downloader:
# - HLS_Downloader for .m3u8 playlists
# - DASH_Downloader for DASH streams
# - MP4_downloader for direct MP4 files
# - TOR_downloader for torrent downloads

downloader = HLS_Downloader(
    m3u8_url=master_playlist,
    output_path=os.path.join(mp4_path, title_name)
).start()
```

---

## 📄 3. `util/ScrapeSerie.py` - Series Episode Scraper

### What to customize:

The entire `collect_season()` method needs to be adapted to your site's HTML structure.

#### Replace these placeholders:

```python
# Extract series title
self.series_name = soup.find("YOUR_TITLE_SELECTOR").get_text(strip=True)

# Find seasons container
seasons_container = soup.find('YOUR_SEASON_CONTAINER_SELECTOR')

# Get all season items
season_items = seasons_container.find_all('YOUR_SEASON_ITEM_SELECTOR')

# For each season:
season_num = int(season_item['YOUR_SEASON_NUMBER_ATTRIBUTE'])
season_name = season_item.get_text(strip=True)

# Find episodes for this season
episodes_container = soup.find('YOUR_EPISODES_CONTAINER_SELECTOR', {
    'YOUR_SEASON_ATTRIBUTE': str(season_num)
})

# Get all episodes
episode_elements = episodes_container.find_all('YOUR_EPISODE_ITEM_SELECTOR')

# For each episode:
ep_num = int(episode_element['YOUR_EPISODE_NUMBER_ATTRIBUTE'])
episode_url = episode_element.get('YOUR_URL_ATTRIBUTE')
episode_name = f"Episode {ep_num}"
```

---

## 📄 4. `serie.py` - Series Download

### What to customize:

#### Section: Retrieve video URL and download (Line ~52)
```python
# Replace with your method to get the episode video URL
# You have access to:
# - obj_episode.url: The episode URL from ScrapeSerie
# - obj_episode.name: Episode name
# - obj_episode.number: Episode number
# - index_season_selected: Season number
# - scrape_serie: The scraper object with all series data

master_playlist = YOUR_METHOD_TO_GET_VIDEO_URL(obj_episode)

# Choose appropriate downloader
downloader = HLS_Downloader(
    m3u8_url=master_playlist,
    output_path=os.path.join(mp4_path, mp4_name)
).start()
```

---

## Support

If you encounter issues:

1. Check the HTML structure of your target site
2. Use browser developer tools to inspect elements
3. Test selectors in Python console before implementing
4. Review existing site implementations for reference