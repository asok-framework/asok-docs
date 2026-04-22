const toggle = document.getElementById('theme-toggle');
const sunIcon = document.getElementById('sun-icon');
const moonIcon = document.getElementById('moon-icon');
const body = document.body;

function updateIcons() {
    const isLight = body.classList.contains('light-mode');
    sunIcon.style.display = isLight ? 'block' : 'none';
    moonIcon.style.display = isLight ? 'none' : 'block';
}

// Restore theme immediately to avoid flicker
if (localStorage.getItem('asok-theme') === 'light') {
    body.classList.add('light-mode');
}
updateIcons();

if (toggle) {
    toggle.addEventListener('click', () => {
        body.classList.toggle('light-mode');
        const isLight = body.classList.contains('light-mode');
        localStorage.setItem('asok-theme', isLight ? 'light' : 'dark');
        updateIcons();
    });
}

// Search Trigger (both desktop and mobile)
const searchTriggers = [document.getElementById('search-trigger'), document.getElementById('search-trigger-mobile')];
const searchOverlay = document.getElementById('search-overlay');
const searchInput = document.getElementById('search-input');

searchTriggers.forEach(trigger => {
    if (trigger) {
        trigger.addEventListener('click', () => {
            // Restore placeholder for a fresh start and consistent height
            const searchResults = document.getElementById('search-results');
            if (searchResults) {
                searchResults.innerHTML = `
                    <div class="search-empty">
                        <svg class="search-empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        <p>Type to search across all documentation</p>
                    </div>
                `;
            }
            if (searchInput) searchInput.value = '';
            
            searchOverlay.classList.add('open');
            setTimeout(() => searchInput && searchInput.focus(), 50);
        });
    }
});

// Close search overlay on background click
if (searchOverlay) {
    searchOverlay.addEventListener('click', (e) => {
        if (e.target === searchOverlay || e.target.closest('.search-hit')) {
            searchOverlay.classList.remove('open');
            if (searchInput) searchInput.value = '';
        }
    });
}

// Mobile Menu Toggle
const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
const mobileMenu = document.getElementById('mobile-menu');
const mobileMenuOverlay = document.getElementById('mobile-menu-overlay');
const menuIconPath = document.getElementById('menu-icon-path');

if (mobileMenuToggle && mobileMenu) {
    mobileMenuToggle.addEventListener('click', () => {
        const isHidden = mobileMenu.classList.contains('hidden');
        if (isHidden) {
            mobileMenu.classList.remove('hidden');
            if (menuIconPath) menuIconPath.setAttribute('d', 'M6 18L18 6M6 6l12 12');
            body.style.overflow = 'hidden';
        } else {
            mobileMenu.classList.add('hidden');
            if (menuIconPath) menuIconPath.setAttribute('d', 'M4 6h16M4 12h16M4 18h16');
            body.style.overflow = '';
        }
    });

    const mobileMenuClose = document.getElementById('mobile-menu-close');

    if (mobileMenuClose) {
        mobileMenuClose.addEventListener('click', () => {
            mobileMenu.classList.add('hidden');
            if (menuIconPath) menuIconPath.setAttribute('d', 'M4 6h16M4 12h16M4 18h16');
            body.style.overflow = '';
        });
    }

    // Close menu when clicking a link (using delegation for SPA compatibility)
    mobileMenu.addEventListener('click', (e) => {
        if (e.target.closest('a')) {
            mobileMenu.classList.add('hidden');
            if (menuIconPath) menuIconPath.setAttribute('d', 'M4 6h16M4 12h16M4 18h16');
            body.style.overflow = '';
        }
    });

    if (mobileMenuOverlay) {
        mobileMenuOverlay.addEventListener('click', () => {
            mobileMenu.classList.add('hidden');
            if (menuIconPath) menuIconPath.setAttribute('d', 'M4 6h16M4 12h16M4 18h16');
            body.style.overflow = '';
        });
    }
}

// Handle Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        if (searchOverlay.classList.contains('open')) {
            searchOverlay.classList.remove('open');
        }
        if (mobileMenu && !mobileMenu.classList.contains('hidden')) {
            mobileMenu.classList.add('hidden');
            if (menuIconPath) menuIconPath.setAttribute('d', 'M4 6h16M4 12h16M4 18h16');
            body.style.overflow = '';
        }
    }
});

// --- Asok SPA Enhancement ---
document.addEventListener('asok:success', (e) => {
    const target = e.detail.target;
    
    // Only close overlays if we are doing a main content swap
    // This prevents closing the search modal when search results are updated
    if (target && (target.id === 'main' || target.id === 'body')) {
        if (mobileMenu) mobileMenu.classList.add('hidden');
        if (searchOverlay) searchOverlay.classList.remove('open');
        if (menuIconPath) menuIconPath.setAttribute('d', 'M4 6h16M4 12h16M4 18h16');
        body.style.overflow = '';
        if (searchInput) searchInput.value = '';
    }
});