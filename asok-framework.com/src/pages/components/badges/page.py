from asok import Request
from pygments import highlight
from pygments.lexers import HtmlLexer
from pygments.formatters import HtmlFormatter


def render(request: Request):
    """
    Renders the interactive Badges & Chips component playground page.
    """
    # 1. Status Badges
    status_raw = """<div class="flex flex-wrap gap-3 items-center justify-center">
    <!-- Active Status -->
    <span class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-bold uppercase tracking-wider bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
        Active
    </span>
    
    <!-- Offline Status -->
    <span class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-bold uppercase tracking-wider bg-rose-500/10 text-rose-400 border border-rose-500/20">
        <span class="w-1.5 h-1.5 rounded-full bg-rose-400"></span>
        Offline
    </span>
    
    <!-- Pending Status -->
    <span class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-bold uppercase tracking-wider bg-amber-500/10 text-amber-400 border border-amber-500/20">
        <span class="w-1.5 h-1.5 rounded-full bg-amber-400 animate-pulse"></span>
        Pending
    </span>
    
    <!-- Beta Status -->
    <span class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-bold uppercase tracking-wider bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
        <span class="w-1.5 h-1.5 rounded-full bg-indigo-400"></span>
        Beta
    </span>
</div>"""

    # 2. Removable Chips
    chips_raw = """<div asok-state="{ tags: ['Python', 'Async', 'WebSockets', 'ORM', 'GraphQL'] }" class="w-full flex flex-col items-center gap-4">
    <!-- Active Tags List -->
    <div class="flex flex-wrap gap-2 justify-center">
        <template asok-for="tag in tags">
            <span class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-bold bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 transition-all">
                <span asok-text="tag"></span>
                <button asok-on:click="tags = tags.filter(t => t !== tag)"
                        class="w-4 h-4 flex items-center justify-center rounded-full hover:bg-indigo-500/30 text-indigo-400 hover:text-white transition-colors cursor-pointer font-bold text-xs select-none">
                    &times;
                </button>
            </span>
        </template>
    </div>

    <!-- Empty State -->
    <div asok-show="tags.length === 0" asok-transition="fade 200" class="text-sm text-slate-500">
        No tags remaining. <button asok-on:click="tags = ['Python', 'Async', 'WebSockets', 'ORM', 'GraphQL']" class="underline text-indigo-400 hover:text-indigo-300 transition-colors cursor-pointer select-none">Reset tags list</button>
    </div>
</div>"""

    # 3. Notification Count Badges
    count_raw = """<div class="flex flex-wrap gap-8 items-center justify-center">
    <!-- Icon Notification Badge -->
    <button class="relative inline-flex items-center gap-2 px-4 py-2.5 rounded-xl font-bold text-sm border border-slate-700 text-slate-300 hover:bg-white/5 transition-all cursor-pointer select-none">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" /></svg>
        Inbox Messages
        <span class="absolute -top-1.5 -right-1.5 w-5 h-5 rounded-full bg-rose-600 text-white text-[10px] font-black flex items-center justify-center shadow-lg shadow-rose-600/20 animate-bounce">
            5
        </span>
    </button>

    <!-- Count Labels -->
    <div class="flex items-center gap-3">
        <span class="text-xs font-bold text-slate-400">Resolved Pull Requests</span>
        <span class="px-2.5 py-0.5 rounded-full text-xs font-black bg-emerald-500/15 text-emerald-400 border border-emerald-500/20">
            28
        </span>
    </div>
    <div class="flex items-center gap-3">
        <span class="text-xs font-bold text-slate-400">Open Bug Reports</span>
        <span class="px-2.5 py-0.5 rounded-full text-xs font-black bg-rose-500/15 text-rose-400 border border-rose-500/20">
            14
        </span>
    </div>
</div>"""

    # 4. Tech & Version Badges
    version_raw = """<div class="flex flex-wrap gap-3 items-center justify-center">
    <!-- Version Pill -->
    <span class="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-bold font-mono bg-slate-800 text-slate-200 border border-slate-700">
        <svg class="w-3.5 h-3.5 text-yellow-500" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0L1.608 6v12L12 24l10.392-6V6z" /></svg>
        v0.3.0
    </span>
    
    <!-- Environment Pill -->
    <span class="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-bold font-mono bg-indigo-950/40 text-indigo-300 border border-indigo-500/20">
        Python 3.12+
    </span>
    
    <!-- License Pill -->
    <span class="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-bold font-mono bg-emerald-950/40 text-emerald-300 border border-emerald-500/20">
        MIT License
    </span>
    
    <!-- Star Counter -->
    <span class="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-bold font-mono bg-slate-800 text-slate-200 border border-slate-700">
        ⭐ 4.8k stars
    </span>
</div>"""

    formatter = HtmlFormatter(cssclass="codehilite", wrapcode=True)
    lexer = HtmlLexer()

    def highlight_code(code_str):
        return highlight(code_str, lexer, formatter)

    return request.stream("page.asok",
        status_raw=status_raw,
        status_html=highlight_code(status_raw),
        chips_raw=chips_raw,
        chips_html=highlight_code(chips_raw),
        count_raw=count_raw,
        count_html=highlight_code(count_raw),
        version_raw=version_raw,
        version_html=highlight_code(version_raw),
        seo_title="Interactive Badges & Chips - Asok Framework",
        description="Copy-paste responsive status badges, tag chips, notification counters, and repository version badges."
    )
