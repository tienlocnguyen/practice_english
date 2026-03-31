/**
 * Game: Image-Word (Chọn hình ảnh ứng với từ)
 * Show a word, player picks the correct image
 */

function initGameRound() {
    const area = document.getElementById('game-area');
    const currentWord = gameState.words[gameState.currentIndex];
    const allWords = getAllWords(TOPICS_DATA);

    // Get 3 wrong image options
    const wrongOptions = shuffle(allWords.filter(w => w.word !== currentWord.word))
        .slice(0, 3);
    const options = shuffle([currentWord, ...wrongOptions]);

    let optionsHtml = '';
    for (const opt of options) {
        const safeWord = escapeHtml(opt.word);
        optionsHtml += `
            <div class="image-option" data-word="${safeWord}" onclick="checkImageAnswer(this, '${safeWord}', '${escapeHtml(currentWord.word)}')">
                <span class="option-emoji">${escapeHtml(opt.image)}</span>
            </div>`;
    }

    area.innerHTML = `
        <div class="animate-fadeIn">
            <div class="question-word">
                ${escapeHtml(currentWord.word)}
                <button class="btn btn-sm btn-speak" onclick="speak('${escapeHtml(currentWord.word)}')">🔊</button>
            </div>
            <div class="question-meaning">💡 ${escapeHtml(currentWord.meaning)}</div>
            <div class="image-options-grid">${optionsHtml}</div>
        </div>`;

    speak(currentWord.word);
}

function checkImageAnswer(el, selected, correct) {
    if (!gameState.isPlaying) return;

    const cards = document.querySelectorAll('.image-option');
    cards.forEach(c => c.classList.add('disabled'));

    if (selected === correct) {
        el.classList.add('correct');
        onCorrectAnswer();
    } else {
        el.classList.add('wrong');
        // Highlight correct one by data-word attribute
        cards.forEach(c => {
            if (c.dataset.word === correct) {
                c.classList.add('correct');
            }
        });
        onWrongAnswer();
    }

    speak(correct);
}
