/**
 * Game: Speed Challenge (Thử thách tốc độ)
 * Answer as many questions as possible within a time limit.
 * Mix of word-image, fill-letter, and image-word questions.
 */

let speedState = {
    timer: null,
    timeLeft: 60,
    totalTime: 60,
    streak: 0,
    bestStreak: 0,
    questionType: ''
};

// Override startGame for speed challenge
function startGame() {
    const topicId = document.getElementById('topic-select').value;
    const allWords = getWordsByTopic(TOPICS_DATA, topicId);

    if (allWords.length < 4) {
        alert('Cần ít nhất 4 từ để chơi!');
        return;
    }

    gameState.words = shuffle(allWords);
    gameState.currentIndex = 0;
    gameState.score = 0;
    gameState.total = 0;
    gameState.isPlaying = true;

    speedState.timeLeft = 60;
    speedState.streak = 0;
    speedState.bestStreak = 0;

    document.getElementById('score-bar').style.display = 'flex';
    document.getElementById('result-area').style.display = 'none';
    document.getElementById('start-btn').style.display = 'none';
    document.getElementById('next-btn').style.display = 'none';

    updateSpeedScoreBar();
    startTimer();
    initGameRound();
}

function startTimer() {
    clearInterval(speedState.timer);
    speedState.timer = setInterval(() => {
        speedState.timeLeft--;
        updateSpeedScoreBar();

        if (speedState.timeLeft <= 0) {
            clearInterval(speedState.timer);
            endSpeedGame();
        }
    }, 1000);
}

function updateSpeedScoreBar() {
    const timeColor = speedState.timeLeft <= 10 ? 'var(--danger)' : 
                      speedState.timeLeft <= 20 ? 'var(--warning)' : 'var(--primary)';
    document.getElementById('score-text').innerHTML = 
        `Điểm: <strong>${gameState.score}</strong> | 🔥 ${speedState.streak}`;
    document.getElementById('progress-text').innerHTML = 
        `<span style="color:${timeColor};font-weight:700">⏱️ ${speedState.timeLeft}s</span>`;
    const pct = (speedState.timeLeft / speedState.totalTime) * 100;
    document.getElementById('progress-fill').style.width = pct + '%';
}

function initGameRound() {
    if (!gameState.isPlaying) return;

    const area = document.getElementById('game-area');
    // Cycle through words, loop if needed
    if (gameState.currentIndex >= gameState.words.length) {
        gameState.words = shuffle(gameState.words);
        gameState.currentIndex = 0;
    }

    const currentWord = gameState.words[gameState.currentIndex];
    const allWords = getAllWords(TOPICS_DATA);

    // Randomly choose question type
    const types = ['word-from-image', 'image-from-word', 'spell-first'];
    speedState.questionType = types[Math.floor(Math.random() * types.length)];

    if (speedState.questionType === 'word-from-image') {
        renderWordFromImage(area, currentWord, allWords);
    } else if (speedState.questionType === 'image-from-word') {
        renderImageFromWord(area, currentWord, allWords);
    } else {
        renderSpellFirst(area, currentWord);
    }
}

function renderWordFromImage(area, currentWord, allWords) {
    const wrongOptions = shuffle(allWords.filter(w => w.word !== currentWord.word))
        .slice(0, 3).map(w => w.word);
    const options = shuffle([currentWord.word, ...wrongOptions]);

    let optionsHtml = '';
    for (const opt of options) {
        const safeOpt = escapeHtml(opt);
        optionsHtml += `<button class="option-btn" onclick="speedAnswer(this, '${safeOpt}', '${escapeHtml(currentWord.word)}')">${safeOpt}</button>`;
    }

    area.innerHTML = `
        <div class="animate-pop" style="text-align:center">
            <div class="speed-type-badge">🖼️ Chọn từ đúng</div>
            <img src="${escapeHtml(currentWord.image)}" alt="?" class="question-image" loading="lazy">
            <div class="options-grid">${optionsHtml}</div>
        </div>`;
}

function renderImageFromWord(area, currentWord, allWords) {
    const wrongOptions = shuffle(allWords.filter(w => w.word !== currentWord.word)).slice(0, 3);
    const options = shuffle([currentWord, ...wrongOptions]);

    let optionsHtml = '';
    for (const opt of options) {
        const safeWord = escapeHtml(opt.word);
        optionsHtml += `
            <div class="image-option" onclick="speedImageAnswer(this, '${safeWord}', '${escapeHtml(currentWord.word)}')">
                <img src="${escapeHtml(opt.image)}" alt="?" loading="lazy">
            </div>`;
    }

    area.innerHTML = `
        <div class="animate-pop" style="text-align:center">
            <div class="speed-type-badge">🔍 Chọn hình đúng</div>
            <div class="question-word">${escapeHtml(currentWord.word)}</div>
            <div class="image-options-grid">${optionsHtml}</div>
        </div>`;
}

