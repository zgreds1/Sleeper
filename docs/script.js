document.addEventListener('DOMContentLoaded', () => {
    const teamSelector = document.getElementById('team-selector');
    const tradesContainer = document.getElementById('trades-container');

    // Add sorting controls
    const controlsDiv = document.querySelector('.controls');
    const sortSelect = document.createElement('select');
    sortSelect.id = 'sort-selector';
    sortSelect.innerHTML = `
        <option value="date-desc">Date (Newest)</option>
        <option value="date-asc">Date (Oldest)</option>
        <option value="value-desc">Net Value (High to Low)</option>
        <option value="value-asc">Net Value (Low to High)</option>
    `;
    sortSelect.style.marginLeft = '1rem';
    controlsDiv.appendChild(sortSelect);

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
    teamSelector.addEventListener('change', () => renderTrades());
    sortSelect.addEventListener('change', () => renderTrades());

    function renderTrades() {
        const team = teamSelector.value;
        const sortMode = sortSelect.value;

        tradesContainer.innerHTML = '';

        if (!team) {
            tradesContainer.innerHTML = `
                <div class="empty-state">
                    Select a team to view their trade history
                </div>
            `;
            return;
        }

        let teamTrades = TRADES_DATA.filter(trade => Object.prototype.hasOwnProperty.call(trade, team));

        if (teamTrades.length === 0) {
            tradesContainer.innerHTML = `
                <div class="empty-state">
                    No trades found for ${team}
                </div>
            `;
            return;
        }

        // Sorting Logic
        teamTrades.sort((a, b) => {
            if (sortMode === 'date-desc') {
                return (b.time_created || 0) - (a.time_created || 0);
            } else if (sortMode === 'date-asc') {
                return (a.time_created || 0) - (b.time_created || 0);
            } else {
                // Calculate net value for sorting
                const netA = calculateNetValue(a, team);
                const netB = calculateNetValue(b, team);
                if (sortMode === 'value-desc') {
                    return netB - netA;
                } else {
                    return netA - netB;
                }
            }
        });

        teamTrades.forEach(trade => {
            const card = createTradeCard(trade, team);
            tradesContainer.appendChild(card);
        });
    }

    function calculateNetValue(trade, myTeam) {
        const mySide = trade[myTeam];
        const receivedValue = (mySide.additions || []).reduce((sum, asset) => sum + (asset.value || 0), 0);
        const sentValue = (mySide.subtractions || []).reduce((sum, asset) => sum + (asset.value || 0), 0);
        return receivedValue - sentValue;
    }

    function createTradeCard(trade, myTeam) {
        const mySide = trade[myTeam];
        const partners = Object.keys(trade).filter(key => key !== myTeam && key !== 'time_created');

        const card = document.createElement('div');
        card.className = 'trade-card';

        // Calculate Values
        const receivedValue = (mySide.additions || []).reduce((sum, asset) => sum + (asset.value || 0), 0);
        const sentValue = (mySide.subtractions || []).reduce((sum, asset) => sum + (asset.value || 0), 0);
        const netValue = receivedValue - sentValue;

        // Net Value Display
        let netValueClass = 'neutral';
        let netValueSign = '';
        if (netValue > 0) {
            netValueClass = 'positive';
            netValueSign = '+';
        } else if (netValue < 0) {
            netValueClass = 'negative';
        }

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
            <div class="trade-header">
                ${dateHtml}
                <div class="net-value ${netValueClass}">
                    Net: ${netValueSign}${netValue.toLocaleString()}
                </div>
            </div>
            <div class="trade-content">
                <div class="trade-side">
                    <h3>Received <span class="side-value">(${receivedValue.toLocaleString()})</span></h3>
                    ${receivedHtml}
                </div>
                <div class="trade-arrow">
                    ⇄
                    <div style="font-size: 0.75rem; margin-top: 0.5rem;">vs ${partnersText}</div>
                </div>
                <div class="trade-side">
                    <h3>Sent <span class="side-value">(${sentValue.toLocaleString()})</span></h3>
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
                    text += ` <span class="asset-meta">(${asset.season} ${asset.round}.${slot})</span>`;
                }
            } else {
                // Pick
                const roundText = getOrdinal(asset.round);
                text = `${asset.season} ${roundText} round pick`;
                className += ' asset-pick';
            }

            // Value Badge
            const value = asset.value || 0;
            const valueHtml = `<span class="asset-value">${value.toLocaleString()}</span>`;

            return `<li class="${className}">
                <span class="asset-name">${text}</span>
                ${valueHtml}
            </li>`;
        }).join('');

        return `<ul class="asset-list">${items}</ul>`;
    }
});
