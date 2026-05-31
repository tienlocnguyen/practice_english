/**
 * Game: Fill Letter (Điền chữ cái vào từ)
 * Show word with missing letters, player fills them in
 */

let fillState = {
    word: '',
    blanks: [],
    inputs: []
};

function initGameRound() {
    const area = document.getElementById('game-area');
    const currentWord = gameState.words[gameState.currentIndex];
    const word = currentWord.word.toLowerCase();

    // Decide how many letters to hide (30-50% of letters)
    const hideCount = Math.max(1, Math.ceil(word.length * 0.4));
    const indices = [];
    const available = Array.from({length: word.length}, (_, i) => i);
    const shuffledIndices = shuffle(available);
    for (let i = 0; i < hideCount; i++) {
        indices.push(shuffledIndices[i]);
    }
    indices.sort((a, b) => a - b);

    fillState.word = word;
    fillState.blanks = indices;

    let lettersHtml = '';
    let inputIndex = 0;
    for (let i = 0; i < word.length; i++) {
        if (indices.includes(i)) {
            lettersHtml += `<input type="text" maxlength="1" class="letter-input" data-index="${i}" data-input-index="${inputIndex}" 
                onkeyup="handleFillInput(event, this)" autofocus>`;
            inputIndex++;
        } else {
            lettersHtml += `<span class="letter-box filled">${escapeHtml(word[i])}</span>`;
        }
    }

    area.innerHTML = `
        <div class="animate-fadeIn" style="text-align:center">
            <div class="fill-image">${escapeHtml(currentWord.image)}</div>
            <div class="question-meaning">💡 ${escapeHtml(currentWord.meaning)}</div>
            <div class="fill-word-display">${lettersHtml}</div>
            <p class="fill-hint">🔤 Điền ${hideCount} chữ cái còn thiếu</p>
            <div class="fill-submit-area">
                <button class="btn btn-primary" onclick="checkFillAnswer()">✅ Kiểm tra</button>
                <button class="btn btn-sm btn-speak" onclick="speak('${escapeHtml(currentWord.word)}')">🔊 Nghe</button>
            </div>
        </div>`;

    // Focus first input
    const firstInput = area.querySelector('.letter-input');
    if (firstInput) setTimeout(() => firstInput.focus(), 100);
}

function handleFillInput(event, input) {
    const value = input.value;
    if (value.length === 1) {
        // Move to next empty input
        const inputs = document.querySelectorAll('.letter-input');
        const currentIdx = parseInt(input.dataset.inputIndex);
        for (let i = currentIdx + 1; i < inputs.length; i++) {
            if (!inputs[i].value) {
                inputs[i].focus();
                return;
            }
        }
    }

    if (event.key === 'Backspace' && !value) {
        const inputs = document.querySelectorAll('.letter-input');
        const currentIdx = parseInt(input.dataset.inputIndex);
        if (currentIdx > 0) {
            inputs[currentIdx - 1].focus();
        }
    }

    if (event.key === 'Enter') {
        checkFillAnswer();
    }
}

function checkFillAnswer() {
    if (!gameState.isPlaying) return;

    const inputs = document.querySelectorAll('.letter-input');
    if (inputs.length > 0 && inputs[0].disabled) return;

    const submitBtns = document.querySelectorAll('.fill-submit-area button');
    submitBtns.forEach(btn => {
        if (btn.textContent.includes('Kiểm tra')) {
            btn.disabled = true;
        }
    });

    let allCorrect = true;

    inputs.forEach(input => {
        const charIndex = parseInt(input.dataset.index);
        const expected = fillState.word[charIndex].toLowerCase();
        const entered = input.value.toLowerCase();

        input.disabled = true;
        if (entered === expected) {
            input.style.borderColor = 'var(--success)';
            input.style.background = 'rgba(16, 185, 129, 0.15)';
            input.style.color = 'var(--success)';
            input.style.borderStyle = 'solid';
        } else {
            input.style.borderColor = 'var(--danger)';
            input.style.background = 'rgba(239, 68, 68, 0.15)';
            input.style.color = 'var(--danger)';
            input.value = expected; // Show correct letter
            allCorrect = false;
        }
    });

    if (allCorrect) {
        onCorrectAnswer();
    } else {
        onWrongAnswer();
    }

    speak(fillState.word);
}
