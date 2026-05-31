/**
 * Game: Word Guess (Đoán từ với gợi ý)
 * Show hints progressively, player guesses the word
 */

let guessState = {
    word: null,
    hintsShown: 0,
    maxHints: 4,
    attempts: 0,
    maxAttempts: 3
};

function initGameRound() {
    const area = document.getElementById('game-area');
    const currentWord = gameState.words[gameState.currentIndex];

    // Build hints
    const hints = [];
    hints.push(`Chủ đề: ${currentWord.topicName || '?'}`);
    hints.push(`Từ có ${currentWord.word.length} chữ cái`);
    if (currentWord.hint) hints.push(currentWord.hint);
    hints.push(`Bắt đầu bằng chữ "${currentWord.word[0].toUpperCase()}"`);
    if (currentWord.example) hints.push(`Ví dụ: "${currentWord.example}"`);

    guessState.word = currentWord;
    guessState.hintsShown = 2; // Show first 2 hints
    guessState.maxHints = hints.length;
    guessState.attempts = 0;

    let hintsHtml = '';
    for (let i = 0; i < hints.length; i++) {
        const visible = i < guessState.hintsShown ? 'visible' : '';
        hintsHtml += `
            <li class="hint-item ${visible}" id="hint-${i}">
                <span class="hint-number">${i + 1}</span>
                <span>${escapeHtml(hints[i])}</span>
            </li>`;
    }

    area.innerHTML = `
        <div class="guess-area animate-fadeIn">
            <div id="guess-img" style="font-size:80px;line-height:1;text-align:center;margin:0 auto 1rem;filter:blur(15px);transition:filter 0.5s;user-select:none">${escapeHtml(currentWord.image)}</div>
            <ul class="hint-list">${hintsHtml}</ul>
            <div class="guess-input-area">
                <input type="text" class="guess-input" id="guess-input" placeholder="Nhập từ..." onkeyup="if(event.key==='Enter')submitGuess()">
                <button class="btn btn-primary" onclick="submitGuess()">Đoán</button>
            </div>
            <p class="guess-feedback" id="guess-feedback"></p>
            <button class="btn btn-secondary btn-sm hint-more-btn" onclick="showMoreHint()">💡 Thêm gợi ý (${guessState.maxHints - guessState.hintsShown} còn lại)</button>
        </div>`;

    // Store hints for later
    guessState.hints = hints;

    setTimeout(() => document.getElementById('guess-input').focus(), 100);
}

function showMoreHint() {
    if (guessState.hintsShown >= guessState.maxHints) return;

    const hintEl = document.getElementById(`hint-${guessState.hintsShown}`);
    if (hintEl) {
        hintEl.classList.add('visible');
    }
    guessState.hintsShown++;

    // Reduce blur on image
    const img = document.getElementById('guess-img');
    const blur = Math.max(0, 15 - guessState.hintsShown * 4);
    img.style.filter = `blur(${blur}px)`;

    // Update button
    const remaining = guessState.maxHints - guessState.hintsShown;
    const btn = document.querySelector('.hint-more-btn');
    if (remaining <= 0) {
        btn.disabled = true;
        btn.textContent = '💡 Hết gợi ý';
    } else {
        btn.textContent = `💡 Thêm gợi ý (${remaining} còn lại)`;
    }
}

function submitGuess() {
    if (!gameState.isPlaying) return;

    const input = document.getElementById('guess-input');
    if (!input || input.disabled) return;

    const feedback = document.getElementById('guess-feedback');
    const guess = input.value.trim().toLowerCase();

    if (!guess) return;

    const correct = guessState.word.word.toLowerCase();

    if (guess === correct) {
        feedback.textContent = '✅ Chính xác!';
        feedback.style.color = 'var(--success)';
        input.disabled = true;
        const submitBtn = input.nextElementSibling;
        if (submitBtn) submitBtn.disabled = true;
        document.getElementById('guess-img').style.filter = 'blur(0)';
        // Show all hints
        for (let i = 0; i < guessState.maxHints; i++) {
            const h = document.getElementById(`hint-${i}`);
            if (h) h.classList.add('visible');
        }
        onCorrectAnswer();
    } else {
        guessState.attempts++;
        if (guessState.attempts >= guessState.maxAttempts) {
            feedback.textContent = `❌ Đáp án: ${correct}`;
            feedback.style.color = 'var(--danger)';
            input.disabled = true;
            const submitBtn = input.nextElementSibling;
            if (submitBtn) submitBtn.disabled = true;
            document.getElementById('guess-img').style.filter = 'blur(0)';
            onWrongAnswer();
        } else {
            feedback.textContent = `❌ Sai rồi! Còn ${guessState.maxAttempts - guessState.attempts} lần thử`;
            feedback.style.color = 'var(--warning)';
            input.value = '';
            input.focus();
            showMoreHint(); // Give extra hint on wrong answer
        }
    }

    speak(correct);
}
