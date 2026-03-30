/**
 * Game: Word-Image (Chọn từ với hình ảnh)
 * Show an image, player picks the correct word from options
 */

function initGameRound() {
    const area = document.getElementById('game-area');
    const currentWord = gameState.words[gameState.currentIndex];
    const allWords = getAllWords(TOPICS_DATA);

    // Get 3 wrong options
    const wrongOptions = shuffle(allWords.filter(w => w.word !== currentWord.word))
        .slice(0, 3)
        .map(w => w.word);
    const options = shuffle([currentWord.word, ...wrongOptions]);

    let optionsHtml = '';
    for (const opt of options) {
        const safeOpt = escapeHtml(opt);
        optionsHtml += `<button class="option-btn" onclick="checkAnswer(this, '${safeOpt}', '${escapeHtml(currentWord.word)}')">${safeOpt}</button>`;
    }

    area.innerHTML = `
        <div class="animate-fadeIn">
            <img src="${escapeHtml(currentWord.image)}" alt="?" class="question-image" loading="lazy">
            <div class="question-meaning">💡 ${escapeHtml(currentWord.meaning)}</div>
            <div class="options-grid">${optionsHtml}</div>
        </div>`;

    speak(currentWord.word);
}

function checkAnswer(btn, selected, correct) {
    if (!gameState.isPlaying) return;

    const buttons = document.querySelectorAll('.option-btn');
    buttons.forEach(b => b.classList.add('disabled'));

    if (selected === correct) {
        btn.classList.add('correct');
        onCorrectAnswer();
    } else {
        btn.classList.add('wrong');
        // Highlight correct answer
        buttons.forEach(b => {
            if (b.textContent === correct) b.classList.add('correct');
        });
        onWrongAnswer();
    }

    speak(correct);
}
