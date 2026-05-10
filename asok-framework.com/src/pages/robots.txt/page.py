from asok import Request


def render(request: Request):
    """
    Generates a robots.txt file for search engine crawlers.
    Allows all bots and points to the sitemap location.
    """
    # Base URL for the site
    base_url = "https://asok-framework.com"

    # Build robots.txt content
    robots_content = f"""User-agent: *
Allow: /

# Sitemap location
Sitemap: {base_url}/sitemap.xml

# Crawl delay (optional, be polite to servers)
Crawl-delay: 1
"""

    # Set plain text content type
    request.content_type = "text/plain"
    return robots_content.strip()
