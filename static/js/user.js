/**
 * User System - Simple user selection without password
 * Stores current user and progress in localStorage
 */
const UserSystem = {
    STORAGE_KEY: 'ep_current_user',
    PROGRESS_KEY: 'ep_progress',
    DEFAULT_USERS: ['Linh', 'Long', 'Test'],
    _onChangeCallbacks: [],

    getCurrentUser() {
        return localStorage.getItem(this.STORAGE_KEY);
    },

    setCurrentUser(name) {
        localStorage.setItem(this.STORAGE_KEY, name);
        this.dismissLogin();
        this.updateNavbar();
        this._fireChange();
    },

    logout() {
        localStorage.removeItem(this.STORAGE_KEY);
        this.showLogin();
        this.updateNavbar();
        this._fireChange();
    },

    onChange(fn) {
        this._onChangeCallbacks.push(fn);
    },

    _fireChange() {
        for (var i = 0; i < this._onChangeCallbacks.length; i++) {
            try { this._onChangeCallbacks[i](); } catch(e) { console.error('UserSystem onChange error:', e); }
        }
    },

    /* ---- Progress management ---- */
    getProgress() {
        try {
            const data = localStorage.getItem(this.PROGRESS_KEY);
            return data ? JSON.parse(data) : {};
        } catch (e) {
            return {};
        }
    },

    saveExamResult(levelId, topicId, score, total) {
        const user = this.getCurrentUser();
        if (!user) return false;
        const progress = this.getProgress();
        if (!progress[user]) progress[user] = {};
        const key = levelId + '_' + topicId;
        const passed = (score / total) >= 0.7;
        progress[user][key] = {
            score: score,
            total: total,
            passed: passed,
            percentage: Math.round((score / total) * 100),
            date: new Date().toISOString()
        };
        localStorage.setItem(this.PROGRESS_KEY, JSON.stringify(progress));
        return passed;
    },

    getExamResult(levelId, topicId) {
        const user = this.getCurrentUser();
        if (!user) return null;
        const progress = this.getProgress();
        if (!progress[user]) return null;
        return progress[user][levelId + '_' + topicId] || null;
    },

    getAllResults() {
        const user = this.getCurrentUser();
        if (!user) return {};
        const progress = this.getProgress();
        return progress[user] || {};
    },

    /* ---- UI ---- */
    updateNavbar() {
        var el = document.getElementById('user-display');
        if (!el) return;
        var user = this.getCurrentUser();
        if (user) {
            el.innerHTML = '<span class="user-name">👤 ' + user + '</span>';
            el.style.display = 'flex';
            var switchBtn = document.getElementById('user-switch-btn');
            if (switchBtn) switchBtn.style.display = 'inline-block';
        } else {
            el.innerHTML = '';
            el.style.display = 'none';
            var switchBtn = document.getElementById('user-switch-btn');
            if (switchBtn) switchBtn.style.display = 'none';
        }
    },

    showLogin() {
        var overlay = document.getElementById('login-overlay');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.id = 'login-overlay';
            overlay.className = 'login-overlay';
            var btns = '';
            for (var i = 0; i < this.DEFAULT_USERS.length; i++) {
                var u = this.DEFAULT_USERS[i];
                btns += '<button class="btn btn-primary login-user-btn" data-user="' + u + '">' + u + '</button>';
            }
            overlay.innerHTML =
                '<div class="login-card">' +
                '<div class="login-icon">👤</div>' +
                '<h2>Chọn người dùng</h2>' +
                '<p>Chọn tên của bạn để bắt đầu học</p>' +
                '<div class="login-buttons">' + btns + '</div>' +
                '</div>';
            document.body.appendChild(overlay);
            overlay.querySelectorAll('.login-user-btn').forEach(function (btn) {
                btn.addEventListener('click', function () {
                    UserSystem.setCurrentUser(this.dataset.user);
                });
            });
        }
        overlay.style.display = 'flex';
    },

    dismissLogin() {
        var overlay = document.getElementById('login-overlay');
        if (overlay) overlay.style.display = 'none';
    },

    init() {
        this.updateNavbar();
        if (!this.getCurrentUser()) {
            this.showLogin();
        }
    }
};

document.addEventListener('DOMContentLoaded', function () {
    UserSystem.init();
});
