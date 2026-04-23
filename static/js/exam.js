/**
 * Exam Engine - Tests vocabulary from all topics in a level
 * Gives pass/not-pass verdict per topic
 */

var examState = {
    questions: [],
    currentIndex: 0,
    currentOptions: [],
    currentCorrect: '',
    answers: [],
    isActive: false
};

function buildExamQuestions(topicsData, questionsPerTopic, includeWrite) {
    questionsPerTopic = questionsPerTopic || 3;
    includeWrite = includeWrite !== false; /* default true */
    var questions = [];
    var allWords = getAllWords(topicsData);
    /* Question types: 0=image→word, 1=meaning→word, 2=word→meaning, 3=meaning→write */
    var NUM_TYPES = includeWrite ? 4 : 3;

    for (var t = 0; t < topicsData.length; t++) {
        var topic = topicsData[t];
        var words = shuffle([].concat(topic.words));
        var count = Math.min(questionsPerTopic, words.length);

        for (var i = 0; i < count; i++) {
            var word = words[i];
            var type = Math.floor(Math.random() * NUM_TYPES);
            var wrongWords = shuffle(allWords.filter(function (w) { return w.word !== word.word; })).slice(0, 3);

            if (type === 0) {
                /* Image → pick word */
                questions.push({
                    topicId: topic.id,
                    topicName: topic.name_vi,
                    type: 'image-to-word',
                    prompt: word.image,
                    promptLabel: word.meaning,
                    correctAnswer: word.word,
                    options: shuffle([word.word].concat(wrongWords.map(function (w) { return w.word; })))
                });
            } else if (type === 1) {
                /* Meaning → pick word */
                questions.push({
                    topicId: topic.id,
                    topicName: topic.name_vi,
                    type: 'meaning-to-word',
                    prompt: word.meaning,
                    promptLabel: '',
                    correctAnswer: word.word,
                    options: shuffle([word.word].concat(wrongWords.map(function (w) { return w.word; })))
                });
            } else if (type === 2) {
                /* Word → pick meaning */
                questions.push({
                    topicId: topic.id,
                    topicName: topic.name_vi,
                    type: 'word-to-meaning',
                    prompt: word.word,
                    promptLabel: word.phonetic,
                    correctAnswer: word.meaning,
                    options: shuffle([word.meaning].concat(wrongWords.map(function (w) { return w.meaning; })))
                });
            } else {
                /* Meaning (Vietnamese) → type English word */
                questions.push({
                    topicId: topic.id,
                    topicName: topic.name_vi,
                    type: 'meaning-to-write',
                    prompt: word.meaning,
                    promptLabel: word.phonetic,
                    correctAnswer: word.word,
                    options: []
                });
            }
        }
    }
    return shuffle(questions);
}

function startExam() {
    /* Topic exam mode: skip login, use all words, include write type */
    var isTopicMode = (typeof TOPIC_EXAM_MODE !== 'undefined') && TOPIC_EXAM_MODE;

    if (!isTopicMode) {
        if (!UserSystem.getCurrentUser()) {
            UserSystem.showLogin();
            return;
        }
    }

    var qPerTopic = isTopicMode ? Math.max(TOPICS_DATA[0].words.length, 6) : 3;
    var questions = buildExamQuestions(TOPICS_DATA, qPerTopic, true);
    examState = {
        questions: questions,
        currentIndex: 0,
        currentOptions: [],
        currentCorrect: '',
        answers: [],
        isActive: true
    };

    document.getElementById('exam-intro').style.display = 'none';
    document.getElementById('exam-area').style.display = 'block';
    document.getElementById('exam-result').style.display = 'none';

    updateExamProgress();
    showExamQuestion();
}

function updateExamProgress() {
    var qNum = examState.currentIndex + 1;
    var total = examState.questions.length;
    var el = document.getElementById('exam-progress-text');
    if (el) el.textContent = 'Câu ' + qNum + '/' + total;
    var fill = document.getElementById('exam-progress-fill');
    if (fill) fill.style.width = ((qNum / total) * 100) + '%';
}

