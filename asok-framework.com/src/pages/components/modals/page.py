from asok import Request
from pygments import highlight
from pygments.lexers import HtmlLexer
from pygments.formatters import HtmlFormatter

def render(request: Request):
    """
    Renders the interactive Modals & Drawers playground page.
    """
    # 1. Centered Modal
    modal_center_raw = """<div asok-state="{ isOpen: false }">
    <!-- Trigger Button -->
    <button asok-on:click="isOpen = true" class="px-5 py-2.5 rounded-xl font-bold text-sm bg-indigo-600 hover:bg-indigo-500 text-white transition-all shadow-lg shadow-indigo-600/10 cursor-pointer">
        Open Centered Modal
    </button>

    <!-- Modal Portal / Backdrop & Dialog -->
    <div asok-show="isOpen" class="fixed inset-0 flex items-center justify-center p-6 z-50">
        <!-- Backdrop with Fade Transition -->
        <div asok-on:click="isOpen = false" 
             asok-transition="fade 200" 
             class="fixed inset-0 bg-black/60 backdrop-blur-xs"></div>

        <!-- Dialog Box with Scale Transition -->
        <div asok-transition="scale 300 fade 200" 
             class="relative max-w-md w-full bg-slate-900 border border-slate-800 rounded-3xl p-8 shadow-2xl text-left z-10">
            <h3 class="text-xl font-bold text-white mb-3">Centered Dialog</h3>
            <p class="text-sm text-slate-400 mb-6 leading-relaxed">
                This modal uses the scale transition to emerge gracefully from the center of the viewport.
            </p>
            <div class="flex justify-end gap-3">
                <button asok-on:click="isOpen = false" 
                        class="px-4 py-2 rounded-xl text-xs font-bold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700/50 cursor-pointer">
                    Cancel
                </button>
                <button asok-on:click="isOpen = false" 
                        class="px-4 py-2 rounded-xl text-xs font-bold bg-indigo-600 hover:bg-indigo-500 text-white cursor-pointer">
                    Confirm
                </button>
            </div>
        </div>
    </div>
</div>"""

    # 2. Full Screen Modal
    modal_full_raw = """<div asok-state="{ isOpen: false }">
    <!-- Trigger Button -->
    <button asok-on:click="isOpen = true" class="px-5 py-2.5 rounded-xl font-bold text-sm bg-indigo-600 hover:bg-indigo-500 text-white transition-all shadow-lg shadow-indigo-600/10 cursor-pointer">
        Open Full Screen Modal
    </button>

    <!-- Full Screen Modal Portal with Slide-up Transition -->
    <div asok-show="isOpen" 
         asok-transition="slide-up 300 fade 200" 
         class="fixed inset-0 bg-slate-950 flex flex-col p-8 md:p-16 z-50 overflow-y-auto">
        <div class="max-w-3xl mx-auto w-full flex-1 flex flex-col justify-between">
            <div class="flex justify-between items-center mb-12">
                <span class="text-[10px] font-black uppercase tracking-widest text-indigo-400 font-mono">Full Screen Overlay</span>
                <button asok-on:click="isOpen = false" class="text-slate-400 hover:text-white text-3xl font-bold cursor-pointer">&times;</button>
            </div>
            
            <div class="space-y-6 text-left my-auto">
                <h2 class="text-4xl md:text-5xl font-black text-white tracking-tight">Full Page Dialog</h2>
                <p class="text-lg text-slate-400 leading-relaxed max-w-xl">
                    This modal covers the entire screen, utilizing a slide-up transition. Perfect for onboarding steps, document editors, or immersive media players.
                </p>
            </div>
            
            <div class="flex justify-end pt-12 border-t border-slate-900">
                <button asok-on:click="isOpen = false" 
                        class="px-6 py-3 rounded-xl font-bold text-sm bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700/50 cursor-pointer">
                    Get Started
                </button>
            </div>
        </div>
    </div>
</div>"""

    # 3. Left Drawer
    drawer_left_raw = """<div asok-state="{ isOpen: false }">
    <!-- Trigger Button -->
    <button asok-on:click="isOpen = true" class="px-5 py-2.5 rounded-xl font-bold text-sm bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700/50 cursor-pointer">
        Open Left Drawer
    </button>

    <!-- Drawer Portal -->
    <div asok-show="isOpen" class="fixed inset-0 overflow-hidden z-50">
        <!-- Backdrop with Fade Transition -->
        <div asok-on:click="isOpen = false" 
             asok-transition="fade 200" 
             class="absolute inset-0 bg-black/60 backdrop-blur-xs"></div>

        <!-- Left Drawer Box with Slide-Left Transition -->
        <div asok-transition="slide-left 300 fade 200" 
             class="absolute inset-y-0 left-0 max-w-sm w-full bg-slate-900 border-r border-slate-850 p-8 shadow-2xl flex flex-col z-10 text-left">
            <div class="flex justify-between items-center mb-8">
                <h3 class="text-xl font-bold text-white tracking-tight">Left Drawer</h3>
                <button asok-on:click="isOpen = false" class="text-slate-400 hover:text-white text-2xl font-bold cursor-pointer">&times;</button>
            </div>
            
            <p class="text-sm text-slate-400 leading-relaxed flex-1">
                Slides in from the left edge. Highly suited for side navigation systems, settings pages, or main application menus.
            </p>
            
            <button asok-on:click="isOpen = false" class="w-full py-2.5 rounded-xl font-bold text-sm bg-indigo-600 hover:bg-indigo-500 text-white cursor-pointer">
                Close Panel
            </button>
        </div>
    </div>
</div>"""

    # 4. Right Drawer
    drawer_right_raw = """<div asok-state="{ isOpen: false }">
    <!-- Trigger Button -->
    <button asok-on:click="isOpen = true" class="px-5 py-2.5 rounded-xl font-bold text-sm bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700/50 cursor-pointer">
        Open Right Drawer
    </button>

    <!-- Drawer Portal -->
    <div asok-show="isOpen" class="fixed inset-0 overflow-hidden z-50">
        <!-- Backdrop with Fade Transition -->
        <div asok-on:click="isOpen = false" 
             asok-transition="fade 200" 
             class="absolute inset-0 bg-black/60 backdrop-blur-xs"></div>

        <!-- Right Drawer Box with Slide-Right Transition -->
        <div asok-transition="slide-right 300 fade 200" 
             class="absolute inset-y-0 right-0 max-w-sm w-full bg-slate-900 border-l border-slate-850 p-8 shadow-2xl flex flex-col z-10 text-left">
            <div class="flex justify-between items-center mb-8">
                <h3 class="text-xl font-bold text-white tracking-tight">Right Drawer</h3>
                <button asok-on:click="isOpen = false" class="text-slate-400 hover:text-white text-2xl font-bold cursor-pointer">&times;</button>
            </div>
            
            <p class="text-sm text-slate-400 leading-relaxed flex-1">
                Slides in from the right edge. Commonly used for editing sideforms, list details, or settings overlays.
            </p>
            
            <button asok-on:click="isOpen = false" class="w-full py-2.5 rounded-xl font-bold text-sm bg-indigo-600 hover:bg-indigo-500 text-white cursor-pointer">
                Close Panel
            </button>
        </div>
    </div>
</div>"""

    # 5. Top Drawer
    drawer_top_raw = """<div asok-state="{ isOpen: false }">
    <!-- Trigger Button -->
    <button asok-on:click="isOpen = true" class="px-5 py-2.5 rounded-xl font-bold text-sm bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700/50 cursor-pointer">
        Open Top Drawer
    </button>

    <!-- Drawer Portal -->
    <div asok-show="isOpen" class="fixed inset-0 overflow-hidden z-50">
        <!-- Backdrop with Fade Transition -->
        <div asok-on:click="isOpen = false" 
             asok-transition="fade 200" 
             class="absolute inset-0 bg-black/60 backdrop-blur-xs"></div>

        <!-- Top Drawer Box with Slide-Down Transition -->
        <div asok-transition="slide-down 300 fade 200" 
             class="absolute inset-x-0 top-0 max-h-xs bg-slate-900 border-b border-slate-850 p-8 shadow-2xl flex flex-col z-10 text-left">
            <div class="flex justify-between items-center mb-6">
                <h3 class="text-xl font-bold text-white tracking-tight">Top Drawer Banner</h3>
                <button asok-on:click="isOpen = false" class="text-slate-400 hover:text-white text-2xl font-bold cursor-pointer">&times;</button>
            </div>
            
            <p class="text-sm text-slate-400 leading-relaxed mb-6">
                Slides down from the top edge. Best suited for global search drawers, warning notices, or navigation sub-panels.
            </p>
            
            <div class="flex justify-end">
                <button asok-on:click="isOpen = false" class="px-4 py-2 rounded-xl text-xs font-bold bg-indigo-600 hover:bg-indigo-500 text-white cursor-pointer">
                    Acknowledge
                </button>
            </div>
        </div>
    </div>
</div>"""

    # 6. Bottom Drawer
    drawer_bottom_raw = """<div asok-state="{ isOpen: false }">
    <!-- Trigger Button -->
    <button asok-on:click="isOpen = true" class="px-5 py-2.5 rounded-xl font-bold text-sm bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700/50 cursor-pointer">
        Open Bottom Drawer
    </button>

    <!-- Drawer Portal -->
    <div asok-show="isOpen" class="fixed inset-0 overflow-hidden z-50">
        <!-- Backdrop with Fade Transition -->
        <div asok-on:click="isOpen = false" 
             asok-transition="fade 200" 
             class="absolute inset-0 bg-black/60 backdrop-blur-xs"></div>

        <!-- Bottom Drawer Box with Slide-Up Transition -->
        <div asok-transition="slide-up 300 fade 200" 
             class="absolute inset-x-0 bottom-0 max-h-xs bg-slate-900 border-t border-slate-850 p-8 shadow-2xl flex flex-col z-10 text-left">
            <div class="flex justify-between items-center mb-6">
                <h3 class="text-xl font-bold text-white tracking-tight">Bottom Sheet</h3>
                <button asok-on:click="isOpen = false" class="text-slate-400 hover:text-white text-2xl font-bold cursor-pointer">&times;</button>
            </div>
            
            <p class="text-sm text-slate-400 leading-relaxed mb-6">
                Slides up from the bottom edge. Simulates a mobile bottom sheet, perfect for quick setting selections or options menus.
            </p>
            
            <div class="flex justify-end">
                <button asok-on:click="isOpen = false" class="px-4 py-2 rounded-xl text-xs font-bold bg-indigo-600 hover:bg-indigo-500 text-white cursor-pointer">
                    Dismiss
                </button>
            </div>
        </div>
    </div>
</div>"""

    # Syntax highlight utilizing Pygments codehilite structure
    formatter = HtmlFormatter(cssclass="codehilite", wrapcode=True)
    lexer = HtmlLexer()

    def highlight_code(code_str):
        return highlight(code_str, lexer, formatter)

    return request.stream("page.asok",
        modal_center_raw=modal_center_raw,
        modal_center_html=highlight_code(modal_center_raw),
        modal_full_raw=modal_full_raw,
        modal_full_html=highlight_code(modal_full_raw),
        drawer_left_raw=drawer_left_raw,
        drawer_left_html=highlight_code(drawer_left_raw),
        drawer_right_raw=drawer_right_raw,
        drawer_right_html=highlight_code(drawer_right_raw),
        drawer_top_raw=drawer_top_raw,
        drawer_top_html=highlight_code(drawer_top_raw),
        drawer_bottom_raw=drawer_bottom_raw,
        drawer_bottom_html=highlight_code(drawer_bottom_raw),
        seo_title="Interactive Modals & Drawers Component - Asok Framework",
        description="Copy-paste interactive Modals and Slide-over Drawers with animations powered by Asok transitions."
    )
