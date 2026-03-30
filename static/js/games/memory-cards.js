/**
 * Game: Memory Cards (Lật thẻ ghi nhớ)
 * Flip cards to match word with image pairs
 */

let memoryState = {
    cards: [],
    flipped: [],
    matched: 0,
    moves: 0,
    totalPairs: 0,
    locked: false
};

function startGame() {
    const topicId = document.getElementById('topic-select').value;
    const allWords = getWordsByTopic(TOPICS_DATA, topicId);

    if (allWords.length < 3) {
        alert('Cần ít nhất 3 từ để chơi!');
        return;
    }

    // Select words (max 6 pairs = 12 cards)
    const selectedWords = shuffle(allWords).slice(0, 6);

    // Create card pairs: one image card + one word card per word
    const cards = [];
    selectedWords.forEach((w, i) => {
        cards.push({
            id: `img-${i}`,
            pairId: i,
            type: 'image',
            image: w.image,
            word: w.word
        });
        cards.push({
            id: `word-${i}`,
            pairId: i,
            type: 'word',
            word: w.word,
            meaning: w.meaning
        });
    });

    memoryState = {
        cards: shuffle(cards),
        flipped: [],
        matched: 0,
        moves: 0,
        totalPairs: selectedWords.length,
        locked: false
    };

    document.getElementById('score-bar').style.display = 'flex';
    document.getElementById('result-area').style.display = 'none';
    document.getElementById('start-btn').style.display = 'none';
    renderMemoryBoard();
    updateMemoryScore();
}

function renderMemoryBoard() {
    const area = document.getElementById('game-area');
    const cols = memoryState.cards.length <= 8 ? 4 : 4;

    let html = `
        <div class="memory-stats" id="memory-stats"></div>
        <div class="memory-grid" style="grid-template-columns: repeat(${cols}, 1fr);">`;

    memoryState.cards.forEach((card, idx) => {
        let backContent = '';
        if (card.type === 'image') {
            backContent = `<img src="${escapeHtml(card.image)}" alt="?" loading="lazy">`;
        } else {
            backContent = `<span class="card-word">${escapeHtml(card.word)}</span>
                          <small style="color:var(--text-light);display:block;margin-top:4px">${escapeHtml(card.meaning)}</small>`;
        }

        html += `
            <div class="memory-card" id="card-${idx}" onclick="flipCard(${idx})">
                <div class="memory-card-inner">
                    <div class="memory-card-front">❓</div>
                    <div class="memory-card-back">${backContent}</div>
                </div>
            </div>`;
    });

    html += '</div>';
    area.innerHTML = html;
}

function flipCard(idx) {
    if (memoryState.locked) return;
    const card = memoryState.cards[idx];
    const el = document.getElementById(`card-${idx}`);

    // Can't flip already flipped or matched cards
    if (el.classList.contains('flipped') || el.classList.contains('matched')) return;

    el.classList.add('flipped');
    memoryState.flipped.push(idx);

    if (memoryState.flipped.length === 2) {
        memoryState.moves++;
        memoryState.locked = true;

        const [first, second] = memoryState.flipped;
        const card1 = memoryState.cards[first];
        const card2 = memoryState.cards[second];

        if (card1.pairId === card2.pairId && card1.type !== card2.type) {
            // Match!
            setTimeout(() => {
                document.getElementById(`card-${first}`).classList.add('matched');
                document.getElementById(`card-${second}`).classList.add('matched');
                memoryState.matched++;
                memoryState.flipped = [];
                memoryState.locked = false;
                updateMemoryScore();
                speak(card1.word);

                if (memoryState.matched === memoryState.totalPairs) {
                    setTimeout(showMemoryResult, 600);
                }
            }, 500);
        } else {
            // No match - flip back
            setTimeout(() => {
                document.getElementById(`card-${first}`).classList.remove('flipped');
                document.getElementById(`card-${second}`).classList.remove('flipped');
                memoryState.flipped = [];
                memoryState.locked = false;
                updateMemoryScore();
            }, 1000);
        }
    }
}

function updateMemoryScore() {
    const statsEl = document.getElementById('memory-stats');
    if (statsEl) {
        statsEl.textContent = `Đã ghép: ${memoryState.matched}/${memoryState.totalPairs} | Lượt lật: ${memoryState.moves}`;
    }
    document.getElementById('score-text').textContent = `Ghép: ${memoryState.matched}/${memoryState.totalPairs}`;
    document.getElementById('progress-text').textContent = `Lượt: ${memoryState.moves}`;
    const pct = memoryState.totalPairs > 0 ? (memoryState.matched / memoryState.totalPairs) * 100 : 0;
    document.getElementById('progress-fill').style.width = pct + '%';
}

function showMemoryResult() {
    document.getElementById('game-area').innerHTML = '';
    document.getElementById('start-btn').style.display = 'inline-block';

    const resultArea = document.getElementById('result-area');
    resultArea.style.display = 'block';

    // Score based on efficiency (fewer moves = better)
    const minMoves = memoryState.totalPairs; // Perfect would be pairs count
    const maxReasonable = memoryState.totalPairs * 3;
    const efficiency = Math.max(0, 1 - (memoryState.moves - minMoves) / maxReasonable);
    const stars = efficiency >= 0.7 ? '⭐⭐⭐' : efficiency >= 0.4 ? '⭐⭐' : '⭐';

    document.getElementById('result-title').textContent = '🎉 Hoàn thành!';
    document.getElementById('result-score').textContent =
        `Ghép ${memoryState.totalPairs} cặp trong ${memoryState.moves} lượt`;
    document.getElementById('result-stars').textContent = stars;
    document.getElementById('progress-fill').style.width = '100%';
}

// Override nextQuestion for memory (not used, but prevents error)
function nextQuestion() {}