function showExamQuestion() {
    var q = examState.questions[examState.currentIndex];
    var area = document.getElementById('exam-question-area');

    examState.currentOptions = q.options;
    examState.currentCorrect = q.correctAnswer;

    var wrapper = document.createElement('div');
    wrapper.className = 'animate-fadeIn';

    var topicBadge = document.createElement('div');
    topicBadge.className = 'exam-topic-badge';
    topicBadge.textContent = q.topicName;
    wrapper.appendChild(topicBadge);

    if (q.type === 'image-to-word') {
        var imgDiv = document.createElement('div');
        imgDiv.className = 'question-image';
        imgDiv.textContent = q.prompt;
        wrapper.appendChild(imgDiv);
        var meaningDiv = document.createElement('div');
        meaningDiv.className = 'question-meaning';
        meaningDiv.textContent = '\uD83D\uDCA1 ' + q.promptLabel;
        wrapper.appendChild(meaningDiv);
    } else if (q.type === 'meaning-to-word') {
        var promptDiv = document.createElement('div');
        promptDiv.className = 'exam-prompt-text';
        promptDiv.textContent = '\uD83D\uDCD6 ' + q.prompt;
        wrapper.appendChild(promptDiv);
    } else if (q.type === 'meaning-to-write') {
        /* Vietnamese meaning → type English word */
        var writeLabel = document.createElement('p');
        writeLabel.className = 'exam-write-label';
        writeLabel.textContent = 'Viết từ tiếng Anh có nghĩa là:';
        wrapper.appendChild(writeLabel);

        var meaningBox = document.createElement('div');
        meaningBox.className = 'exam-write-meaning';
        meaningBox.textContent = q.prompt;
        wrapper.appendChild(meaningBox);

        if (q.promptLabel) {
            var phoneticP = document.createElement('p');
            phoneticP.className = 'exam-write-phonetic';
            phoneticP.textContent = q.promptLabel;
            wrapper.appendChild(phoneticP);
        }

        var writeRow = document.createElement('div');
        writeRow.className = 'exam-write-row';

        var writeInput = document.createElement('input');
        writeInput.type = 'text';
        writeInput.id = 'exam-write-input';
        writeInput.className = 'exam-write-input';
        writeInput.placeholder = 'Nhập từ tiếng Anh...';
        writeInput.setAttribute('autocomplete', 'off');
        writeInput.setAttribute('autocorrect', 'off');
        writeInput.setAttribute('autocapitalize', 'off');
        writeInput.setAttribute('spellcheck', 'false');

        var writeBtn = document.createElement('button');
        writeBtn.className = 'btn btn-primary';
        writeBtn.textContent = '✅ Kiểm tra';

        writeRow.appendChild(writeInput);
        writeRow.appendChild(writeBtn);
        wrapper.appendChild(writeRow);

        while (area.firstChild) area.removeChild(area.firstChild);
        area.appendChild(wrapper);

        writeBtn.addEventListener('click', checkExamWrite);
        writeInput.addEventListener('keydown', function (e) {
            if (e.key === 'Enter') checkExamWrite();
        });
        setTimeout(function () { writeInput.focus(); }, 80);
        return; /* skip options grid for write type */
    } else {
        var wordDiv = document.createElement('div');
        wordDiv.className = 'question-word';
        wordDiv.textContent = q.prompt;
        wrapper.appendChild(wordDiv);
        var meaningDiv2 = document.createElement('div');
        meaningDiv2.className = 'question-meaning';
        meaningDiv2.textContent = q.promptLabel;
        wrapper.appendChild(meaningDiv2);
    }

    var optionsGrid = document.createElement('div');
    optionsGrid.className = 'options-grid';
    for (var i = 0; i < q.options.length; i++) {
        var optBtn = document.createElement('button');
        optBtn.className = 'option-btn exam-opt';
        optBtn.setAttribute('data-idx', i);
        optBtn.textContent = q.options[i];
        optionsGrid.appendChild(optBtn);
    }
    wrapper.appendChild(optionsGrid);

    while (area.firstChild) area.removeChild(area.firstChild);
    area.appendChild(wrapper);

    area.querySelectorAll('.exam-opt').forEach(function (btn) {
        btn.addEventListener('click', function () {
            handleExamOptionClick(this);
        });
    });
}

