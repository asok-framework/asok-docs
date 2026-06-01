from asok import Request
from pygments import highlight
from pygments.lexers import HtmlLexer
from pygments.formatters import HtmlFormatter


def render(request: Request):
    """
    Renders the interactive Buttons component playground page.
    """
    # 1. Style Variants
    variants_raw = """<div class="flex flex-wrap gap-4 items-center justify-center">
    <!-- Primary Button -->
    <button class="px-5 py-2.5 rounded-xl font-bold text-sm bg-indigo-600 hover:bg-indigo-500 active:scale-95 text-white transition-all shadow-lg shadow-indigo-600/20 cursor-pointer select-none">
        Primary Action
    </button>

    <!-- Outlined Button -->
    <button class="px-5 py-2.5 rounded-xl font-bold text-sm border border-slate-700 hover:border-indigo-500 hover:bg-indigo-500/5 text-slate-300 hover:text-indigo-400 active:scale-95 transition-all cursor-pointer select-none">
        Secondary Outline
    </button>

    <!-- Ghost Button -->
    <button class="px-5 py-2.5 rounded-xl font-bold text-sm text-slate-400 hover:text-white hover:bg-white/5 active:scale-95 transition-all cursor-pointer select-none">
        Ghost Link
    </button>

    <!-- Soft/Tonal Button -->
    <button class="px-5 py-2.5 rounded-xl font-bold text-sm bg-indigo-500/10 hover:bg-indigo-500/20 text-indigo-400 active:scale-95 transition-all cursor-pointer select-none">
        Soft Accent
    </button>

    <!-- Destructive Button -->
    <button class="px-5 py-2.5 rounded-xl font-bold text-sm bg-rose-600 hover:bg-rose-500 active:scale-95 text-white transition-all shadow-lg shadow-rose-600/20 cursor-pointer select-none">
        Delete Record
    </button>
</div>"""

    # 2. Tailles (Sizes)
    sizes_raw = """<div class="flex flex-wrap gap-4 items-center justify-center">
    <!-- Extra Small -->
    <button class="px-3 py-1.5 rounded-lg text-xs font-bold bg-slate-800 hover:bg-slate-700 text-slate-300 transition-all cursor-pointer select-none">
        XS Button
    </button>
    
    <!-- Small -->
    <button class="px-4 py-2 rounded-xl text-xs font-bold bg-indigo-600 hover:bg-indigo-500 text-white transition-all cursor-pointer select-none">
        Small Size
    </button>
    
    <!-- Medium (Default) -->
    <button class="px-5 py-2.5 rounded-xl text-sm font-bold bg-indigo-600 hover:bg-indigo-500 text-white transition-all cursor-pointer select-none">
        Default MD
    </button>
    
    <!-- Large -->
    <button class="px-6 py-3.5 rounded-xl text-base font-bold bg-indigo-600 hover:bg-indigo-500 text-white transition-all cursor-pointer select-none">
        Large LG
    </button>
    
    <!-- Extra Large -->
    <button class="px-8 py-4.5 rounded-2xl text-lg font-black bg-indigo-600 hover:bg-indigo-500 text-white transition-all cursor-pointer select-none shadow-xl shadow-indigo-600/10">
        Epic XL Size
    </button>
</div>"""

    # 3. Icon Buttons & Loading State
    loading_raw = """<div asok-state="{ isLoading: false }" class="flex flex-wrap gap-4 items-center justify-center">
    <!-- With Prefix Icon -->
    <button class="inline-flex items-center gap-2.5 px-5 py-2.5 rounded-xl font-bold text-sm bg-indigo-600 hover:bg-indigo-500 text-white transition-all cursor-pointer select-none">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4" /></svg>
        Create Workspace
    </button>

    <!-- With Suffix Icon -->
    <button class="inline-flex items-center gap-2.5 px-5 py-2.5 rounded-xl font-bold text-sm border border-slate-700 hover:border-slate-600 text-slate-300 transition-all cursor-pointer select-none">
        Next Step
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7" /></svg>
    </button>

    <!-- Icon Only -->
    <button class="w-10 h-10 rounded-xl flex items-center justify-center border border-slate-700 hover:bg-white/5 text-slate-400 hover:text-white transition-all cursor-pointer select-none">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
    </button>

    <!-- Async Loading Button -->
    <button asok-on:click="isLoading = !isLoading"
            class="inline-flex items-center gap-2.5 px-5 py-2.5 rounded-xl font-bold text-sm bg-indigo-600 hover:bg-indigo-500 text-white transition-all cursor-pointer select-none"
            asok-class="isLoading ? 'opacity-70 cursor-not-allowed' : ''">
        <svg asok-show="isLoading" class="w-4 h-4 animate-spin text-white" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span asok-text="isLoading ? 'Deploying...' : 'Simulate Load'"></span>
    </button>
</div>"""

    # 4. Button Groups
    groups_raw = """<div class="flex flex-col md:flex-row gap-6 items-center justify-center">
    <!-- Attached Button Group -->
    <div class="inline-flex rounded-xl overflow-hidden border border-slate-700 divide-x divide-slate-700 bg-slate-800">
        <button class="px-4 py-2.5 text-xs font-bold text-indigo-400 bg-indigo-500/10 cursor-pointer select-none">
            Day
        </button>
        <button class="px-4 py-2.5 text-xs font-bold text-slate-400 hover:text-white hover:bg-white/5 transition-colors cursor-pointer select-none">
            Week
        </button>
        <button class="px-4 py-2.5 text-xs font-bold text-slate-400 hover:text-white hover:bg-white/5 transition-colors cursor-pointer select-none">
            Month
        </button>
        <button class="px-4 py-2.5 text-xs font-bold text-slate-400 hover:text-white hover:bg-white/5 transition-colors cursor-pointer select-none">
            Year
        </button>
    </div>

    <!-- Dropdown Split Action -->
    <div asok-state="{ isOpen: false }" class="relative inline-flex items-stretch rounded-xl overflow-hidden shadow-lg shadow-indigo-600/10">
        <!-- Main Trigger -->
        <button class="px-5 py-2.5 text-sm font-bold bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 text-white transition-colors cursor-pointer select-none">
            Publish Post
        </button>
        <!-- Split separator -->
        <div class="w-px bg-indigo-700"></div>
        <!-- Dropdown trigger -->
        <button asok-on:click="isOpen = !isOpen"
                class="px-3 bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 text-white transition-colors cursor-pointer select-none">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 9l-7 7-7-7" /></svg>
        </button>

        <!-- Dropdown Menu Options -->
        <div asok-show="isOpen" asok-transition="slide-down 150 fade 150"
             class="absolute right-0 top-full mt-2 w-48 bg-slate-900 border border-slate-800 rounded-xl p-1.5 shadow-2xl z-20 text-left">
            <button asok-on:click="isOpen = false" class="w-full text-left px-3 py-2 rounded-lg text-xs font-bold text-slate-300 hover:text-white hover:bg-white/5 cursor-pointer">
                Draft Publication
            </button>
            <button asok-on:click="isOpen = false" class="w-full text-left px-3 py-2 rounded-lg text-xs font-bold text-slate-300 hover:text-white hover:bg-white/5 cursor-pointer">
                Schedule Publish...
            </button>
        </div>
    </div>
</div>"""

    formatter = HtmlFormatter(cssclass="codehilite", wrapcode=True)
    lexer = HtmlLexer()

    def highlight_code(code_str):
        return highlight(code_str, lexer, formatter)

    return request.stream("page.asok",
        variants_raw=variants_raw,
        variants_html=highlight_code(variants_raw),
        sizes_raw=sizes_raw,
        sizes_html=highlight_code(sizes_raw),
        loading_raw=loading_raw,
        loading_html=highlight_code(loading_raw),
        groups_raw=groups_raw,
        groups_html=highlight_code(groups_raw),
        seo_title="Interactive Buttons Component - Asok Framework",
        description="Copy-paste button variants, sizes, loading states, and dropdown split button groups for Asok applications."
    )
