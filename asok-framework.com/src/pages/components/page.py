from asok import Request

def render(request: Request):
    """
    Renders the UI Components dashboard.
    """
    components = [
        {
            "name": "Modals & Drawers",
            "slug": "modals",
            "description": "Centered dialogs and slide-over drawers utilizing client-side directives and transition animations.",
            "category": "Interactive Elements",
            "badge": "directives",
        },
        {
            "name": "Accordions & Collapsibles",
            "slug": "accordions",
            "description": "Collapsing accordion sections and expandable FAQ cards with smooth slide and fade transitions.",
            "category": "Disclosure",
            "badge": "directives",
        },
        {
            "name": "Tabs Navigation",
            "slug": "tabs",
            "description": "Horizontal and vertical tab switchers to organize page content efficiently with fade transitions.",
            "category": "Navigation",
            "badge": "directives",
        },
        {
            "name": "Dropdowns & Tooltips",
            "slug": "dropdowns",
            "description": "Interactive context menus, overlays, and hover tooltips with custom directions.",
            "category": "Overlays",
            "badge": "directives",
        },
        {
            "name": "Alerts & Toasts",
            "slug": "alerts",
            "description": "Toast notification stacks, inline banners, and dismissible alerts with reactive state.",
            "category": "Feedback",
            "badge": "asok-state",
        },
        {
            "name": "Buttons",
            "slug": "buttons",
            "description": "Style variants, sizes, icon buttons, loading states, and attached button groups.",
            "category": "Actions",
            "badge": "interactive",
        },
        {
            "name": "Badges & Chips",
            "slug": "badges",
            "description": "Status indicators, removable tag chips, notification counts, and version badges.",
            "category": "Display",
            "badge": "asok-for",
        },
        {
            "name": "Forms",
            "slug": "forms",
            "description": "Text inputs, checkboxes, radio groups, toggles, selects, and textareas with validation states.",
            "category": "Inputs",
            "badge": "asok-bind",
        },
        {
            "name": "Data Tables",
            "slug": "tables",
            "description": "Interactive data table grids showcasing live keyword search, dynamic pagination, column sorting, and bulk actions.",
            "category": "Data Display",
            "badge": "reactive",
        },
    ]
    
    return request.stream("page.asok",
        components=components,
        seo_title="UI Components Library - Asok Framework",
        description="Explore pre-built interactive UI components for the Asok framework. Copy-paste code with native transitions."
    )
