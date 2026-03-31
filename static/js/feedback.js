/**
 * Feedback system for reporting incorrect vocabulary data.
 * Saves feedback to localStorage and supports export to downloadable JSON file.
 */

const FeedbackSystem = (function () {
    const STORAGE_KEY = 'vocab_feedback';

    function escapeHtml(text) {
        var div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    function loadFeedback() {
        try {
            return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
        } catch (e) {
            return [];
        }
    }

    function saveFeedback(feedbackList) {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(feedbackList));
    }

    function addFeedback(entry) {
        const list = loadFeedback();
        entry.id = generateId();
        entry.created_at = new Date().toISOString();
        entry.status = 'pending';
        list.push(entry);
        saveFeedback(list);
        updateBadge();
        return entry;
    }

    function generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2, 6);
    }

    function getFeedbackCount() {
        return loadFeedback().length;
    }

    function updateBadge() {
        const badge = document.getElementById('feedback-export-count');
        if (badge) {
            const count = getFeedbackCount();
            badge.textContent = count;
            badge.style.display = count > 0 ? 'inline-block' : 'none';
        }
    }

    function exportFeedback() {
        const list = loadFeedback();
        if (list.length === 0) {
            alert('Chưa có phản hồi nào để xuất.');
            return;
        }
        const data = {
            exported_at: new Date().toISOString(),
            count: list.length,
            feedback: list
        };
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        const uniqueName = 'feedback_' + Date.now() + '_' + Math.random().toString(36).substr(2, 6) + '.json';
        a.href = url;
        a.download = uniqueName;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    function clearFeedback() {
        if (confirm('Xóa tất cả phản hồi đã lưu?')) {
            localStorage.removeItem(STORAGE_KEY);
            updateBadge();
        }
    }

    function openFeedbackModal(wordData) {
        closeFeedbackModal();
        var overlay = document.createElement('div');
        overlay.id = 'feedback-overlay';
        overlay.className = 'feedback-overlay';
        overlay.onclick = function (e) {
            if (e.target === overlay) closeFeedbackModal();
        };

        var fieldOptions = [
            { value: 'image', label: '🖼️ Hình ảnh (image)' },
            { value: 'meaning', label: '📝 Nghĩa (meaning)' },
            { value: 'example', label: '📖 Ví dụ (example)' },
            { value: 'phonetic', label: '🔊 Phiên âm (phonetic)' },
            { value: 'hint', label: '💡 Gợi ý (hint)' },
            { value: 'word', label: '🔤 Từ vựng (word)' },
            { value: 'other', label: '❓ Khác (other)' }
        ];

        var optionsHtml = fieldOptions.map(function (opt) {
            return '<option value="' + opt.value + '">' + opt.label + '</option>';
        }).join('');

        var currentValue = '';
        var selectedField = fieldOptions[0].value;
        if (wordData && wordData[selectedField] !== undefined) {
            currentValue = wordData[selectedField];
        }

        var modal = document.createElement('div');
        modal.className = 'feedback-modal';
        modal.innerHTML =
            '<div class="feedback-modal-header">' +
                '<h3>⚠️ Báo lỗi từ vựng</h3>' +
                '<button class="feedback-close-btn" onclick="FeedbackSystem.closeFeedbackModal()">&times;</button>' +
            '</div>' +
            '<div class="feedback-modal-body">' +
                '<div class="feedback-word-info">' +
                    '<strong>' + escapeHtml(wordData.word) + '</strong> — ' + escapeHtml(wordData.meaning) +
                '</div>' +
                '<div class="feedback-field-group">' +
                    '<label for="feedback-field">Trường bị lỗi:</label>' +
                    '<select id="feedback-field" onchange="FeedbackSystem.onFieldChange()">' + optionsHtml + '</select>' +
                '</div>' +
                '<div class="feedback-field-group">' +
                    '<label>Giá trị hiện tại:</label>' +
                    '<div id="feedback-current-value" class="feedback-current-value">' + escapeHtml(String(currentValue)) + '</div>' +
                '</div>' +
                '<div class="feedback-field-group">' +
                    '<label for="feedback-comment">Mô tả lỗi:</label>' +
                    '<textarea id="feedback-comment" rows="2" placeholder="Mô tả lỗi bạn phát hiện..."></textarea>' +
                '</div>' +
                '<div class="feedback-field-group">' +
                    '<label for="feedback-suggestion">Gợi ý sửa:</label>' +
                    '<input type="text" id="feedback-suggestion" placeholder="Giá trị đúng nên là...">' +
                '</div>' +
            '</div>' +
            '<div class="feedback-modal-footer">' +
                '<button class="btn btn-sm btn-secondary" onclick="FeedbackSystem.closeFeedbackModal()">Hủy</button>' +
                '<button class="btn btn-sm btn-primary" onclick="FeedbackSystem.submitFeedback()">Gửi phản hồi</button>' +
            '</div>';

        overlay.appendChild(modal);
        document.body.appendChild(overlay);

        // Store word data for submission
        overlay.dataset.wordJson = JSON.stringify(wordData);
    }

    function onFieldChange() {
        var overlay = document.getElementById('feedback-overlay');
        if (!overlay) return;
        var wordData = JSON.parse(overlay.dataset.wordJson);
        var field = document.getElementById('feedback-field').value;
        var currentEl = document.getElementById('feedback-current-value');
        var val = wordData[field];
        currentEl.textContent = val !== undefined ? String(val) : '(không có)';
    }

    function submitFeedback() {
        var overlay = document.getElementById('feedback-overlay');
        if (!overlay) return;
        var wordData = JSON.parse(overlay.dataset.wordJson);
        var field = document.getElementById('feedback-field').value;
        var comment = document.getElementById('feedback-comment').value.trim();
        var suggestion = document.getElementById('feedback-suggestion').value.trim();

        if (!comment && !suggestion) {
            alert('Vui lòng nhập mô tả lỗi hoặc gợi ý sửa.');
            return;
        }

        var entry = {
            level: wordData._level,
            topic: wordData._topic,
            word: wordData.word,
            field: field,
            current_value: wordData[field] !== undefined ? String(wordData[field]) : '',
            comment: comment,
            suggestion: suggestion
        };

        addFeedback(entry);
        closeFeedbackModal();
        showToast('✅ Đã lưu phản hồi!');
    }

    function closeFeedbackModal() {
        var overlay = document.getElementById('feedback-overlay');
        if (overlay) overlay.remove();
    }

    function showToast(message) {
        var toast = document.createElement('div');
        toast.className = 'feedback-toast';
        toast.textContent = message;
        document.body.appendChild(toast);
        setTimeout(function () {
            toast.classList.add('feedback-toast-hide');
            setTimeout(function () { toast.remove(); }, 300);
        }, 2000);
    }

    // Init badge and event delegation on load
    document.addEventListener('DOMContentLoaded', function () {
        updateBadge();
        document.addEventListener('click', function (e) {
            var btn = e.target.closest('.feedback-report-btn');
            if (btn && btn.dataset.word) {
                var wordData = JSON.parse(btn.dataset.word);
                openFeedbackModal(wordData);
            }
        });
    });

    return {
        openFeedbackModal: openFeedbackModal,
        closeFeedbackModal: closeFeedbackModal,
        submitFeedback: submitFeedback,
        onFieldChange: onFieldChange,
        exportFeedback: exportFeedback,
        clearFeedback: clearFeedback,
        getFeedbackCount: getFeedbackCount,
        updateBadge: updateBadge
    };
})();
