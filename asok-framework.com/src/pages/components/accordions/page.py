from asok import Request
from pygments import highlight
from pygments.lexers import HtmlLexer
from pygments.formatters import HtmlFormatter

def render(request: Request):
    """
    Renders the interactive Accordions component page.
    """
    # 1. Single Collapsible
    accordion_single_raw = """<div asok-state="{ isExpanded: false }" class="max-w-md w-full border border-slate-800 rounded-2xl overflow-hidden bg-slate-900 text-left">
    <!-- Trigger Header -->
    <button asok-on:click="isExpanded = !isExpanded" 
            class="w-full flex justify-between items-center p-5 font-bold text-sm text-white hover:bg-slate-850 transition-colors cursor-pointer">
        <span>What is Asok?</span>
        <svg class="w-4 h-4 transition-transform duration-200" 
             asok-class="isExpanded ? 'rotate-180 text-indigo-400' : 'text-slate-400'" 
             fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 9l-7 7-7-7" />
        </svg>
    </button>

    <!-- Content with slide transition -->
    <div asok-show="isExpanded" 
         asok-transition="slide-down 200 fade 150" 
         class="p-5 border-t border-slate-850 text-xs text-slate-400 leading-relaxed bg-slate-900/50">
        Asok is an ultra-lightweight, reactive, and streaming Python web framework. It focuses on zero external dependencies and built-in tooling for modern developer experiences.
    </div>
</div>"""

    # 2. Exclusive Group
    accordion_group_raw = """<div asok-state="{ activeIdx: 1 }" class="max-w-md w-full border border-slate-800 rounded-2xl overflow-hidden bg-slate-900 text-left space-y-px">
    <!-- Item 1 -->
    <div class="border-b border-slate-850">
        <button asok-on:click="activeIdx = activeIdx === 1 ? null : 1" 
                class="w-full flex justify-between items-center p-5 font-bold text-sm text-white hover:bg-slate-850 transition-colors cursor-pointer">
            <span>Features built-in</span>
            <svg class="w-4 h-4 transition-transform duration-200" 
                 asok-class="activeIdx === 1 ? 'rotate-180 text-indigo-400' : 'text-slate-400'" 
                 fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 9l-7 7-7-7" />
            </svg>
        </button>
        <div asok-show="activeIdx === 1" 
             asok-transition="slide-down 200 fade 150" 
             class="p-5 text-xs text-slate-400 leading-relaxed bg-slate-900/50">
            Asok includes a multi-engine ORM, secure authentication, Django-style admin, background workers, and real-time WebSocket templates out of the box.
        </div>
    </div>
    
    <!-- Item 2 -->
    <div class="border-b border-slate-850">
        <button asok-on:click="activeIdx = activeIdx === 2 ? null : 2" 
                class="w-full flex justify-between items-center p-5 font-bold text-sm text-white hover:bg-slate-850 transition-colors cursor-pointer">
            <span>Client reactivity without JS</span>
            <svg class="w-4 h-4 transition-transform duration-200" 
                 asok-class="activeIdx === 2 ? 'rotate-180 text-indigo-400' : 'text-slate-400'" 
                 fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 9l-7 7-7-7" />
            </svg>
        </button>
        <div asok-show="activeIdx === 2" 
             asok-transition="slide-down 200 fade 150" 
             class="p-5 text-xs text-slate-400 leading-relaxed bg-slate-900/50">
            Use Asok Directives (`asok-state`, `asok-on`, `asok-text`) to create rich client interactivity without writing a single line of JavaScript.
        </div>
    </div>
</div>"""

    formatter = HtmlFormatter(cssclass="codehilite", wrapcode=True)
    lexer = HtmlLexer()

    def highlight_code(code_str):
        return highlight(code_str, lexer, formatter)

    return request.stream("page.asok",
        accordion_single_raw=accordion_single_raw,
        accordion_single_html=highlight_code(accordion_single_raw),
        accordion_group_raw=accordion_group_raw,
        accordion_group_html=highlight_code(accordion_group_raw),
        seo_title="Interactive Accordions Component - Asok Framework",
        description="Copy-paste interactive Collapsible sections and Accordion groups with smooth slide animations."
    )
