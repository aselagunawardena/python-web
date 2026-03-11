// Fetch and display games from API
async function loadGames() {
    try {
        const response = await fetch('/api/games');
        const data = await response.json();
        
        if (data.games && data.games.length > 0) {
            const gamesContainer = document.querySelector('.games-grid');
            gamesContainer.innerHTML = '';
            
            data.games.forEach(game => {
                const card = createGameCard(game);
                gamesContainer.appendChild(card);
            });
        }
    } catch (error) {
        console.error('Error loading games:', error);
    }
}

// Create a game card element
function createGameCard(game) {
    const card = document.createElement('div');
    card.className = 'game-card';
    card.innerHTML = `
        <div class="game-rank">${game.rank}</div>
        <img src="${game.image || 'https://via.placeholder.com/150x200?text=No+Image'}" alt="${game.title}">
        <h3>${game.title}</h3>
        <p>${game.description}</p>
    `;
    return card;
}

// Load data when page loads
document.addEventListener('DOMContentLoaded', () => {
    loadGames();
});