function checkExamWrite() {
    if (!examState.isActive) return;

    var input = document.getElementById('exam-write-input');
    if (!input) return;

    var userAnswer = input.value.trim().toLowerCase();
    var correct = examState.currentCorrect.trim().toLowerCase();

    examState.isActive = false;
    input.disabled = true;

    var writeRow = input.parentElement;
    var isCorrect = userAnswer === correct;

    var feedback = document.createElement('div');
    feedback.className = 'exam-write-feedback ' + (isCorrect ? 'vte-correct' : 'vte-wrong');

    var q = examState.questions[examState.currentIndex];
    if (isCorrect) {
        feedback.innerHTML = '✅ Đúng rồi! <strong>' + escapeHtml(q.correctAnswer) + '</strong>';
    } else {
        feedback.innerHTML = '❌ Sai rồi! Đáp án đúng: <strong>' + escapeHtml(q.correctAnswer) + '</strong>'
            + (userAnswer ? ' (bạn viết: <em>' + escapeHtml(input.value.trim()) + '</em>)' : '');
    }
    writeRow.insertAdjacentElement('afterend', feedback);

    examState.answers.push({
        topicId: q.topicId,
        correct: isCorrect
    });

    setTimeout(function () {
        examState.currentIndex++;
        examState.isActive = true;
        if (examState.currentIndex < examState.questions.length) {
            updateExamProgress();
            showExamQuestion();
        } else {
            examState.isActive = false;
            showExamResult();
        }
    }, 1200);
}

function handleExamOptionClick(btn) {
    if (!examState.isActive) return;
    examState.isActive = false; /* prevent double-click */

    var idx = parseInt(btn.dataset.idx, 10);
    var selected = examState.currentOptions[idx];
    var correct = examState.currentCorrect;

    var buttons = document.querySelectorAll('.exam-opt');
    buttons.forEach(function (b) {
        b.classList.add('disabled');
        b.disabled = true;
    });

    var q = examState.questions[examState.currentIndex];
    var isCorrect = selected === correct;

    examState.answers.push({
        topicId: q.topicId,
        correct: isCorrect
    });

    if (isCorrect) {
        btn.classList.add('correct');
    } else {
        btn.classList.add('wrong');
        var correctIdx = examState.currentOptions.indexOf(correct);
        buttons.forEach(function (b) {
            if (parseInt(b.dataset.idx, 10) === correctIdx) b.classList.add('correct');
        });
    }

    setTimeout(function () {
        examState.currentIndex++;
        examState.isActive = true;
        if (examState.currentIndex < examState.questions.length) {
            updateExamProgress();
            showExamQuestion();
        } else {
            examState.isActive = false;
            showExamResult();
        }
    }, 1000);
}

