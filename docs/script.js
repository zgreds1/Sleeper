document.addEventListener('DOMContentLoaded', () => {
    const teamSelector = document.getElementById('team-selector');
    const tradesContainer = document.getElementById('trades-container');

    // 1. Extract unique teams
    const teams = new Set();
    TRADES_DATA.forEach(trade => {
        Object.keys(trade).forEach(key => {
            if (key !== 'time_created') {
                teams.add(key);
            }
        });
    });

    // 2. Populate selector
    const sortedTeams = Array.from(teams).sort((a, b) => a.localeCompare(b));
    sortedTeams.forEach(team => {
        const option = document.createElement('option');
        option.value = team;
        option.textContent = team;
        teamSelector.appendChild(option);
    });

    // 3. Handle selection
    teamSelector.addEventListener('change', (e) => {
        const selectedTeam = e.target.value;
        renderTrades(selectedTeam);
    });

    function renderTrades(team) {
        tradesContainer.innerHTML = '';

        if (!team) {
            tradesContainer.innerHTML = `
                <div class="empty-state">
                    Select a team to view their trade history
                </div>
            `;
            return;
        }

        const teamTrades = TRADES_DATA.filter(trade => Object.prototype.hasOwnProperty.call(trade, team));

        if (teamTrades.length === 0) {
            tradesContainer.innerHTML = `
                <div class="empty-state">
                    No trades found for ${team}
                </div>
            `;
            return;
        }

        // Sort trades by date (newest first) if time_created exists
        teamTrades.sort((a, b) => (b.time_created || 0) - (a.time_created || 0));

        teamTrades.forEach(trade => {
            const card = createTradeCard(trade, team);
            tradesContainer.appendChild(card);
        });
    }

    function createTradeCard(trade, myTeam) {
        const mySide = trade[myTeam];
        const partners = Object.keys(trade).filter(key => key !== myTeam && key !== 'time_created');

        const card = document.createElement('div');
        card.className = 'trade-card';

        // Date formatting
        let dateHtml = '';
        if (trade.time_created) {
            const date = new Date(trade.time_created);
            dateHtml = `<div class="trade-date">${date.toLocaleDateString()} ${date.toLocaleTimeString()}</div>`;
        }

        // Received Column
        const receivedHtml = renderAssetList(mySide.additions);

        // Sent Column
        const sentHtml = renderAssetList(mySide.subtractions);

        const partnersText = partners.join(', ');

        card.innerHTML = `
            ${dateHtml}
            <div class="trade-content">
                <div class="trade-side">
                    <h3>Received</h3>
                    ${receivedHtml}
                </div>
                <div class="trade-arrow">
                    ⇄
                    <div style="font-size: 0.75rem; margin-top: 0.5rem;">vs ${partnersText}</div>
                </div>
                <div class="trade-side">
                    <h3>Sent</h3>
                    ${sentHtml}
                </div>
            </div>
        `;

        return card;
    }

    function getOrdinal(n) {
        const s = ["th", "st", "nd", "rd"];
        const v = n % 100;
        return n + (s[(v - 20) % 10] || s[v] || s[0]);
    }

    function renderAssetList(assets) {
        if (!assets || assets.length === 0) {
            return '<div class="asset-list"><span class="asset-item" style="color: var(--text-secondary); font-style: italic;">Nothing</span></div>';
        }

        const items = assets.map(asset => {
            let text = '';
            let className = 'asset-item';

            if (asset.name) {
                // Player
                text = asset.name;
                className += ' asset-player';

                // Check if player was originally a draft pick
                if (asset.season && asset.round && asset.slot) {
                    const slot = asset.slot.toString().padStart(2, '0');
                    text += ` (${asset.season} ${asset.round}.${slot})`;
                }
            } else {
                // Pick
                // Format: 2028 2nd round pick
                // Or if slot is present? The user example for pure pick was:
                // { "id": "", "round": 2, "slot": "", "season": "2028" } -> 2028 2nd round pick

                const roundText = getOrdinal(asset.round);
                text = `${asset.season} ${roundText} round pick`;

                if (asset.slot) {
                    // If slot is present in a pure pick, maybe show it? 
                    // User didn't specify, but usually picks with slots are specific.
                    // Let's stick to the requested format for general picks, 
                    // but if slot exists, maybe append it? 
                    // "2025 4.10" style is for players. 
                    // Let's just use the requested format "2028 2nd round pick" for now.
                    // If slot is there, maybe "2025 4th round pick (4.10)"?
                    // Let's keep it simple as requested: "2028 2nd round pick"
                    // But wait, if it has a slot, it's a specific pick.
                    // The user example for player was "Dillon Gabriel (2025 4.10)".
                    // The user example for pick was "2028 2nd round pick".
                    // I will stick to "Season Round-ordinal round pick".
                }

                className += ' asset-pick';
            }

            return `<li class="${className}">${text}</li>`;
        }).join('');

        return `<ul class="asset-list">${items}</ul>`;
    }
});
