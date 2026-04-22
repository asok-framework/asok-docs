// --- Global Utilities ---
window.addCopyButtons = () => {
    document.querySelectorAll('.codehilite').forEach(block => {
        if (block.querySelector('.copy-btn')) return;
        
        const button = document.createElement('button');
        button.className = 'copy-btn';
        button.setAttribute('aria-label', 'Copy code');
        button.innerHTML = `
            <svg width="14" height="14" fill="none" stroke="white" stroke-width="2.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
            </svg>
        `;
        
        button.addEventListener('click', async () => {
            const pre = block.querySelector('pre');
            if (!pre) return;
            const code = pre.innerText;
            await navigator.clipboard.writeText(code);
            
            button.innerHTML = `
                <svg width="14" height="14" fill="none" stroke="#818cf8" stroke-width="3" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"></path>
                </svg>
            `;
            button.classList.add('copied');
            
            setTimeout(() => {
                button.innerHTML = `
                    <svg width="14" height="14" fill="none" stroke="white" stroke-width="2.5" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                    </svg>
                `;
                button.classList.remove('copied');
            }, 2000);
        });
        
        block.appendChild(button);
    });
};

// --- Feedback Handler ---
window.initFeedback = () => {
    const yesBtn = document.getElementById('feedback-yes');
    const thanksMsg = document.getElementById('feedback-thanks');
    const feedbackBox = document.getElementById('feedback-box');

    if (yesBtn && thanksMsg) {
        yesBtn.addEventListener('click', () => {
            // Hide buttons and show thanks message
            feedbackBox.querySelector('.flex').style.display = 'none';
            feedbackBox.querySelector('p').style.display = 'none';
            thanksMsg.classList.remove('hidden');
        });
    }
};

// Handle SPA success events
document.addEventListener('asok:success', () => {
    window.addCopyButtons();
    setTimeout(window.addCopyButtons, 100);
    window.initTOC();
    setTimeout(window.initTOC, 100);
    window.initFeedback();
});

// --- Table of Contents Scroll Spy ---
window.initTOC = () => {
    const toc = document.getElementById('toc');
    if (!toc) return;

    const links = toc.querySelectorAll('.toc-link');
    if (links.length === 0) return;

    // Get all heading IDs from TOC links
    const headingIds = Array.from(links).map(link => link.getAttribute('href').substring(1));
    const headings = headingIds.map(id => document.getElementById(id)).filter(h => h);

    if (headings.length === 0) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            const id = entry.target.getAttribute('id');
            const tocLink = toc.querySelector(`a[href="#${id}"]`);

            if (entry.isIntersecting) {
                // Remove active from all
                links.forEach(l => l.classList.remove('active'));
                // Add active to current
                if (tocLink) {
                    tocLink.classList.add('active');
                }
            }
        });
    }, {
        rootMargin: '-80px 0px -80% 0px',
        threshold: 0
    });

    headings.forEach(heading => observer.observe(heading));

    // Smooth scroll when clicking TOC links
    links.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1);
            const target = document.getElementById(targetId);
            if (target) {
                const offset = 80; // Account for sticky header
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - offset;
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
                // Update URL without scrolling
                history.replaceState(null, null, `#${targetId}`);
            }
        });
    });
};

document.addEventListener('DOMContentLoaded', () => {
    // Initialize copy buttons
    window.addCopyButtons();

    // Initialize TOC scroll spy
    window.initTOC();

    // Initialize feedback
    window.initFeedback();
    
    // Auto-initialize when DOM changes (for SPA support)
    const observer = new MutationObserver((mutations) => {
        // Debounce or at least check if we really need to run
        window.addCopyButtons();
    });
    
    if (document.body) {
        observer.observe(document.body, { childList: true, subtree: true });
    }

    // --- Search Command Palette ---
    const overlay = document.getElementById('search-overlay');
    const searchInput = document.getElementById('search-input');
    const trigger = document.getElementById('search-trigger');
    const resultsBox = document.getElementById('search-results');

    if (overlay && searchInput) {
        const open = () => {
            overlay.classList.add('open');
            setTimeout(() => searchInput.focus(), 50);
        };
        const close = () => {
            overlay.classList.remove('open');
            searchInput.blur();
        };

        if (trigger) trigger.addEventListener('click', open);

        // Keyboard nav inside results
        let activeIdx = -1;
        const getItems = () => resultsBox.querySelectorAll('a.search-hit');
        const highlight = (idx) => {
            const items = getItems();
            items.forEach(el => el.classList.remove('active'));
            if (idx >= 0 && idx < items.length) {
                items[idx].classList.add('active');
                items[idx].scrollIntoView({ block: 'nearest' });
            }
        };

        const obs = new MutationObserver(() => { activeIdx = -1; });
        obs.observe(resultsBox, { childList: true, subtree: true });

        document.addEventListener('keydown', (e) => {
            if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
                e.preventDefault();
                overlay.classList.contains('open') ? close() : open();
            }
            if (!overlay.classList.contains('open')) return;

            if (e.key === 'Escape') { close(); return; }

            const items = getItems();
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                activeIdx = Math.min(activeIdx + 1, items.length - 1);
                highlight(activeIdx);
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                activeIdx = Math.max(activeIdx - 1, 0);
                highlight(activeIdx);
            } else if (e.key === 'Enter' && activeIdx >= 0 && activeIdx < items.length) {
                e.preventDefault();
                items[activeIdx].click();
            }
        });

        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) close();
        });
    }
});
