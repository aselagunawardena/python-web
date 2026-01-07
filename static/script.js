// Navbar menu toggle
document.addEventListener('DOMContentLoaded', () => {
    const hamburgerBtn = document.getElementById('hamburgerBtn');
    const closeBtn = document.getElementById('closeBtn');
    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.getElementById('sidebarOverlay');

    hamburgerBtn.addEventListener('click', () => {
        sidebar.classList.add('active');
        sidebarOverlay.classList.add('active');
    });

    closeBtn.addEventListener('click', () => {
        sidebar.classList.remove('active');
        sidebarOverlay.classList.remove('active');
    });

    sidebarOverlay.addEventListener('click', () => {
        sidebar.classList.remove('active');
        sidebarOverlay.classList.remove('active');
    });

    // Sidebar link behavior
    const settingsPanel = document.getElementById('settingsPanel');
    document.querySelectorAll('.sidebar-menu a').forEach(link => {
        if (link.id === 'settingsLink') {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                // Toggle settings panel inside sidebar
                settingsPanel.classList.toggle('open');
            });
        } else {
            link.addEventListener('click', () => {
                sidebar.classList.remove('active');
                sidebarOverlay.classList.remove('active');
                // ensure settings panel is closed when navigating
                if (settingsPanel) settingsPanel.classList.remove('open');
            });
        }
    });

    // Background selection and persistence
    const BG_KEY = 'selectedBg';
    const bgRadios = document.querySelectorAll('.settings-panel input[name="bg"]');
    function applyBgClass(cls) {
        document.body.classList.remove('bg-default','bg-night','bg-forest','bg-sunset','bg-solid');
        if (cls) document.body.classList.add(cls);
    }
    // initialize from localStorage
    const saved = localStorage.getItem(BG_KEY) || 'bg-default';
    applyBgClass(saved);
    if (bgRadios) {
        bgRadios.forEach(r => {
            if (r.value === saved) r.checked = true;
            r.addEventListener('change', (e) => {
                const val = e.target.value;
                applyBgClass(val);
                localStorage.setItem(BG_KEY, val);
            });
        });
    }

    // Search functionality
    const searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const searchTerm = searchInput.value;
            console.log('Search:', searchTerm);
            // Add your search logic here
        }
    });

    // Text display removed
});

// displayText removed
