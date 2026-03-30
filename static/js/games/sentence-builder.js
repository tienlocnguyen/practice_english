/**
 * Game: Sentence Builder (Xây dựng câu)
 * Arrange shuffled words to form correct sentences.
 * Uses the example sentences from word data.
 */

let sentenceState = {
    sentence: [],
    shuffled: [],
    answer: [],
    used: []
};

function initGameRound() {
    const area = document.getElementById('game-area');
    const currentWord = gameState.words[gameState.currentIndex];
    
    // Build sentence from example
    let sentence = currentWord.example || `I like ${currentWord.word}.`;
    // Clean sentence
    sentence = sentence.replace(/["""]/g, '').trim();
    if (!sentence.endsWith('.') && !sentence.endsWith('!') && !sentence.endsWith('?')) {
        sentence += '.';
    }

    // Split into words (keep punctuation attached)
    const words = sentence.split(/\s+/);
    
    // Shuffle words
    let shuffled = shuffle([...words]);
    let attempts = 0;
    while (shuffled.join(' ') === words.join(' ') && attempts < 20) {
        shuffled = shuffle([...words]);
        attempts++;
    }

    sentenceState = {
        sentence: words,
        shuffled: shuffled,
        answer: [],
        used: new Array(shuffled.length).fill(false)
    };

    renderSentenceBuilder(currentWord);
}

function renderSentenceBuilder(wordData) {
    const area = document.getElementById('game-area');

    // Answer slots
    let slotsHtml = '<div class="sentence-answer" id="sentence-answer">';
    for (let i = 0; i < sentenceState.sentence.length; i++) {
        const word = sentenceState.answer[i] || '';
        const filledClass = word ? 'filled' : '';
        slotsHtml += `<div class="sentence-slot ${filledClass}" onclick="removeWordFromSlot(${i})" title="Nhấp để xóa">${escapeHtml(word)}</div>`;
    }
    slotsHtml += '</div>';

    // Available words
    let wordsHtml = '<div class="sentence-words">';
    for (let i = 0; i < sentenceState.shuffled.length; i++) {
        const usedClass = sentenceState.used[i] ? 'used' : '';
        wordsHtml += `<button class="sentence-word-btn ${usedClass}" onclick="addWordToSentence(${i})">${escapeHtml(sentenceState.shuffled[i])}</button>`;
    }
    wordsHtml += '</div>';

    area.innerHTML = `
        <div class="animate-fadeIn sentence-builder-area">
            <div class="sentence-context">
                <img src="${escapeHtml(wordData.image)}" alt="" class="sentence-img" loading="lazy">
                <div>
                    <div class="sentence-target-word">${escapeHtml(wordData.word)}</div>
                    <div class="sentence-meaning">💡 ${escapeHtml(wordData.meaning)}</div>
                </div>
            </div>
            <p class="sentence-instruction">📝 Sắp xếp các từ thành câu đúng:</p>
            ${slotsHtml}
            ${wordsHtml}
            <div class="sentence-controls">
                <button class="btn btn-secondary btn-sm" onclick="clearSentence()">🔄 Xóa hết</button>
                <button class="btn btn-primary" onclick="checkSentenceAnswer()">✅ Kiểm tra</button>
                <button class="btn btn-sm btn-speak" onclick="speak('${escapeHtml(sentenceState.sentence.join(' '))}')">🔊</button>
            </div>
        </div>`;
}

function addWordToSentence(wordIdx) {
    if (sentenceState.used[wordIdx]) return;

    const emptySlot = sentenceState.answer.length;
    if (emptySlot >= sentenceState.sentence.length) return;

    sentenceState.answer.push(sentenceState.shuffled[wordIdx]);
    sentenceState.used[wordIdx] = true;

    renderSentenceBuilder(gameState.words[gameState.currentIndex]);

    // Auto check if all slots filled
    if (sentenceState.answer.length === sentenceState.sentence.length) {
        setTimeout(() => checkSentenceAnswer(), 300);
    }
}

function removeWordFromSlot(slotIdx) {
    if (slotIdx >= sentenceState.answer.length) return;
    const word = sentenceState.answer[slotIdx];
    
    // Find the word in shuffled and unmark it
    for (let i = 0; i < sentenceState.shuffled.length; i++) {
        if (sentenceState.used[i] && sentenceState.shuffled[i] === word) {
            sentenceState.used[i] = false;
            break;
        }
    }
    
    // Remove from answer and shift remaining
    sentenceState.answer.splice(slotIdx, 1);

    renderSentenceBuilder(gameState.words[gameState.currentIndex]);
}

function clearSentence() {
    sentenceState.answer = [];
    sentenceState.used = new Array(sentenceState.shuffled.length).fill(false);
    renderSentenceBuilder(gameState.words[gameState.currentIndex]);
}

function checkSentenceAnswer() {
    if (!gameState.isPlaying) return;
    if (sentenceState.answer.length < sentenceState.sentence.length) return;

    const correctSentence = sentenceState.sentence.join(' ');
    const userSentence = sentenceState.answer.join(' ');

    const slots = document.querySelectorAll('.sentence-slot');
    const wordBtns = document.querySelectorAll('.sentence-word-btn');

    if (userSentence === correctSentence) {
        slots.forEach(s => {
            s.style.borderColor = 'var(--success)';
            s.style.background = 'rgba(16, 185, 129, 0.15)';
            s.style.color = 'var(--success)';
        });
        wordBtns.forEach(b => b.disabled = true);
        onCorrectAnswer();
    } else {
        // Highlight correct/wrong positions
        slots.forEach((s, i) => {
            if (sentenceState.answer[i] === sentenceState.sentence[i]) {
                s.style.borderColor = 'var(--success)';
                s.style.color = 'var(--success)';
            } else {
                s.style.borderColor = 'var(--danger)';
                s.style.color = 'var(--danger)';
            }
        });

        // Show correct answer after delay
        setTimeout(() => {
            sentenceState.answer = [...sentenceState.sentence];
            renderSentenceBuilder(gameState.words[gameState.currentIndex]);
            document.querySelectorAll('.sentence-word-btn').forEach(b => b.disabled = true);
            document.querySelectorAll('.sentence-slot').forEach(s => {
                s.style.pointerEvents = 'none';
                s.style.borderColor = 'var(--success)';
                s.style.color = 'var(--success)';
            });
        }, 1200);

        onWrongAnswer();
    }

    speak(correctSentence);
}
