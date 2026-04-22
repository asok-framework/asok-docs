import os
import markdown
import re
from asok import Request


def render(request: Request):
    """
    Renders the changelog page by parsing the root CHANGELOG.md file.
    """
    root_dir = request.environ.get("asok.root", os.getcwd())
    # Navigate up from src/pages/changelog to the project root
    changelog_path = os.path.abspath(os.path.join(root_dir, "..", "CHANGELOG.md"))
    
    if not os.path.exists(changelog_path):
        return "<h1>Changelog file not found</h1>"

    with open(changelog_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Remove the first H1 title as it's already included in the page layout header
    md_text = re.sub(r'^#\s+.*$', '', md_text, count=1, flags=re.MULTILINE)
    md_text = md_text.lstrip()

    # Convert Markdown to HTML with support for code highlighting, tables, and Table of Contents (TOC)
    md_processor = markdown.Markdown(
        extensions=['fenced_code', 'codehilite', 'tables', 'toc'],
        extension_configs={
            'toc': {
                'permalink': '#',
                'permalink_class': 'heading-anchor',
                'permalink_title': 'Link to this section',
                'baselevel': 1,
                'toc_depth': '2-3'
            }
        }
    )
    html_content = md_processor.convert(md_text)

    # Extract TOC tokens for the sidebar navigation
    try:
        toc_tokens = md_processor.toc_tokens
    except:
        toc_tokens = []

    return request.stream("page.html", content=html_content, toc_tokens=toc_tokens)
