import os
from datetime import datetime, timezone
from asok import Request


def render(request: Request):
    """
    Generates a dynamic XML sitemap for SEO purposes.
    Includes all documentation pages and static pages with proper priority and update frequency.
    """
    # Base URL for the site
    base_url = "https://asok-framework.com"

    # Get current date in ISO format
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Resolve the documentation directory path
    root_dir = request.environ.get("asok.root", os.getcwd())
    docs_dir = os.path.abspath(os.path.join(root_dir, "..", "docs"))

    # Static pages with their priorities and change frequencies
    static_pages = [
        {"loc": "/", "priority": "1.0", "changefreq": "weekly"},
        {"loc": "/changelog", "priority": "0.7", "changefreq": "weekly"},
        {"loc": "/legal", "priority": "0.3", "changefreq": "yearly"},
        {"loc": "/privacy", "priority": "0.3", "changefreq": "yearly"},
        {"loc": "/terms", "priority": "0.3", "changefreq": "yearly"},
    ]

    # Collect all documentation files
    doc_pages = []
    if os.path.exists(docs_dir):
        for filename in sorted(os.listdir(docs_dir)):
            if filename.endswith(".md") and filename != "README.md":
                # Extract slug from filename (e.g., "01-getting-started.md" -> "01-getting-started")
                slug = filename[:-3]

                # Set higher priority for getting started guide
                priority = "0.9" if "getting-started" in slug else "0.8"

                doc_pages.append({
                    "loc": f"/docs/{slug}",
                    "priority": priority,
                    "changefreq": "monthly"
                })

    # Start building the XML sitemap
    xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    # Add static pages
    for page in static_pages:
        xml_lines.append("  <url>")
        xml_lines.append(f"    <loc>{base_url}{page['loc']}</loc>")
        xml_lines.append(f"    <lastmod>{today}</lastmod>")
        xml_lines.append(f"    <changefreq>{page['changefreq']}</changefreq>")
        xml_lines.append(f"    <priority>{page['priority']}</priority>")
        xml_lines.append("  </url>")

    # Add documentation pages
    for page in doc_pages:
        xml_lines.append("  <url>")
        xml_lines.append(f"    <loc>{base_url}{page['loc']}</loc>")
        xml_lines.append(f"    <lastmod>{today}</lastmod>")
        xml_lines.append(f"    <changefreq>{page['changefreq']}</changefreq>")
        xml_lines.append(f"    <priority>{page['priority']}</priority>")
        xml_lines.append("  </url>")

    xml_lines.append("</urlset>")

    # Join all lines and return as XML response
    sitemap_xml = "\n".join(xml_lines)

    # Set XML content type and return
    request.content_type = "application/xml"
    return sitemap_xml
