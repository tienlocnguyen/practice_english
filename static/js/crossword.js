/**
 * Crossword Puzzle Engine
 */

let cwState = {
    data: null,
    grid: [],
    size: 0,
    words: [],
    numberMap: {}
};

function startCrossword() {
    const select = document.getElementById('crossword-select');
    const idx = parseInt(select.value);
    const cw = CROSSWORDS_DATA[idx];

    if (!cw) return;

    cwState.data = cw;
    cwState.size = cw.size;
    cwState.words = cw.words;

    // Build empty grid
    cwState.grid = [];
    for (let r = 0; r < cw.size; r++) {
        cwState.grid[r] = [];
        for (let c = 0; c < cw.size; c++) {
            cwState.grid[r][c] = { letter: '', isActive: false, number: 0, inputId: '' };
        }
    }

    // Place words on grid
    cwState.numberMap = {};
    let num = 1;
    // Sort words by position for numbering
    const sortedWords = [...cwState.words].sort((a, b) => {
        if (a.row !== b.row) return a.row - b.row;
        return a.col - b.col;
    });

    for (const w of sortedWords) {
        const key = `${w.row}-${w.col}`;
        if (!cwState.numberMap[key]) {
            cwState.numberMap[key] = num++;
        }
        w.number = cwState.numberMap[key];

        for (let i = 0; i < w.word.length; i++) {
            const r = w.direction === 'down' ? w.row + i : w.row;
            const c = w.direction === 'across' ? w.col + i : w.col;
            if (r < cw.size && c < cw.size) {
                cwState.grid[r][c].letter = w.word[i].toUpperCase();
                cwState.grid[r][c].isActive = true;
                cwState.grid[r][c].inputId = `cw-${r}-${c}`;
            }
        }
        // Set number
        cwState.grid[w.row][w.col].number = cwState.numberMap[key];
    }

    document.getElementById('crossword-result').style.display = 'none';
    renderCrossword();
}

function renderCrossword() {
    const gridEl = document.getElementById('crossword-grid');
    const cluesEl = document.getElementById('crossword-clues');

    // Render grid
    let gridHtml = '';
    gridEl.style.gridTemplateColumns = `repeat(${cwState.size}, 45px)`;

    for (let r = 0; r < cwState.size; r++) {
        for (let c = 0; c < cwState.size; c++) {
            const cell = cwState.grid[r][c];
            if (cell.isActive) {
                const numHtml = cell.number > 0 ? `<span class="cw-number">${cell.number}</span>` : '';
                gridHtml += `<div class="cw-cell" id="cell-${r}-${c}">
                    ${numHtml}
                    <input type="text" maxlength="1" id="cw-${r}-${c}" 
                           onkeyup="handleCwInput(event, ${r}, ${c})"
                           onfocus="highlightClue(${r}, ${c})">
                </div>`;
            } else {
                gridHtml += `<div class="cw-cell blocked"></div>`;
            }
        }
    }
    gridEl.innerHTML = gridHtml;

    // Render clues
    const acrossClues = cwState.words.filter(w => w.direction === 'across').sort((a, b) => a.number - b.number);
    const downClues = cwState.words.filter(w => w.direction === 'down').sort((a, b) => a.number - b.number);

    let cluesHtml = '<h3>➡️ Hàng ngang (Across)</h3>';
    for (const w of acrossClues) {
        cluesHtml += `<div class="clue-item" onclick="focusWord(${w.row}, ${w.col}, '${w.direction}')">
            <span class="clue-number">${w.number}.</span> ${escapeHtml(w.clue_vi || w.clue)}
        </div>`;
    }

    cluesHtml += '<h3 style="margin-top:1rem">⬇️ Hàng dọc (Down)</h3>';
    for (const w of downClues) {
        cluesHtml += `<div class="clue-item" onclick="focusWord(${w.row}, ${w.col}, '${w.direction}')">
            <span class="clue-number">${w.number}.</span> ${escapeHtml(w.clue_vi || w.clue)}
        </div>`;
    }

    cluesEl.innerHTML = cluesHtml;
}

function handleCwInput(event, row, col) {
    const input = document.getElementById(`cw-${row}-${col}`);
    if (!input) return;

    if (input.value.length === 1 || event.key === 'ArrowRight' || event.key === 'ArrowDown') {
        // Try moving right first, then down
        const nextRight = document.getElementById(`cw-${row}-${col + 1}`);
        const nextDown = document.getElementById(`cw-${row + 1}-${col}`);
        if (nextRight) nextRight.focus();
        else if (nextDown) nextDown.focus();
    }

    if (event.key === 'ArrowLeft') {
        const prev = document.getElementById(`cw-${row}-${col - 1}`);
        if (prev) prev.focus();
    }
    if (event.key === 'ArrowUp') {
        const prev = document.getElementById(`cw-${row - 1}-${col}`);
        if (prev) prev.focus();
    }

    if (event.key === 'Backspace' && !input.value) {
        const prevRight = document.getElementById(`cw-${row}-${col - 1}`);
        const prevDown = document.getElementById(`cw-${row - 1}-${col}`);
        if (prevRight) prevRight.focus();
        else if (prevDown) prevDown.focus();
    }
}

function focusWord(row, col, direction) {
    const input = document.getElementById(`cw-${row}-${col}`);
    if (input) input.focus();
}

function highlightClue(row, col) {
    // Could add visual clue highlighting
}

function checkCrossword() {
    let totalCells = 0;
    let correctCells = 0;

    for (let r = 0; r < cwState.size; r++) {
        for (let c = 0; c < cwState.size; c++) {
            const cell = cwState.grid[r][c];
            if (!cell.isActive) continue;

            totalCells++;
            const input = document.getElementById(`cw-${r}-${c}`);
            const cellEl = document.getElementById(`cell-${r}-${c}`);
            if (!input || !cellEl) continue;

            const entered = input.value.toUpperCase();
            if (entered === cell.letter) {
                correctCells++;
                cellEl.classList.remove('wrong');
                cellEl.classList.add('correct');
            } else {
                cellEl.classList.remove('correct');
                cellEl.classList.add('wrong');
            }
        }
    }

    const resultEl = document.getElementById('crossword-result');
    const pct = totalCells > 0 ? Math.round((correctCells / totalCells) * 100) : 0;

    if (correctCells === totalCells) {
        resultEl.style.display = 'block';
        document.getElementById('cw-result-title').textContent = '🎉 Tuyệt vời!';
        document.getElementById('cw-result-text').textContent = `Bạn đã giải đúng tất cả ${totalCells} ô!`;
    } else {
        resultEl.style.display = 'block';
        document.getElementById('cw-result-title').textContent = '💪 Gần đúng rồi!';
        document.getElementById('cw-result-text').textContent =
            `Đúng ${correctCells}/${totalCells} ô (${pct}%). Các ô đỏ cần sửa lại.`;
    }
}

// Auto-start first crossword
document.addEventListener('DOMContentLoaded', function() {
    if (typeof CROSSWORDS_DATA !== 'undefined' && CROSSWORDS_DATA.length > 0) {
        startCrossword();
    }
});
