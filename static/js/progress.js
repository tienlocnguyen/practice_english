/**
 * Progress View - Shows user progress across all levels with medals and download
 */

/* Medal thresholds */
function getMedal(passedCount, totalCount) {
    if (totalCount === 0) return null;
    if (passedCount === totalCount) return { emoji: '🥇', label: 'Huy chương Vàng', labelVi: 'Xuất sắc!', cls: 'medal-gold' };
    if (passedCount >= totalCount * 0.5) return { emoji: '🥈', label: 'Huy chương Bạc', labelVi: 'Tốt lắm!', cls: 'medal-silver' };
    if (passedCount > 0) return { emoji: '🥉', label: 'Huy chương Đồng', labelVi: 'Cố gắng thêm!', cls: 'medal-bronze' };
    return null;
}

function renderProgress() {
    var container = document.getElementById('progress-content');
    if (!container) return;

    var user = UserSystem.getCurrentUser();
    if (!user) {
        container.textContent = 'Vui lòng đăng nhập để xem tiến trình.';
        return;
    }

    while (container.firstChild) container.removeChild(container.firstChild);

    var results = UserSystem.getAllResults();
    var allLevels = typeof ALL_LEVELS !== 'undefined' ? ALL_LEVELS : [];

    /* Overall stats */
    var totalPassed = 0;
    var totalTopics = 0;
    var totalExams = 0;

    for (var key in results) {
        if (results.hasOwnProperty(key)) {
            totalExams++;
            if (results[key].passed) totalPassed++;
        }
    }

    /* User header */
    var header = document.createElement('div');
    header.className = 'progress-user-header';

    var avatar = document.createElement('div');
    avatar.className = 'progress-avatar';
    avatar.textContent = '👤';
    header.appendChild(avatar);

    var userName = document.createElement('h2');
    userName.className = 'progress-user-name';
    userName.textContent = user;
    header.appendChild(userName);

    var statsRow = document.createElement('div');
    statsRow.className = 'progress-stats-row';

    var statExams = document.createElement('div');
    statExams.className = 'progress-stat';
    var statExamsNum = document.createElement('div');
    statExamsNum.className = 'stat-number';
    statExamsNum.textContent = totalExams;
    var statExamsLabel = document.createElement('div');
    statExamsLabel.className = 'stat-label';
    statExamsLabel.textContent = 'Đã thi';
    statExams.appendChild(statExamsNum);
    statExams.appendChild(statExamsLabel);
    statsRow.appendChild(statExams);

    var statPassed = document.createElement('div');
    statPassed.className = 'progress-stat';
    var statPassedNum = document.createElement('div');
    statPassedNum.className = 'stat-number stat-success';
    statPassedNum.textContent = totalPassed;
    var statPassedLabel = document.createElement('div');
    statPassedLabel.className = 'stat-label';
    statPassedLabel.textContent = 'Đạt';
    statPassed.appendChild(statPassedNum);
    statPassed.appendChild(statPassedLabel);
    statsRow.appendChild(statPassed);

    var statFailed = document.createElement('div');
    statFailed.className = 'progress-stat';
    var statFailedNum = document.createElement('div');
    statFailedNum.className = 'stat-number stat-danger';
    statFailedNum.textContent = totalExams - totalPassed;
    var statFailedLabel = document.createElement('div');
    statFailedLabel.className = 'stat-label';
    statFailedLabel.textContent = 'Chưa đạt';
    statFailed.appendChild(statFailedNum);
    statFailed.appendChild(statFailedLabel);
    statsRow.appendChild(statFailed);

    header.appendChild(statsRow);
    container.appendChild(header);

    /* Medal showcase */
    var medalSection = document.createElement('div');
    medalSection.className = 'medal-showcase';

    var medalTitle = document.createElement('h3');
    medalTitle.className = 'section-title';
    medalTitle.textContent = '🏆 Bộ sưu tập Huy chương';
    medalSection.appendChild(medalTitle);

    var medalGrid = document.createElement('div');
    medalGrid.className = 'medal-grid';
    var hasMedals = false;

    for (var l = 0; l < allLevels.length; l++) {
        var level = allLevels[l];
        var lvlPassed = 0;
        var lvlAttempted = 0;
        var lvlTotal = level.topics.length;

        for (var t = 0; t < level.topics.length; t++) {
            var topicId = level.topics[t].id;
            var r = results[level.level + '_' + topicId];
            if (r) {
                lvlAttempted++;
                if (r.passed) lvlPassed++;
            }
        }

        totalTopics += lvlTotal;
        var medal = getMedal(lvlPassed, lvlTotal);

        var medalCard = document.createElement('div');
        medalCard.className = 'medal-card' + (medal ? ' ' + medal.cls : ' medal-locked');

        var medalEmoji = document.createElement('div');
        medalEmoji.className = 'medal-emoji';
        medalEmoji.textContent = medal ? medal.emoji : '🔒';
        medalCard.appendChild(medalEmoji);

        var medalName = document.createElement('div');
        medalName.className = 'medal-level-name';
        medalName.textContent = level.label;
        medalCard.appendChild(medalName);

        if (medal) {
            hasMedals = true;
            var medalLabel = document.createElement('div');
            medalLabel.className = 'medal-label';
            medalLabel.textContent = medal.label;
            medalCard.appendChild(medalLabel);

            var medalSub = document.createElement('div');
            medalSub.className = 'medal-sub';
            medalSub.textContent = lvlPassed + '/' + lvlTotal + ' chủ đề — ' + medal.labelVi;
            medalCard.appendChild(medalSub);
        } else {
            var medalLabel = document.createElement('div');
            medalLabel.className = 'medal-label';
            medalLabel.textContent = lvlAttempted > 0 ? '0/' + lvlTotal + ' đạt' : 'Chưa thi';
            medalCard.appendChild(medalLabel);
        }

        medalGrid.appendChild(medalCard);
    }

    medalSection.appendChild(medalGrid);

    if (!hasMedals) {
        var noMedal = document.createElement('p');
        noMedal.className = 'no-medals-hint';
        noMedal.textContent = '💡 Hãy làm bài kiểm tra để nhận huy chương đầu tiên!';
        medalSection.appendChild(noMedal);
    }

    container.appendChild(medalSection);

    /* Per-level progress details */
    var detailSection = document.createElement('div');
    detailSection.className = 'progress-details';

    var detailTitle = document.createElement('h3');
    detailTitle.className = 'section-title';
    detailTitle.textContent = '📊 Chi tiết theo cấp độ';
    detailSection.appendChild(detailTitle);

    for (var l2 = 0; l2 < allLevels.length; l2++) {
        var lvl = allLevels[l2];
        var levelCard = document.createElement('div');
        levelCard.className = 'progress-level-card';

        var levelHeader = document.createElement('div');
        levelHeader.className = 'progress-level-header';

        var levelName = document.createElement('h4');
        levelName.textContent = '📖 ' + lvl.label;
        levelHeader.appendChild(levelName);

        /* Level medal inline */
        var lvlP = 0;
        for (var t2 = 0; t2 < lvl.topics.length; t2++) {
            var r2 = results[lvl.level + '_' + lvl.topics[t2].id];
            if (r2 && r2.passed) lvlP++;
        }
        var lvlMedal = getMedal(lvlP, lvl.topics.length);
        if (lvlMedal) {
            var inlineMedal = document.createElement('span');
            inlineMedal.className = 'level-medal-inline';
            inlineMedal.textContent = lvlMedal.emoji + ' ' + lvlMedal.label;
            levelHeader.appendChild(inlineMedal);
        }

        levelCard.appendChild(levelHeader);

        var topicList = document.createElement('div');
        topicList.className = 'progress-topic-list';

        for (var t3 = 0; t3 < lvl.topics.length; t3++) {
            var topic = lvl.topics[t3];
            var topicResult = results[lvl.level + '_' + topic.id];

            var topicRow = document.createElement('div');
            topicRow.className = 'progress-topic-row' + (topicResult ? (topicResult.passed ? ' passed' : ' failed') : '');

            var topicName = document.createElement('span');
            topicName.className = 'progress-topic-name';
            topicName.textContent = topic.icon + ' ' + topic.name_vi;
            topicRow.appendChild(topicName);

            if (topicResult) {
                var topicScore = document.createElement('span');
                topicScore.className = 'progress-topic-score';
                topicScore.textContent = topicResult.score + '/' + topicResult.total + ' (' + topicResult.percentage + '%)';
                topicRow.appendChild(topicScore);

                var topicBadge = document.createElement('span');
                topicBadge.className = 'topic-result-badge ' + (topicResult.passed ? 'badge-pass' : 'badge-fail');
                topicBadge.textContent = topicResult.passed ? 'PASS' : 'NOT PASS';
                topicRow.appendChild(topicBadge);

                var topicDate = document.createElement('span');
                topicDate.className = 'progress-topic-date';
                try {
                    topicDate.textContent = new Date(topicResult.date).toLocaleDateString('vi-VN');
                } catch(e) {
                    topicDate.textContent = '';
                }
                topicRow.appendChild(topicDate);
            } else {
                var noResult = document.createElement('span');
                noResult.className = 'progress-topic-no-result';
                noResult.textContent = '— Chưa thi —';
                topicRow.appendChild(noResult);
            }

            topicList.appendChild(topicRow);
        }

        levelCard.appendChild(topicList);
        detailSection.appendChild(levelCard);
    }

    container.appendChild(detailSection);
}

