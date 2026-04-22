import os
import re
import subprocess
import markdown
from asok import Request

# Regex to detect GitHub-specific navigation links (e.g., [← Previous | Docs | Next →])
# These are removed to avoid duplication with the site's native navigation
_NAV_RE = re.compile(
    r'^(?:\[[^\]]*\]\([^)]*\.md\)\s*\|\s*){1,2}\[[^\]]*\]\([^)]*\.md\)$',
    re.MULTILINE
)

def render(request: Request):
    """
    Renders a dynamic documentation page from a markdown file based on the URL slug.
    """
    slug = request.params.get("slug")
    
    # Resolve the documentation directory path
    root_dir = request.environ.get("asok.root", os.getcwd())
    docs_dir = os.path.abspath(os.path.join(root_dir, "..", "docs"))
    filepath = os.path.join(docs_dir, f"{slug}.md")

    # Return 404 if the requested markdown file does not exist
    if not os.path.exists(filepath):
        request.status_code(404)
        return request.stream("404.html")

    with open(filepath, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Get the last modification date from git
    last_updated = None
    try:
        result = subprocess.run(
            ['git', 'log', '-1', '--format=%cd', '--date=short', filepath],
            capture_output=True,
            text=True,
            cwd=docs_dir
        )
        if result.returncode == 0 and result.stdout.strip():
            last_updated = result.stdout.strip()
    except:
        pass

    # Calculate estimated reading time (assuming ~200 words per minute)
    word_count = len(md_text.split())
    reading_time = max(1, round(word_count / 200))

    # 1. Strip out the manual GitHub navigation bar
    md_text = _NAV_RE.sub('', md_text).rstrip()

    # 2. Rewrite internal GitHub links: [Text](filename.md) -> [Text](filename)
    # This allows standard markdown files to work as web routes
    md_text = re.sub(r'\[([^\]]+)\]\(([^/)]+)\.md(?:#[^)]*)?\)', r'[\1](\2)', md_text)

    # Remove the trailing horizontal rule if it preceded the navigation
    md_text = re.sub(r'\n---\s*$', '', md_text)

    # Initialize the Markdown processor with core extensions and TOC support
    md_processor = markdown.Markdown(
        extensions=[
            'fenced_code',
            'codehilite',
            'tables',
            'toc'
        ],
        extension_configs={
            'toc': {
                'permalink': '#',
                'permalink_class': 'heading-anchor',
                'permalink_title': 'Link to this section',
                'baselevel': 1,
                'toc_depth': '2-4'
            }
        }
    )
    html_content = md_processor.convert(md_text)

    # Extract the Table of Contents tokens
    try:
        toc_tokens = md_processor.toc_tokens
    except:
        toc_tokens = []

    # Inject Single Page Application (SPA) attributes into internal links
    # This ensures that clicking a link triggers a partial update instead of a full reload
    def add_spa_attrs(match):
        opening_tag = match.group(0)
        # Skip anchor links (internal section jumps)
        if 'href="#' in opening_tag or 'class="heading-anchor"' in opening_tag:
            return opening_tag
        return opening_tag.replace('<a ', '<a data-block="article_content,title,docs_menu" data-push-url data-trigger="click" ')

    html_content = re.sub(r'<a\s[^>]*>', add_spa_attrs, html_content)
    
    # Calculate Next and Previous page references for footer navigation
    menu = request.params.get("docs_menu", [])
    idx = -1
    if slug:
        for i, item in enumerate(menu):
            if item["slug"] == slug:
                idx = i
                break
    
    prev_page = menu[idx-1] if idx > 0 else None
    next_page = menu[idx+1] if idx < len(menu)-1 and idx != -1 else None

    return request.stream("page.html",
        content=html_content,
        slug=slug,
        title=slug.replace("-", " ").title(),
        prev_page=prev_page,
        next_page=next_page,
        toc_tokens=toc_tokens,
        last_updated=last_updated,
        reading_time=reading_time
    )