function renderSpellFirst(area, currentWord) {
    const word = currentWord.word.toLowerCase();
    const firstLetter = word[0];
    const restHidden = word.slice(1).replace(/[a-z]/g, ' _ ');

    area.innerHTML = `
        <div class="animate-pop" style="text-align:center">
            <div class="speed-type-badge">✏️ Đánh vần nhanh</div>
            <img src="${escapeHtml(currentWord.image)}" alt="?" class="fill-image" loading="lazy">
            <p style="font-size:1.2rem;margin-bottom:1rem">💡 ${escapeHtml(currentWord.meaning)}</p>
            <div style="font-size:1.5rem;font-weight:700;color:var(--primary);margin-bottom:1rem;letter-spacing:3px">
                ${firstLetter.toUpperCase()} ${restHidden}
            </div>
            <div class="guess-input-area">
                <input type="text" class="guess-input" id="speed-input" placeholder="Nhập từ..." 
                       onkeyup="if(event.key==='Enter')checkSpeedSpell()" autofocus>
                <button class="btn btn-primary" onclick="checkSpeedSpell()">→</button>
            </div>
        </div>`;

    setTimeout(() => {
        const input = document.getElementById('speed-input');
        if (input) input.focus();
    }, 50);
}

function speedAnswer(btn, selected, correct) {
    if (!gameState.isPlaying) return;
    gameState.total++;

    const buttons = document.querySelectorAll('.option-btn');
    buttons.forEach(b => b.classList.add('disabled'));

    if (selected === correct) {
        btn.classList.add('correct');
        gameState.score++;
        speedState.streak++;
        speedState.bestStreak = Math.max(speedState.bestStreak, speedState.streak);
        // Bonus time for streaks
        if (speedState.streak % 5 === 0) {
            speedState.timeLeft = Math.min(speedState.timeLeft + 5, speedState.totalTime);
        }
    } else {
        btn.classList.add('wrong');
        buttons.forEach(b => { if (b.textContent === correct) b.classList.add('correct'); });
        speedState.streak = 0;
    }

    updateSpeedScoreBar();
    gameState.currentIndex++;
    setTimeout(() => initGameRound(), 400);
}

function speedImageAnswer(el, selected, correct) {
    if (!gameState.isPlaying) return;
    gameState.total++;

    const cards = document.querySelectorAll('.image-option');
    cards.forEach(c => c.classList.add('disabled'));

    if (selected === correct) {
        el.classList.add('correct');
        gameState.score++;
        speedState.streak++;
        speedState.bestStreak = Math.max(speedState.bestStreak, speedState.streak);
        if (speedState.streak % 5 === 0) {
            speedState.timeLeft = Math.min(speedState.timeLeft + 5, speedState.totalTime);
        }
    } else {
        el.classList.add('wrong');
        speedState.streak = 0;
    }

    updateSpeedScoreBar();
    gameState.currentIndex++;
    setTimeout(() => initGameRound(), 400);
}

function checkSpeedSpell() {
    if (!gameState.isPlaying) return;
    const input = document.getElementById('speed-input');
    if (!input) return;

    const guess = input.value.trim().toLowerCase();
    if (!guess) return;

    const currentWord = gameState.words[gameState.currentIndex];
    const correct = currentWord.word.toLowerCase();
    gameState.total++;

    if (guess === correct) {
        input.style.borderColor = 'var(--success)';
        input.style.background = 'rgba(16, 185, 129, 0.1)';
        gameState.score++;
        speedState.streak++;
        speedState.bestStreak = Math.max(speedState.bestStreak, speedState.streak);
        if (speedState.streak % 5 === 0) {
            speedState.timeLeft = Math.min(speedState.timeLeft + 5, speedState.totalTime);
        }
    } else {
        input.style.borderColor = 'var(--danger)';
        input.style.background = 'rgba(239, 68, 68, 0.1)';
        speedState.streak = 0;
    }

    updateSpeedScoreBar();
    gameState.currentIndex++;
    setTimeout(() => initGameRound(), 400);
}

function endSpeedGame() {
    gameState.isPlaying = false;
    document.getElementById('game-area').innerHTML = '';
    document.getElementById('start-btn').style.display = 'inline-block';

    const resultArea = document.getElementById('result-area');
    resultArea.style.display = 'block';

    const pct = gameState.total > 0 ? Math.round((gameState.score / gameState.total) * 100) : 0;
    const stars = gameState.score >= 15 ? '⭐⭐⭐' : gameState.score >= 10 ? '⭐⭐' : gameState.score >= 5 ? '⭐' : '💪';

    document.getElementById('result-title').textContent = '⏱️ Hết giờ!';
    document.getElementById('result-score').innerHTML = 
        `Đúng: <strong>${gameState.score}</strong>/${gameState.total} câu (${pct}%)<br>
         🔥 Chuỗi dài nhất: ${speedState.bestStreak}`;
    document.getElementById('result-stars').textContent = stars;
    document.getElementById('progress-fill').style.width = '0%';
}

function nextQuestion() {
    // Not used in speed mode
}
