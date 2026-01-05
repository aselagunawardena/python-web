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

    // Close sidebar on link click
    document.querySelectorAll('.sidebar-menu a').forEach(link => {
        link.addEventListener('click', () => {
            sidebar.classList.remove('active');
            sidebarOverlay.classList.remove('active');
        });
    });

    // Search functionality
    const searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const searchTerm = searchInput.value;
            console.log('Search:', searchTerm);
            // Add your search logic here
        }
    });

    // Text display functionality
    document.getElementById('textInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && e.ctrlKey) {
            displayText();
        }
    });
});

async function displayText() {
    const textInput = document.getElementById('textInput').value;
    
    if (!textInput.trim()) {
        alert('Please type something!');
        return;
    }

    try {
        const response = await fetch('/api/display', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: textInput })
        });

        const data = await response.json();
        
        // Show the output section and display the text
        document.getElementById('outputSection').style.display = 'block';
        document.getElementById('displayBox').textContent = data.text;
    } catch (error) {
        console.error('Error:', error);
        alert('Something went wrong!');
    }
}
