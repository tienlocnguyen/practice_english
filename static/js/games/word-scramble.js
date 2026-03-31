/**
 * Game: Word Scramble (Xáo trộn chữ cái)
 * Letters are scrambled, player arranges them correctly
 */

let scrambleState = {
    word: '',
    letters: [],
    answer: [],
    used: []
};

function initGameRound() {
    const area = document.getElementById('game-area');
    const currentWord = gameState.words[gameState.currentIndex];
    const word = currentWord.word.toLowerCase();

    // Scramble letters (make sure it's different from original)
    let scrambled = shuffle(word.split(''));
    let attempts = 0;
    while (scrambled.join('') === word && attempts < 20) {
        scrambled = shuffle(word.split(''));
        attempts++;
    }

    scrambleState = {
        word: word,
        letters: scrambled,
        answer: new Array(word.length).fill(''),
        used: new Array(scrambled.length).fill(false)
    };

    renderScramble(currentWord);
}

function renderScramble(wordData) {
    const area = document.getElementById('game-area');

    let slotsHtml = '';
    for (let i = 0; i < scrambleState.word.length; i++) {
        const letter = scrambleState.answer[i] || '';
        const filledClass = letter ? 'filled' : '';
        slotsHtml += `<div class="scramble-slot ${filledClass}" onclick="removeLetterFromSlot(${i})" title="Nhấp để xóa">${escapeHtml(letter)}</div>`;
    }

    let lettersHtml = '';
    for (let i = 0; i < scrambleState.letters.length; i++) {
        const usedClass = scrambleState.used[i] ? 'used' : '';
        lettersHtml += `<button class="scramble-letter ${usedClass}" onclick="addLetterToAnswer(${i})">${escapeHtml(scrambleState.letters[i])}</button>`;
    }

    area.innerHTML = `
        <div class="scramble-area animate-fadeIn">
            <div class="scramble-image">${escapeHtml(wordData.image)}</div>
            <p class="scramble-hint">💡 ${escapeHtml(wordData.meaning)} (${scrambleState.word.length} chữ cái)</p>
            <div class="scramble-answer">${slotsHtml}</div>
            <div class="scramble-letters">${lettersHtml}</div>
            <div class="scramble-controls">
                <button class="btn btn-secondary btn-sm" onclick="clearScramble()">🔄 Xóa hết</button>
                <button class="btn btn-primary" onclick="checkScrambleAnswer()">✅ Kiểm tra</button>
                <button class="btn btn-sm btn-speak" onclick="speak('${escapeHtml(wordData.word)}')">🔊</button>
            </div>
        </div>`;
}

function addLetterToAnswer(letterIdx) {
    if (scrambleState.used[letterIdx]) return;

    // Find first empty slot
    const emptySlot = scrambleState.answer.indexOf('');
    if (emptySlot === -1) return;

    scrambleState.answer[emptySlot] = scrambleState.letters[letterIdx];
    scrambleState.used[letterIdx] = true;

    renderScramble(gameState.words[gameState.currentIndex]);

    // Auto-check if all filled
    if (!scrambleState.answer.includes('')) {
        // Small delay then check
        setTimeout(() => checkScrambleAnswer(), 300);
    }
}

function removeLetterFromSlot(slotIdx) {
    const letter = scrambleState.answer[slotIdx];
    if (!letter) return;

    // Find the letter in the used array (first matching unused)
    for (let i = 0; i < scrambleState.letters.length; i++) {
        if (scrambleState.used[i] && scrambleState.letters[i] === letter) {
            scrambleState.used[i] = false;
            break;
        }
    }
    scrambleState.answer[slotIdx] = '';

    renderScramble(gameState.words[gameState.currentIndex]);
}

function clearScramble() {
    scrambleState.answer = new Array(scrambleState.word.length).fill('');
    scrambleState.used = new Array(scrambleState.letters.length).fill(false);
    renderScramble(gameState.words[gameState.currentIndex]);
}

function checkScrambleAnswer() {
    if (!gameState.isPlaying) return;

    const answer = scrambleState.answer.join('').toLowerCase();
    const correct = scrambleState.word;

    if (answer.length < correct.length) {
        // Not all filled
        return;
    }

    const slots = document.querySelectorAll('.scramble-slot');
    const buttons = document.querySelectorAll('.scramble-letter');

    if (answer === correct) {
        slots.forEach(s => {
            s.style.borderColor = 'var(--success)';
            s.style.background = 'rgba(16, 185, 129, 0.15)';
            s.style.color = 'var(--success)';
        });
        buttons.forEach(b => b.disabled = true);
        onCorrectAnswer();
    } else {
        slots.forEach((s, i) => {
            if (scrambleState.answer[i] === correct[i]) {
                s.style.borderColor = 'var(--success)';
                s.style.color = 'var(--success)';
            } else {
                s.style.borderColor = 'var(--danger)';
                s.style.color = 'var(--danger)';
            }
        });

        // Show correct answer after a delay
        setTimeout(() => {
            for (let i = 0; i < correct.length; i++) {
                scrambleState.answer[i] = correct[i];
            }
            renderScramble(gameState.words[gameState.currentIndex]);
            // Disable interaction
            document.querySelectorAll('.scramble-letter').forEach(b => b.disabled = true);
            document.querySelectorAll('.scramble-slot').forEach(s => s.style.pointerEvents = 'none');
        }, 800);

        onWrongAnswer();
    }

    speak(correct);
}
