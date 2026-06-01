from asok import Request, Table, TableColumn
from pygments import highlight
from pygments.lexers import HtmlLexer, PythonLexer
from pygments.formatters import HtmlFormatter

# Initial seed data for the playground
MOCK_USERS = [
    {
        "id": 1, 
        "name": "Alice Vance", 
        "email": "alice@asok-framework.com", 
        "role": "Administrator", 
        "status": "Active", 
        "avatar": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150"
    },
    {
        "id": 2, 
        "name": "Bob Miller", 
        "email": "bob@asok-framework.com", 
        "role": "Developer", 
        "status": "Active", 
        "avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150"
    },
    {
        "id": 3, 
        "name": "Charlie Rose", 
        "email": "charlie@asok-framework.com", 
        "role": "Designer", 
        "status": "Inactive", 
        "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150"
    },
    {
        "id": 4, 
        "name": "Diana Prince", 
        "email": "diana@asok-framework.com", 
        "role": "Product Manager", 
        "status": "Active", 
        "avatar": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150"
    },
    {
        "id": 5, 
        "name": "Ethan Hunt", 
        "email": "ethan@asok-framework.com", 
        "role": "Security Specialist", 
        "status": "Active", 
        "avatar": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=150"
    },
    {
        "id": 6, 
        "name": "Fiona Gallagher", 
        "email": "fiona@asok-framework.com", 
        "role": "Support Agent", 
        "status": "Inactive", 
        "avatar": "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=150"
    },
    {
        "id": 7, 
        "name": "George Clark", 
        "email": "george@asok-framework.com", 
        "role": "Marketing Director", 
        "status": "Active", 
        "avatar": "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=150"
    },
]


def get_users(request: Request) -> list[dict]:
    """Helper to fetch or seed data list from the current user's session."""
    if "playground_users" not in request.session:
        request.session["playground_users"] = list(MOCK_USERS)
    return request.session["playground_users"]


def render(request: Request):
    """Renders the Tables component playground page."""
    return render_page(request)


def action_delete_user(request: Request):
    """
    Handles both single item row-level and bulk actions deletion.
    Returns JSON response indicating success for dynamic client-side updates.
    """
    user_id = request.get("id")
    
    if user_id == "bulk-delete":
        # Bulk deletion mode: parse selected IDs from JSON payload
        selected_ids = request.json_body
        if isinstance(selected_ids, list):
            users = get_users(request)
            request.session["playground_users"] = [
                u for u in users 
                if u["id"] not in selected_ids and str(u["id"]) not in selected_ids
            ]
    elif user_id:
        # Single deletion mode
        users = get_users(request)
        request.session["playground_users"] = [
            u for u in users if str(u["id"]) != str(user_id)
        ]
        
    return request.json({"status": "ok"})


def action_reset_users(request: Request):
    """Resets the mock users list in the user session."""
    request.session["playground_users"] = list(MOCK_USERS)
    return render_page(request)


