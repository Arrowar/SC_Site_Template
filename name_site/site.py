# 16.03.25
# 2) Second file to edit


# External libraries
from bs4 import BeautifulSoup
from rich.console import Console


# Internal utilities
from StreamingCommunity.Util.headers import get_userAgent
from StreamingCommunity.Util.http_client import create_client
from StreamingCommunity.Util.table import TVShowManager


# Logic class
from StreamingCommunity.Api.Template.config_loader import site_constant
from StreamingCommunity.Api.Template.Class.SearchType import MediaManager


# Variable
console = Console()
media_search_manager = MediaManager()
table_show_manager = TVShowManager()


def title_search(query: str) -> int:
    """
    Search for titles based on a search query.
      
    Parameters:
        - query (str): The query to search for.

    Returns:
        int: The number of titles found.
    """
    media_search_manager.clear()
    table_show_manager.clear()

    # -------------------------
    # SITE-SPECIFIC SECTION
    # Change only the lines below for each site:
    # - search_url: where to perform the search (can be f-string using {query})
    # - results_selector: CSS selector that yields each result element
    # - title_selector / url_selector / image_selector: how to extract fields from each element
    # -------------------------

    # example default (keep or replace with: "your site where with search element")
    search_url = f"{site_constant.FULL_URL}/?story={query}&do=search&subaction=search"
    # search_url = "https://example.com/search?query=your_search_here"  # <-- replace this for other sites

    console.print(f"[cyan]Search url: [yellow]{search_url}")

    try:
        # minimal request line (keep headers)
        response = create_client(headers={'user-agent': get_userAgent()}).get(search_url)
        response.raise_for_status()
    except Exception as e:
        console.print(f"[red]Site: {site_constant.SITE_NAME}, request search error: {e}")
        return 0

    # Use soup or json if api available
    soup = BeautifulSoup(response.text, "html.parser")

    # selector that yields each result element (customize per site)
    results_selector = "div.movie"  # <-- change this to the container of each result

    # iterate results (rename element/ekement as needed)
    for i, element in enumerate(soup.select(results_selector)):
        # Example extraction (adjust selectors or attribute access per site)
        # Option A: anchor inside a heading
        anchor = element.select_one("h2.movie-title a")
        if anchor:
            title = anchor.get_text(strip=True)
            url = anchor.get("href")
        else:
            # Option B: direct attribute or alternative structure
            # title = element.get("title")  # uncomment if title is an attribute
            # url = element.get("href")     # uncomment if element itself is the link
            continue

        # Type detection (adjust the indicator or logic if needed)
        tipo = "tv" if (url and "/serie-tv/" in url) else "film"

        # Image extraction with a common fallback
        img_tag = element.select_one("img.layer-image")
        if img_tag:
            image_attr = img_tag.get("data-src") or img_tag.get("src")
            image = f"{site_constant.FULL_URL}{image_attr}" if image_attr and image_attr.startswith("/") else image_attr
        else:
            image = None

        # If image is present add to media search manager otherwise add None
        media_search_manager.add_media({
            'url': url,
            'name': title,
            'type': tipo,
            'image': image
        })

    # Return the number of titles found
    return media_search_manager.get_length()