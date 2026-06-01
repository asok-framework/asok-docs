from asok import Request
from pygments import highlight
from pygments.lexers import HtmlLexer
from pygments.formatters import HtmlFormatter

def render(request: Request):
    """
    Renders the interactive Dropdowns & Tooltips component page.
    """
    # 1. Dropdown Menu
    dropdown_menu_raw = """<div asok-state="{ isOpen: false }" class="relative inline-block text-left">
    <!-- Trigger Button -->
    <button asok-on:click="isOpen = !isOpen" 
            class="px-5 py-2.5 rounded-xl font-bold text-sm bg-indigo-600 hover:bg-indigo-500 text-white transition-all shadow-lg shadow-indigo-600/10 cursor-pointer flex items-center gap-2">
        <span>Options</span>
        <svg class="w-4 h-4 transition-transform duration-200" asok-class="isOpen ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 9l-7 7-7-7" />
        </svg>
    </button>
    
    <!-- Click Outside Overlay -->
    <div asok-show="isOpen" asok-on:click="isOpen = false" class="fixed inset-0 z-10 bg-transparent"></div>
    
    <!-- Dropdown Menu Box with Scale transition -->
    <div asok-show="isOpen" 
         asok-transition="scale 150 fade 100" 
         class="absolute right-0 mt-2 w-48 rounded-xl bg-slate-900 border border-slate-800 shadow-2xl p-2 z-20 text-left">
        <button asok-on:click="isOpen = false" class="w-full text-left px-4 py-2.5 rounded-lg text-sm text-slate-300 hover:text-white hover:bg-white/5 cursor-pointer">
            Edit Profile
        </button>
        <button asok-on:click="isOpen = false" class="w-full text-left px-4 py-2.5 rounded-lg text-sm text-slate-300 hover:text-white hover:bg-white/5 cursor-pointer">
            Security Settings
        </button>
        <div class="h-px w-full my-1 bg-slate-850"></div>
        <button asok-on:click="isOpen = false" class="w-full text-left px-4 py-2.5 rounded-lg text-sm text-red-400 hover:text-red-300 hover:bg-red-500/10 cursor-pointer">
            Sign Out
        </button>
    </div>
</div>"""

    # 2. Context Tooltip
    tooltip_context_raw = """<div asok-state="{ isHovered: false }" class="relative inline-block">
    <!-- Hover Target -->
    <button asok-on:mouseenter="isHovered = true" 
            asok-on:mouseleave="isHovered = false" 
            class="px-5 py-2.5 rounded-xl font-bold text-sm bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700/50 cursor-help">
        Hover Over Me
    </button>
    
    <!-- Tooltip Bubble with Fade Transition -->
    <div asok-show="isHovered" 
         asok-transition="fade 150" 
         class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-1.5 rounded-lg bg-slate-950 border border-slate-850 shadow-xl text-xs text-white font-medium whitespace-nowrap z-30">
        This tooltip uses hover directives and fade transitions.
        <!-- Arrow -->
        <div class="absolute top-full left-1/2 -translate-x-1/2 border-4 border-transparent border-t-slate-950"></div>
    </div>
</div>"""

    formatter = HtmlFormatter(cssclass="codehilite", wrapcode=True)
    lexer = HtmlLexer()

    def highlight_code(code_str):
        return highlight(code_str, lexer, formatter)

    return request.stream("page.asok",
        dropdown_menu_raw=dropdown_menu_raw,
        dropdown_menu_html=highlight_code(dropdown_menu_raw),
        tooltip_context_raw=tooltip_context_raw,
        tooltip_context_html=highlight_code(tooltip_context_raw),
        seo_title="Interactive Dropdowns Component - Asok Framework",
        description="Copy-paste interactive dropdown menus and context tooltips utilizing hover directives and scale transitions."
    )
