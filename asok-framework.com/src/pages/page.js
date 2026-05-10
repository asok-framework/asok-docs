// Delegate events to document to support SPA navigation transitions
document.addEventListener('click', (e) => {
    // Playground tabs logic
    const tab = e.target.closest('.playground-tab');
    if (tab) {
        const targetTab = tab.dataset.tab;
        if (!targetTab) return;

        // Update tabs styling
        document.querySelectorAll('.playground-tab').forEach(t => {
            t.classList.remove('active', 'font-bold');
            t.classList.add('font-medium');
            t.style.background = 'transparent';
            t.style.color = 'var(--editor-tab-inactive)';
            t.style.border = '1px solid transparent';
        });

        tab.classList.add('active', 'font-bold');
        tab.classList.remove('font-medium');
        tab.style.background = 'var(--editor-tab-active-bg)';
        tab.style.color = 'var(--accent-primary)';
        tab.style.border = '1px solid var(--editor-tab-active-border)';

        // Update content visibility
        document.querySelectorAll('.playground-content').forEach(content => {
            content.classList.add('pg-hidden');
        });

        const targetContent = document.querySelector(`[data-content="${targetTab}"]`);
        if (targetContent) {
            targetContent.classList.remove('pg-hidden');
        }
        return;
    }

    // Pip copy logic
    const copyBtn = e.target.closest('#copy-pip-btn');
    if (copyBtn) {
        navigator.clipboard.writeText('pip install asok').then(() => {
            const copyIcon = copyBtn.querySelector('.copy-icon');
            const checkIcon = copyBtn.querySelector('.check-icon');

            if (copyIcon && checkIcon) {
                copyIcon.classList.add('pg-hidden');
                checkIcon.classList.remove('pg-hidden');
                
                setTimeout(() => {
                    copyIcon.classList.remove('pg-hidden');
                    checkIcon.classList.add('pg-hidden');
                }, 2000);
            }
        });
    }
});