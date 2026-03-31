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

function buildExamQuestions(topicsData, questionsPerTopic) {
    questionsPerTopic = questionsPerTopic || 3;
    var questions = [];
    var allWords = getAllWords(topicsData);

    for (var t = 0; t < topicsData.length; t++) {
        var topic = topicsData[t];
        var words = shuffle([].concat(topic.words));
        var count = Math.min(questionsPerTopic, words.length);

        for (var i = 0; i < count; i++) {
            var word = words[i];
            var type = Math.floor(Math.random() * 3);
            var wrongWords = shuffle(allWords.filter(function (w) { return w.word !== word.word; }));

            if (type === 0) {
                /* Image → pick word */
                questions.push({
                    topicId: topic.id,
                    topicName: topic.name_vi,
                    type: 'image-to-word',
                    prompt: word.image,
                    promptLabel: word.meaning,
                    correctAnswer: word.word,
                    options: shuffle([word.word].concat(wrongWords.slice(0, 3).map(function (w) { return w.word; })))
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
                    options: shuffle([word.word].concat(wrongWords.slice(0, 3).map(function (w) { return w.word; })))
                });
            } else {
                /* Word → pick meaning */
                questions.push({
                    topicId: topic.id,
                    topicName: topic.name_vi,
                    type: 'word-to-meaning',
                    prompt: word.word,
                    promptLabel: word.phonetic,
                    correctAnswer: word.meaning,
                    options: shuffle([word.meaning].concat(wrongWords.slice(0, 3).map(function (w) { return w.meaning; })))
                });
            }
        }
    }
    return shuffle(questions);
}

function startExam() {
    if (!UserSystem.getCurrentUser()) {
        UserSystem.showLogin();
        return;
    }

    var questions = buildExamQuestions(TOPICS_DATA, 3);
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
    if (fill) fill.style.width = ((examState.currentIndex / total) * 100) + '%';
}

function showExamQuestion() {
    var q = examState.questions[examState.currentIndex];
    var area = document.getElementById('exam-question-area');

    examState.currentOptions = q.options;
    examState.currentCorrect = q.correctAnswer;

    var promptHtml = '';
    if (q.type === 'image-to-word') {
        promptHtml =
            '<div class="question-image">' + escapeHtml(q.prompt) + '</div>' +
            '<div class="question-meaning">\uD83D\uDCA1 ' + escapeHtml(q.promptLabel) + '</div>';
    } else if (q.type === 'meaning-to-word') {
        promptHtml = '<div class="exam-prompt-text">\uD83D\uDCD6 ' + escapeHtml(q.prompt) + '</div>';
    } else {
        promptHtml =
            '<div class="question-word">' + escapeHtml(q.prompt) + '</div>' +
            '<div class="question-meaning">' + escapeHtml(q.promptLabel) + '</div>';
    }

    var optionsHtml = '';
    for (var i = 0; i < q.options.length; i++) {
        optionsHtml += '<button class="option-btn exam-opt" data-idx="' + i + '">' + escapeHtml(q.options[i]) + '</button>';
    }

    area.innerHTML =
        '<div class="animate-fadeIn">' +
        '<div class="exam-topic-badge">' + escapeHtml(q.topicName) + '</div>' +
        promptHtml +
        '<div class="options-grid">' + optionsHtml + '</div>' +
        '</div>';

    area.querySelectorAll('.exam-opt').forEach(function (btn) {
        btn.addEventListener('click', function () {
            handleExamOptionClick(this);
        });
    });
}

function handleExamOptionClick(btn) {
    if (!examState.isActive) return;
    examState.isActive = false; /* prevent double-click */

    var idx = parseInt(btn.dataset.idx, 10);
    var selected = examState.currentOptions[idx];
    var correct = examState.currentCorrect;

    var buttons = document.querySelectorAll('.exam-opt');
    buttons.forEach(function (b) { b.classList.add('disabled'); });

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

    /* Save results and build result HTML */
    var totalCorrect = 0;
    var totalQuestions = 0;
    var resultsHtml = '';
    var levelId = (typeof LEVEL_ID !== 'undefined') ? LEVEL_ID : '';

    for (var t = 0; t < TOPICS_DATA.length; t++) {
        var topic = TOPICS_DATA[t];
        var result = topicResults[topic.id];
        if (!result) continue;

        totalCorrect += result.correct;
        totalQuestions += result.total;

        var pct = Math.round((result.correct / result.total) * 100);
        var passed = pct >= 70;

        UserSystem.saveExamResult(levelId, topic.id, result.correct, result.total);

        resultsHtml +=
            '<div class="exam-topic-result ' + (passed ? 'passed' : 'failed') + '">' +
            '<span class="topic-result-icon">' + (passed ? '✅' : '❌') + '</span>' +
            '<span class="topic-result-name">' + topic.icon + ' ' + topic.name_vi + '</span>' +
            '<span class="topic-result-score">' + result.correct + '/' + result.total + '</span>' +
            '<span class="topic-result-badge ' + (passed ? 'badge-pass' : 'badge-fail') + '">' + (passed ? 'PASS' : 'NOT PASS') + '</span>' +
            '</div>';
    }

    var overallPct = totalQuestions > 0 ? Math.round((totalCorrect / totalQuestions) * 100) : 0;
    var overallPassed = overallPct >= 70;

    resultArea.innerHTML =
        '<div class="result-card exam-result-card">' +
        '<h2>' + (overallPassed ? '🎉 Chúc mừng!' : '💪 Cố gắng thêm!') + '</h2>' +
        '<p class="exam-overall-score">Tổng điểm: ' + totalCorrect + '/' + totalQuestions + ' (' + overallPct + '%)</p>' +
        '<div class="exam-overall-badge ' + (overallPassed ? 'badge-pass' : 'badge-fail') + '">' +
        (overallPassed ? '✅ PASS' : '❌ NOT PASS') +
        '</div>' +
        '<h3>📊 Kết quả theo chủ đề:</h3>' +
        '<div class="exam-topic-results">' + resultsHtml + '</div>' +
        '<div class="exam-result-actions">' +
        '<button class="btn btn-primary" onclick="startExam()">🔄 Thi lại</button>' +
        '<a href="index.html" class="btn btn-secondary">← Quay lại</a>' +
        '</div>' +
        '</div>';
}
