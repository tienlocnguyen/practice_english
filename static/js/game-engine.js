/**
 * Game Engine - common game state and UI management
 */

let gameState = {
    words: [],
    currentIndex: 0,
    score: 0,
    total: 0,
    isPlaying: false
};

function initTopicSelector() {
    const select = document.getElementById('topic-select');
    if (!select) return;
    for (const topic of TOPICS_DATA) {
        const opt = document.createElement('option');
        opt.value = topic.id;
        opt.textContent = `${topic.icon} ${topic.name_vi}`;
        select.appendChild(opt);
    }
}

function loadTopic() {
    // Reset state when topic changes
    resetGameState();
}

function resetGameState() {
    gameState = {
        words: [],
        currentIndex: 0,
        score: 0,
        total: 0,
        isPlaying: false
    };
    document.getElementById('score-bar').style.display = 'none';
    document.getElementById('result-area').style.display = 'none';
    document.getElementById('next-btn').style.display = 'none';
    document.getElementById('game-area').innerHTML =
        '<p class="game-placeholder">Chọn chủ đề và nhấn "Bắt đầu" để chơi!</p>';
}

function startGame() {
    const topicId = document.getElementById('topic-select').value;
    const allWords = getWordsByTopic(TOPICS_DATA, topicId);

    if (allWords.length < 2) {
        alert('Cần ít nhất 2 từ để chơi!');
        return;
    }

    gameState.words = shuffle(allWords);
    gameState.currentIndex = 0;
    gameState.score = 0;
    gameState.total = Math.min(gameState.words.length, 10); // Max 10 questions
    gameState.isPlaying = true;

    document.getElementById('score-bar').style.display = 'flex';
    document.getElementById('result-area').style.display = 'none';
    document.getElementById('start-btn').style.display = 'none';
    updateScoreBar();

    // Call game-specific init
    if (typeof initGameRound === 'function') {
        initGameRound();
    }
}

function updateScoreBar() {
    document.getElementById('score-text').textContent = `Điểm: ${gameState.score}`;
    document.getElementById('progress-text').textContent =
        `Câu: ${gameState.currentIndex + 1}/${gameState.total}`;
    const pct = ((gameState.currentIndex) / gameState.total) * 100;
    document.getElementById('progress-fill').style.width = pct + '%';
}

function onCorrectAnswer() {
    gameState.score++;
    updateScoreBar();
    showNextButton();
}

function onWrongAnswer() {
    updateScoreBar();
    showNextButton();
}

function showNextButton() {
    if (gameState.currentIndex + 1 < gameState.total) {
        document.getElementById('next-btn').style.display = 'inline-block';
    } else {
        setTimeout(showResult, 800);
    }
}

function nextQuestion() {
    gameState.currentIndex++;
    document.getElementById('next-btn').style.display = 'none';
    updateScoreBar();
    if (typeof initGameRound === 'function') {
        initGameRound();
    }
}

function showResult() {
    gameState.isPlaying = false;
    document.getElementById('game-area').innerHTML = '';
    document.getElementById('next-btn').style.display = 'none';
    document.getElementById('start-btn').style.display = 'inline-block';

    const resultArea = document.getElementById('result-area');
    resultArea.style.display = 'block';

    const pct = Math.round((gameState.score / gameState.total) * 100);
    document.getElementById('result-title').textContent =
        pct >= 70 ? '🎉 Tuyệt vời!' : pct >= 40 ? '👍 Khá tốt!' : '💪 Cố gắng thêm!';
    document.getElementById('result-score').textContent =
        `Đúng ${gameState.score}/${gameState.total} câu (${pct}%)`;
    document.getElementById('result-stars').textContent = showStars(gameState.score, gameState.total);

    // Update progress bar to 100%
    document.getElementById('progress-fill').style.width = '100%';
}

// Init on page load
document.addEventListener('DOMContentLoaded', function() {
    initTopicSelector();
});
