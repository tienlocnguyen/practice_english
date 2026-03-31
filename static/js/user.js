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
        const percentage = Math.floor((score / total) * 100);
        const passed = percentage >= 70;
        progress[user][key] = {
            score: score,
            total: total,
            passed: passed,
            percentage: percentage,
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
            while (el.firstChild) el.removeChild(el.firstChild);
            var span = document.createElement('span');
            span.className = 'user-name';
            span.textContent = '👤 ' + user;
            el.appendChild(span);
            el.style.display = 'flex';
            var switchBtn = document.getElementById('user-switch-btn');
            if (switchBtn) switchBtn.style.display = 'inline-block';
        } else {
            while (el.firstChild) el.removeChild(el.firstChild);
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
            overlay.setAttribute('role', 'dialog');
            overlay.setAttribute('aria-modal', 'true');
            overlay.setAttribute('aria-label', 'Chọn người dùng');

            var card = document.createElement('div');
            card.className = 'login-card';

            var icon = document.createElement('div');
            icon.className = 'login-icon';
            icon.textContent = '👤';
            card.appendChild(icon);

            var h2 = document.createElement('h2');
            h2.textContent = 'Chọn người dùng';
            card.appendChild(h2);

            var p = document.createElement('p');
            p.textContent = 'Chọn tên của bạn để bắt đầu học';
            card.appendChild(p);

            var btnsDiv = document.createElement('div');
            btnsDiv.className = 'login-buttons';

            for (var i = 0; i < this.DEFAULT_USERS.length; i++) {
                var btn = document.createElement('button');
                btn.className = 'btn btn-primary login-user-btn';
                btn.setAttribute('data-user', this.DEFAULT_USERS[i]);
                btn.textContent = this.DEFAULT_USERS[i];
                btn.addEventListener('click', function () {
                    UserSystem.setCurrentUser(this.dataset.user);
                });
                btnsDiv.appendChild(btn);
            }

            card.appendChild(btnsDiv);
            overlay.appendChild(card);
            document.body.appendChild(overlay);
        }
        overlay.style.display = 'flex';
        var firstBtn = overlay.querySelector('.login-user-btn');
        if (firstBtn) firstBtn.focus();
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
