import os
import re
from collections import OrderedDict

from models.docs_index import DocsIndex

# Global flag to ensure documentation is indexed only once per process lifetime
_indexed = False

CATEGORIES = [
    {
        "name": "Foundations",
        "range": range(1, 7), # 01 - 06
    },
    {
        "name": "Database & ORM",
        "range": range(7, 11), # 07 - 10
    },
    {
        "name": "Forms & Data",
        "range": range(11, 17), # 11 - 16
    },
    {
        "name": "Security & Auth",
        "range": range(17, 24), # 17 - 23
    },
    {
        "name": "Reactive UI",
        "range": range(24, 30), # 24 - 29
    },
    {
        "name": "Internal Tools",
        "range": range(30, 37), # 30 - 36
    },
    {
        "name": "Operations & Tools",
        "range": range(37, 47), # 37 - 46
    },
    {
        "name": "References & Advanced",
        "range": range(47, 55), # 47 - 54
    }
]


def _get_category_name(slug):
    match = re.match(r"^(\d+)-", slug)
    if not match:
        return "Other"
    num = int(match.group(1))
    for cat in CATEGORIES:
        if num in cat["range"]:
            return cat["name"]
    return "Other"


def _index_docs(docs_dir):
    """
    Scans the docs directory and populates the SQLite Full-Text Search (FTS) index.
    """
    global _indexed

    # Check if the database already contains documentation entries
    if DocsIndex.count() > 0:
        _indexed = True
        return

    # Prevent multiple indexing attempts within the same request lifecycle
    if _indexed:
        return
    _indexed = True

    # Scan all markdown files excluding README
    files = [f for f in os.listdir(docs_dir) if f.endswith(".md") and f != "README.md"]
    for f in files:
        filepath = os.path.join(docs_dir, f)
        with open(filepath, "r", encoding="utf-8") as fh:
            text = fh.read()

        # Extract the first H1 title from the file
        title_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        title = title_match.group(1) if title_match else f[:-3].replace("-", " ").title()
        
        # Clean text for search indexing by removing special markdown characters
        context = re.sub(r"[#*`\[\]()]", " ", text)

        # Use filename without extension as the routing slug
        slug = f[:-3]
        DocsIndex.create(title=title, slug=slug, context=context)


def handle(request, next):
    """
    Middleware that prepares the documentation menu and search index for all requests.
    """
    # Initialize empty menu to prevent template crashes if the docs directory is missing
    request.params["docs_menu"] = []
    request.params["docs_menu_categorized"] = []

    # Skip processing for API routes
    if request.path.startswith('/api/'):
        return next(request)

    # Resolve the documentation directory relative to the project root
    root_dir = request.environ.get("asok.root", os.getcwd())
    docs_dir = os.path.abspath(os.path.join(root_dir, "..", "docs"))

    if os.path.exists(docs_dir):
        # Index documentation for Full-Text Search
        _index_docs(docs_dir)

        # Build the sidebar menu from markdown filenames
        files = sorted([f for f in os.listdir(docs_dir) if f.endswith(".md") and f != "README.md"])
        menu = []
        for f in files:
            slug = f[:-3]
            # Clean up title: remove numeric prefix (e.g., '01-name' -> 'Name')
            title = slug.replace("-", " ").title()
            if title[0:2].isdigit() and title[2] == " ":
                 title = title[3:]
            menu.append({"slug": slug, "title": title})

        request.params["docs_menu"] = menu

        # Group menu items into categories
        categorized = OrderedDict()
        for cat in CATEGORIES:
            categorized[cat["name"]] = []
        categorized["Other"] = []

        for item in menu:
            cat_name = _get_category_name(item["slug"])
            categorized[cat_name].append(item)

        request.params["docs_menu_categorized"] = [
            {"category": name, "pages": items}
            for name, items in categorized.items()
            if items
        ]

    return next(request)

