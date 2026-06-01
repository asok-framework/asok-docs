from asok import Request
from pygments import highlight
from pygments.lexers import HtmlLexer
from pygments.formatters import HtmlFormatter


def render(request: Request):
    """
    Renders the interactive Alerts & Toasts component playground page.
    """
    # 1. Toast Notification Stack
    toast_raw = """<div asok-state="{ toasts: [] }" class="w-full flex flex-col items-center gap-4">
    <!-- Trigger Buttons -->
    <div class="flex flex-wrap gap-3 justify-center">
        <button asok-on:click="toasts = toasts.concat({'id': Date.now(), 'type': 'success', 'msg': 'System database backup completed successfully.'})"
                class="px-5 py-2.5 rounded-xl font-bold text-xs bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/20 active:scale-95 transition-all cursor-pointer shadow-lg shadow-emerald-500/5">
            + Success Toast
        </button>
        <button asok-on:click="toasts = toasts.concat({'id': Date.now(), 'type': 'error', 'msg': 'Database connection lost. Reconnecting in 5s...'})"
                class="px-5 py-2.5 rounded-xl font-bold text-xs bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 border border-rose-500/20 active:scale-95 transition-all cursor-pointer shadow-lg shadow-rose-500/5">
            + Error Toast
        </button>
        <button asok-on:click="toasts = toasts.concat({'id': Date.now(), 'type': 'warning', 'msg': 'API usage limit is at 85% of monthly capacity.'})"
                class="px-5 py-2.5 rounded-xl font-bold text-xs bg-amber-500/10 hover:bg-amber-500/20 text-amber-400 border border-amber-500/20 active:scale-95 transition-all cursor-pointer shadow-lg shadow-amber-500/5">
            + Warning Toast
        </button>
        <button asok-on:click="toasts = toasts.concat({'id': Date.now(), 'type': 'info', 'msg': 'Deploying update v2.4.0-rc1 to staging.'})"
                class="px-5 py-2.5 rounded-xl font-bold text-xs bg-sky-500/10 hover:bg-sky-500/20 text-sky-400 border border-sky-500/20 active:scale-95 transition-all cursor-pointer shadow-lg shadow-sky-500/5">
            + Info Toast
        </button>
    </div>

    <!-- Active Toasts Counter -->
    <div class="text-xs text-slate-500 font-mono">
        Active toasts in stack: <span asok-text="toasts.length" class="font-bold text-indigo-400">0</span>
    </div>

    <!-- Portal Container for Stacked Toasts -->
    <div class="fixed bottom-6 right-6 z-50 flex flex-col gap-3 max-w-sm w-full pointer-events-none">
        <template asok-for="toast in toasts">
            <div asok-transition="slide-right 300 fade 200"
                 class="pointer-events-auto w-full flex items-start gap-3.5 p-4 rounded-2xl border shadow-2xl backdrop-blur-md transition-all duration-200"
                 asok-class="toast.type === 'success' ? 'bg-slate-900/90 border-emerald-500/20 text-slate-200' : toast.type === 'error' ? 'bg-slate-900/90 border-rose-500/20 text-slate-200' : toast.type === 'warning' ? 'bg-slate-900/90 border-amber-500/20 text-slate-200' : 'bg-slate-900/90 border-sky-500/20 text-slate-200'">
                
                <!-- Toast Left Colored Indicator Bar -->
                <div class="absolute left-0 top-0 bottom-0 w-1.5 rounded-l-2xl"
                     asok-class="toast.type === 'success' ? 'bg-emerald-500' : toast.type === 'error' ? 'bg-rose-500' : toast.type === 'warning' ? 'bg-amber-500' : 'bg-sky-500'">
                </div>

                <!-- Icons depending on type -->
                <div class="flex-shrink-0 mt-0.5"
                     asok-class="toast.type === 'success' ? 'text-emerald-400' : toast.type === 'error' ? 'text-rose-400' : toast.type === 'warning' ? 'text-amber-400' : 'text-sky-400'">
                    <span asok-show="toast.type === 'success'">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                    </span>
                    <span asok-show="toast.type === 'error'">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                    </span>
                    <span asok-show="toast.type === 'warning'">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
                    </span>
                    <span asok-show="toast.type === 'info'">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                    </span>
                </div>

                <!-- Message -->
                <div class="flex-1 text-sm font-medium pr-2 text-left" asok-text="toast.msg"></div>

                <!-- Close Button -->
                <button asok-on:click="toasts = toasts.filter(t => t.id !== toast.id)"
                        class="flex-shrink-0 text-slate-500 hover:text-slate-200 transition-colors cursor-pointer text-lg leading-none select-none">
                    &times;
                </button>
            </div>
        </template>
    </div>
</div>"""

    # 2. Inline Alerts
    inline_raw = """<div class="w-full max-w-lg mx-auto flex flex-col gap-3">
    <!-- Success Banner -->
    <div class="flex gap-3.5 p-4 rounded-2xl border bg-emerald-950/20 border-emerald-500/20 text-emerald-300">
        <svg class="w-5 h-5 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
        <div class="text-sm text-left">
            <span class="font-bold">Transaction processed!</span> Your subscription has been renewed and invoices sent to your billing email address.
        </div>
    </div>

    <!-- Error Banner -->
    <div class="flex gap-3.5 p-4 rounded-2xl border bg-rose-950/20 border-rose-500/20 text-rose-300">
        <svg class="w-5 h-5 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
        <div class="text-sm text-left">
            <span class="font-bold">Access Denied:</span> You do not have permission to execute this background task. Contact your admin for RBAC keys.
        </div>
    </div>

    <!-- Warning Banner -->
    <div class="flex gap-3.5 p-4 rounded-2xl border bg-amber-950/20 border-amber-500/20 text-amber-300">
        <svg class="w-5 h-5 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
        <div class="text-sm text-left">
            <span class="font-bold">Disk storage warning:</span> Local media assets storage is at 94% capacity. We recommend configuring an external S3 store.
        </div>
    </div>

    <!-- Info Banner -->
    <div class="flex gap-3.5 p-4 rounded-2xl border bg-sky-950/20 border-sky-500/20 text-sky-300">
        <svg class="w-5 h-5 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
        <div class="text-sm text-left">
            <span class="font-bold">Beta Feature:</span> Hot-swapping background workers is currently in developer preview. Report bugs in the repository.
        </div>
    </div>
</div>"""

    # 3. Dismissible Banners
    dismiss_raw = """<div asok-state="{ visible: true }" class="w-full max-w-lg mx-auto">
    <!-- Removable banner with fade-out transition -->
    <div asok-show="visible" asok-transition="fade 250"
         class="relative flex items-center justify-between gap-4 p-4 rounded-2xl border bg-slate-900 border-slate-800 text-slate-300">
        <div class="flex gap-3">
            <span class="text-lg">📢</span>
            <div class="text-sm text-left">
                <span class="font-bold text-white">We are upgrading!</span> Database migration v3 will occur tonight between 02:00 and 04:00 UTC. Expect short read latency.
            </div>
        </div>
        <button asok-on:click="visible = false"
                class="text-slate-500 hover:text-white transition-colors cursor-pointer text-xl leading-none select-none px-2">&times;</button>
    </div>

    <div asok-show="!visible" asok-transition="fade 200" class="py-6 text-center text-xs text-slate-500 font-medium">
        Banner dismissed. <button asok-on:click="visible = true" class="underline text-indigo-400 hover:text-indigo-300 transition-colors cursor-pointer">Restore notification</button>
    </div>
</div>"""

    formatter = HtmlFormatter(cssclass="codehilite", wrapcode=True)
    lexer = HtmlLexer()

    def highlight_code(code_str):
        return highlight(code_str, lexer, formatter)

    return request.stream("page.asok",
        toast_raw=toast_raw,
        toast_html=highlight_code(toast_raw),
        inline_raw=inline_raw,
        inline_html=highlight_code(inline_raw),
        dismiss_raw=dismiss_raw,
        dismiss_html=highlight_code(dismiss_raw),
        seo_title="Interactive Alerts & Toasts - Asok Framework",
        description="Copy-paste responsive inline alert banners and live stacked toast notification widgets built with Asok."
    )
