from asok import Request
from pygments import highlight
from pygments.lexers import HtmlLexer
from pygments.formatters import HtmlFormatter

def render(request: Request):
    """
    Renders the interactive Tabs component page.
    """
    # 1. Horizontal Tabs
    tabs_horizontal_raw = """<div asok-state="{ activeTab: 'account' }" class="max-w-md w-full border border-slate-800 rounded-2xl p-6 bg-slate-900 text-left">
    <!-- Tab Buttons -->
    <div class="flex gap-2 border-b border-slate-800 pb-3 mb-6">
        <button asok-on:click="activeTab = 'account'" 
                class="px-4 py-2 text-xs font-bold rounded-lg border transition-all cursor-pointer"
                asok-class="activeTab === 'account' ? 'bg-indigo-500/10 border-indigo-500/20 text-indigo-400' : 'bg-transparent border-transparent text-slate-400 hover:text-white'">
            Account
        </button>
        <button asok-on:click="activeTab = 'security'" 
                class="px-4 py-2 text-xs font-bold rounded-lg border transition-all cursor-pointer"
                asok-class="activeTab === 'security' ? 'bg-indigo-500/10 border-indigo-500/20 text-indigo-400' : 'bg-transparent border-transparent text-slate-400 hover:text-white'">
            Security
        </button>
    </div>
    
    <!-- Tab Panels -->
    <div asok-show="activeTab === 'account'" asok-transition="fade 150" class="text-sm text-slate-400 leading-relaxed">
        <h4 class="font-bold text-white mb-2 text-xs uppercase tracking-wider">Account Settings</h4>
        <p>Update your public profile, email address, avatar, and other profile configuration parameters here.</p>
    </div>
    
    <div asok-show="activeTab === 'security'" asok-transition="fade 150" class="text-sm text-slate-400 leading-relaxed">
        <h4 class="font-bold text-white mb-2 text-xs uppercase tracking-wider">Security Access</h4>
        <p>Manage your passwords, active sessions, double-authentication mechanisms, and API personal access tokens.</p>
    </div>
</div>"""

    # 2. Vertical Tabs
    tabs_vertical_raw = """<div asok-state="{ activeTab: 'general' }" class="max-w-lg w-full border border-slate-800 rounded-2xl p-6 bg-slate-900 text-left grid grid-cols-1 md:grid-cols-[140px_1fr] gap-6">
    <!-- Tab List -->
    <div class="flex flex-col gap-1 border-r border-slate-800 pr-4">
        <button asok-on:click="activeTab = 'general'" 
                class="w-full text-left px-3 py-2 text-xs font-bold rounded-lg border transition-all cursor-pointer"
                asok-class="activeTab === 'general' ? 'bg-indigo-500/10 border-indigo-500/20 text-indigo-400' : 'bg-transparent border-transparent text-slate-400 hover:text-white'">
            General
        </button>
        <button asok-on:click="activeTab = 'advanced'" 
                class="w-full text-left px-3 py-2 text-xs font-bold rounded-lg border transition-all cursor-pointer"
                asok-class="activeTab === 'advanced' ? 'bg-indigo-500/10 border-indigo-500/20 text-indigo-400' : 'bg-transparent border-transparent text-slate-400 hover:text-white'">
            Advanced
        </button>
    </div>
    
    <!-- Tab Panels -->
    <div class="min-h-[100px]">
        <div asok-show="activeTab === 'general'" asok-transition="fade 150" class="text-sm text-slate-400 leading-relaxed">
            <h4 class="font-bold text-white mb-2 text-xs uppercase tracking-wider">General Configurations</h4>
            <p>Define your primary project properties, repository name, base URL, and active deployment targets.</p>
        </div>
        
        <div asok-show="activeTab === 'advanced'" asok-transition="fade 150" class="text-sm text-slate-400 leading-relaxed">
            <h4 class="font-bold text-white mb-2 text-xs uppercase tracking-wider">Advanced Tweak Parameters</h4>
            <p>Access CORS policies, cache lifetime duration keys, thread workers allocation, and raw SQL connection strings.</p>
        </div>
    </div>
</div>"""

    formatter = HtmlFormatter(cssclass="codehilite", wrapcode=True)
    lexer = HtmlLexer()

    def highlight_code(code_str):
        return highlight(code_str, lexer, formatter)

    return request.stream("page.asok",
        tabs_horizontal_raw=tabs_horizontal_raw,
        tabs_horizontal_html=highlight_code(tabs_horizontal_raw),
        tabs_vertical_raw=tabs_vertical_raw,
        tabs_vertical_html=highlight_code(tabs_vertical_raw),
        seo_title="Interactive Tabs Component - Asok Framework",
        description="Copy-paste interactive horizontal and vertical tabs navigation components with fade transitions."
    )