function downloadProgress() {
    var user = UserSystem.getCurrentUser();
    if (!user) {
        UserSystem.showLogin();
        return;
    }

    var results = UserSystem.getAllResults();
    var allLevels = typeof ALL_LEVELS !== 'undefined' ? ALL_LEVELS : [];

    var exportData = {
        user: user,
        exportDate: new Date().toISOString(),
        medals: [],
        levels: []
    };

    for (var l = 0; l < allLevels.length; l++) {
        var level = allLevels[l];
        var lvlPassed = 0;
        var topics = [];

        for (var t = 0; t < level.topics.length; t++) {
            var topic = level.topics[t];
            var r = results[level.level + '_' + topic.id];
            if (r && r.passed) lvlPassed++;
            topics.push({
                name: topic.name_vi,
                result: r || null
            });
        }

        var medal = getMedal(lvlPassed, level.topics.length);
        if (medal) {
            exportData.medals.push({
                level: level.label,
                medal: medal.emoji + ' ' + medal.label,
                passed: lvlPassed,
                total: level.topics.length
            });
        }

        exportData.levels.push({
            level: level.label,
            medal: medal ? medal.emoji + ' ' + medal.label : null,
            passedTopics: lvlPassed,
            totalTopics: level.topics.length,
            topics: topics
        });
    }

    var blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = 'progress_' + user + '_' + new Date().toISOString().slice(0, 10) + '.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

/* Init */
document.addEventListener('DOMContentLoaded', function () {
    /* Small delay ensures user.js has initialized */
    setTimeout(function () {
        renderProgress();
        if (typeof UserSystem !== 'undefined') {
            UserSystem.onChange(renderProgress);
        }
    }, 50);
});
