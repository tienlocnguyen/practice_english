/**
 * Game: Vietnamese to English (Viết từ tiếng Anh)
 * Shows Vietnamese meaning, player types the English word.
 */

function initGameRound() {
    const currentWord = gameState.words[gameState.currentIndex];
    renderVnToEn(currentWord);
}

function renderVnToEn(wordData) {
    const area = document.getElementById('game-area');
    area.innerHTML = `
        <div class="vn-to-en-area animate-fadeIn">
            <p class="vte-label">Hãy viết từ tiếng Anh có nghĩa là:</p>
            <div class="vte-meaning">${escapeHtml(wordData.meaning)}</div>
            <p class="vte-phonetic">${escapeHtml(wordData.phonetic)}</p>
            <div class="vte-input-row">
                <input
                    type="text"
                    id="vte-answer"
                    class="vte-input"
                    placeholder="Nhập từ tiếng Anh..."
                    autocomplete="off"
                    autocorrect="off"
                    autocapitalize="off"
                    spellcheck="false"
                    onkeydown="if(event.key==='Enter') checkVnToEn()"
                >
                <button class="btn btn-primary" onclick="checkVnToEn()">✅ Kiểm tra</button>
                <button class="btn btn-sm btn-speak" onclick="speak('${escapeHtml(wordData.word)}')">🔊</button>
            </div>
            <p class="vte-hint">💡 Gợi ý: ${escapeHtml(wordData.hint)}</p>
        </div>`;

    const input = document.getElementById('vte-answer');
    if (input) setTimeout(() => input.focus(), 80);
}

function checkVnToEn() {
    if (!gameState.isPlaying) return;
    const input = document.getElementById('vte-answer');
    if (!input || input.disabled) return;

    const userAnswer = input.value.trim().toLowerCase();
    const currentWord = gameState.words[gameState.currentIndex];
    const correct = currentWord.word.trim().toLowerCase();

    input.disabled = true;
    const checkBtn = input.nextElementSibling;
    if (checkBtn) checkBtn.disabled = true;

    const area = document.getElementById('game-area');
    const existingFeedback = area.querySelector('.vte-feedback');
    if (existingFeedback) existingFeedback.remove();

    const feedback = document.createElement('div');

    if (userAnswer === correct) {
        feedback.className = 'vte-feedback vte-correct';
        feedback.innerHTML = `✅ Đúng rồi! <strong>${escapeHtml(currentWord.word)}</strong> — ${escapeHtml(currentWord.meaning)}`;
        area.querySelector('.vn-to-en-area').appendChild(feedback);
        onCorrectAnswer();
    } else {
        feedback.className = 'vte-feedback vte-wrong';
        feedback.innerHTML = `❌ Sai rồi! Đáp án đúng là: <strong>${escapeHtml(currentWord.word)}</strong> — ${escapeHtml(currentWord.meaning)}`;
        area.querySelector('.vn-to-en-area').appendChild(feedback);
        onWrongAnswer();
    }
}