def render_page(request: Request):
    """Generates the compiled table components and highlights code snippets."""
    users = get_users(request)

    # Instantiate the native Asok Table component configured in reactive mode
    table = Table(
        users,
        request=request,
        class_="asok-table-container w-full rounded-3xl border border-slate-800 bg-slate-900/40 backdrop-blur-md overflow-hidden shadow-2xl",
        table__class="w-full text-slate-350 border-collapse text-left",
        thead__class="bg-slate-950/60 border-b border-slate-800",
        tr__class="hover:bg-slate-800/30 transition-colors border-b border-slate-800/50 last:border-b-0",
        th__class="px-6 py-4 text-xs font-bold uppercase tracking-wider text-slate-400 text-left border-b border-slate-800",
        td__class="px-6 py-4 text-sm border-b border-slate-850",
        header__class="p-5 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-slate-950/40 border-b border-slate-800",
        footer__class="p-5 flex flex-col sm:flex-row justify-between items-center gap-4 bg-slate-950/40 border-t border-slate-800",
        search__class="px-4 py-2 rounded-xl text-xs bg-slate-950 border border-slate-850 text-slate-200 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all placeholder-slate-600 w-full max-w-[240px]",
        page_link__class="px-3.5 py-1.5 rounded-lg text-xs font-bold bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700/50 transition-colors cursor-pointer select-none disabled:opacity-40 disabled:cursor-not-allowed",
        bulk__class="flex items-center justify-between p-3.5 rounded-xl border border-emerald-500/20 bg-emerald-950/20 backdrop-blur-md text-slate-200 text-xs gap-3 w-full"
    )

    # Configure custom column outputs using HTML templates and custom cell styling
    table.columns = [
        TableColumn("avatar", label="", template='''
            <img src="{{ item.avatar }}" class="w-8 h-8 rounded-full border border-slate-700 object-cover">
        ''', td__class="w-12"),
        TableColumn("name", label="User Name", sortable=True, td__class="font-semibold text-slate-200"),
        TableColumn("email", label="Email", sortable=True, td__class="text-slate-400"),
        TableColumn("role", label="Role", sortable=True, td__class="text-slate-400"),
        TableColumn("status", label="Status", template='''
            <span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium border {{ item.status == "Active" ? "bg-emerald-500/10 border-emerald-500/20 text-emerald-400" : "bg-rose-500/10 border-rose-500/20 text-rose-400" }}">
                <span class="w-1.5 h-1.5 rounded-full {{ item.status == "Active" ? "bg-emerald-400 animate-pulse" : "bg-rose-400" }}"></span>
                {{ item.status }}
            </span>
        '''),
    ]

    # Configure bulk actions and row-level AJAX deletion hook
    table.actions([
        ("Delete", "/components/tables?_action=delete_user&id={id}", "trash", {
            "ajax": True,
            "method": "POST",
            "confirm": "Are you sure you want to delete this user?"
        })
    ])

    # Enable client-side interactivity and paginate to 4 items per page
    table.reactive().paginate(4)

    # 1. Python implementation snippet
    python_code = """# Python definition & Table Setup
from asok import Request, Table, TableColumn

def render(request: Request):
    # Setup interactive responsive data grid
    table = Table(
        get_users(request),
        request=request,
        class_="asok-table-container w-full rounded-3xl bg-slate-900 border border-slate-800",
        table__class="w-full text-slate-300 border-collapse",
        thead__class="bg-slate-950 border-b border-slate-800",
        th__class="px-6 py-4 text-xs font-bold uppercase tracking-wider text-left",
        td__class="px-6 py-4 text-sm border-b border-slate-850",
        search__class="px-4 py-2 rounded-xl text-xs bg-slate-950 border border-slate-800 text-slate-200"
    )

    # Configure columns with layouts
    table.columns = [
        TableColumn("avatar", label="", template='''
            <img src="{{ item.avatar }}" class="w-8 h-8 rounded-full border border-slate-700 object-cover">
        '''),
        TableColumn("name", label="Name", sortable=True),
        TableColumn("email", label="Email", sortable=True),
        TableColumn("role", label="Role", sortable=True),
        TableColumn("status", label="Status", template='''
            <span class="badge {{ item.status == "Active" ? "bg-green" : "bg-red" }}">
                {{ item.status }}
            </span>
        '''),
    ]

    # Add Action Buttons
    table.actions([
        ("Delete", "/components/tables?_action=delete_user&id={id}", "trash", {
            "ajax": True,
            "method": "POST",
            "confirm": "Really delete this user?"
        })
    ])

    # Configure interactive reactive pagination
    table.reactive().paginate(4)

    return request.stream("page.asok", table=table)

def action_delete_user(request: Request):
    user_id = request.get("id")
    if user_id == "bulk-delete":
        selected_ids = request.json_body
        # Delete selected_ids list
    elif user_id:
        # Delete user_id single item
    return request.json({"status": "ok"})
"""

    # 2. HTML template markup snippet
    html_code = """<!-- HTML Template rendering (page.asok) -->
{% block table_playground_block %}
<div id="table_playground_block">
    <!-- Render the complete table widget dynamically -->
    {{ table }}
</div>
{% endblock %}
"""

    formatter = HtmlFormatter(cssclass="codehilite", wrapcode=True)
    lexer_py = PythonLexer()
    lexer_html = HtmlLexer()

    return request.stream("page.asok",
        table=table,
        python_html=highlight(python_code, lexer_py, formatter),
        html_html=highlight(html_code, lexer_html, formatter),
        seo_title="Interactive Data Tables Component - Asok Framework",
        description="Explore Asok's native reactive Table widget featuring client-side search, pagination, bulk selection, column sorting, and AJAX row deletions."
    )