function showExamResult() {
    document.getElementById('exam-area').style.display = 'none';
    var resultArea = document.getElementById('exam-result');
    resultArea.style.display = 'block';

    /* Calculate per-topic results */
    var topicResults = {};
    for (var i = 0; i < examState.answers.length; i++) {
        var ans = examState.answers[i];
        if (!topicResults[ans.topicId]) topicResults[ans.topicId] = { correct: 0, total: 0 };
        topicResults[ans.topicId].total++;
        if (ans.correct) topicResults[ans.topicId].correct++;
    }

    /* Save results and build result via DOM */
    var totalCorrect = 0;
    var totalQuestions = 0;
    var levelId = (typeof LEVEL_ID !== 'undefined') ? LEVEL_ID : '';

    var card = document.createElement('div');
    card.className = 'result-card exam-result-card';

    var topicResultsContainer = document.createElement('div');
    topicResultsContainer.className = 'exam-topic-results';

    for (var t = 0; t < TOPICS_DATA.length; t++) {
        var topic = TOPICS_DATA[t];
        var result = topicResults[topic.id];
        if (!result) continue;

        totalCorrect += result.correct;
        totalQuestions += result.total;

        var pct = Math.round((result.correct / result.total) * 100);
        var passed = pct >= 70;

        UserSystem.saveExamResult(levelId, topic.id, result.correct, result.total);

        var row = document.createElement('div');
        row.className = 'exam-topic-result ' + (passed ? 'passed' : 'failed');

        var iconSpan = document.createElement('span');
        iconSpan.className = 'topic-result-icon';
        iconSpan.textContent = passed ? '✅' : '❌';
        row.appendChild(iconSpan);

        var nameSpan = document.createElement('span');
        nameSpan.className = 'topic-result-name';
        nameSpan.textContent = topic.icon + ' ' + topic.name_vi;
        row.appendChild(nameSpan);

        var scoreSpan = document.createElement('span');
        scoreSpan.className = 'topic-result-score';
        scoreSpan.textContent = result.correct + '/' + result.total;
        row.appendChild(scoreSpan);

        var badgeSpan = document.createElement('span');
        badgeSpan.className = 'topic-result-badge ' + (passed ? 'badge-pass' : 'badge-fail');
        badgeSpan.textContent = passed ? 'PASS' : 'NOT PASS';
        row.appendChild(badgeSpan);

        topicResultsContainer.appendChild(row);
    }

    var overallPct = totalQuestions > 0 ? Math.round((totalCorrect / totalQuestions) * 100) : 0;
    var overallPassed = overallPct >= 70;

    /* Medal for achievement */
    var passedCount = 0;
    var topicCount = 0;
    for (var t2 = 0; t2 < TOPICS_DATA.length; t2++) {
        var r = topicResults[TOPICS_DATA[t2].id];
        if (r) {
            topicCount++;
            if (Math.round((r.correct / r.total) * 100) >= 70) passedCount++;
        }
    }
    var medal = '';
    if (passedCount === topicCount && topicCount > 0) medal = '🥇';
    else if (passedCount >= topicCount * 0.5) medal = '🥈';
    else if (passedCount > 0) medal = '🥉';

    var h2 = document.createElement('h2');
    h2.textContent = overallPassed ? '🎉 Chúc mừng!' : '💪 Cố gắng thêm!';
    card.appendChild(h2);

    if (medal) {
        var medalDiv = document.createElement('div');
        medalDiv.className = 'exam-medal';
        medalDiv.textContent = medal;
        card.appendChild(medalDiv);

        var medalLabel = document.createElement('div');
        medalLabel.className = 'exam-medal-label';
        if (medal === '🥇') medalLabel.textContent = 'Huy chương Vàng — Xuất sắc!';
        else if (medal === '🥈') medalLabel.textContent = 'Huy chương Bạc — Tốt lắm!';
        else medalLabel.textContent = 'Huy chương Đồng — Cố gắng thêm!';
        card.appendChild(medalLabel);
    }

    var scoreP = document.createElement('p');
    scoreP.className = 'exam-overall-score';
    scoreP.textContent = 'Tổng điểm: ' + totalCorrect + '/' + totalQuestions + ' (' + overallPct + '%)';
    card.appendChild(scoreP);

    var overallBadge = document.createElement('div');
    overallBadge.className = 'exam-overall-badge ' + (overallPassed ? 'badge-pass' : 'badge-fail');
    overallBadge.textContent = overallPassed ? '✅ PASS' : '❌ NOT PASS';
    card.appendChild(overallBadge);

    var h3 = document.createElement('h3');
    h3.textContent = '📊 Kết quả theo chủ đề:';
    card.appendChild(h3);

    card.appendChild(topicResultsContainer);

    var actions = document.createElement('div');
    actions.className = 'exam-result-actions';

    var retryBtn = document.createElement('button');
    retryBtn.className = 'btn btn-primary';
    retryBtn.textContent = '🔄 Thi lại';
    retryBtn.addEventListener('click', function() { startExam(); });
    actions.appendChild(retryBtn);

    var backLink = document.createElement('a');
    backLink.href = 'index.html';
    backLink.className = 'btn btn-secondary';
    backLink.textContent = '← Quay lại';
    actions.appendChild(backLink);

    card.appendChild(actions);

    while (resultArea.firstChild) resultArea.removeChild(resultArea.firstChild);
    resultArea.appendChild(card);
}
