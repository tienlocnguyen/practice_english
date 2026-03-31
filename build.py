#!/usr/bin/env python3
"""
English Practice - Static Site Generator
Reads JSON data and generates a static website for English vocabulary practice.
"""

import json
import os
import shutil
import sys
from pathlib import Path


def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def escape_html_attr(text):
    """Escape a string for safe use in an HTML attribute."""
    return str(text).replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')


def render_template(template_str, context):
    """Simple template rendering with {{variable}} syntax."""
    result = template_str
    for key, value in context.items():
        result = result.replace('{{' + key + '}}', str(value))
    return result


def generate_head(title, base_url=".", extra_css=""):
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Luyện Tiếng Anh</title>
    <link rel="stylesheet" href="{base_url}/css/style.css">
    <link rel="stylesheet" href="{base_url}/css/user-exam.css">
    {extra_css}
</head>"""


def generate_nav(base_url="."):
    return f"""
<nav class="navbar">
    <a href="{base_url}/index.html" class="nav-logo">🎓 Luyện Tiếng Anh</a>
    <div class="nav-links">
        <a href="{base_url}/index.html">🏠 Trang chủ</a>
        <div id="user-display" class="user-display"></div>
        <button id="user-switch-btn" class="btn-user-switch" style="display:none" onclick="UserSystem.logout()">🔄 Đổi</button>
    </div>
</nav>"""


def generate_footer(base_url="."):
    return f"""
<footer class="footer">
    <p>🎓 Luyện Tiếng Anh - Học từ vựng qua mini game</p>
</footer>
<script src="{base_url}/js/user.js"></script>
"""


def generate_index_page(config, levels, output_dir):
    """Generate the main index page."""
    games = config['games']
    level_cards = ""
    for level_data in levels:
        lvl = level_data['level']
        label = level_data['label']
        desc = level_data['description']
        topic_count = len(level_data['topics'])
        word_count = sum(len(t['words']) for t in level_data['topics'])
        level_cards += f"""
        <div class="level-card" onclick="window.location.href='level{lvl}/index.html'">
            <div class="level-badge">Level {lvl}</div>
            <h3>{label}</h3>
            <p>{desc}</p>
            <div class="level-stats">
                <span>📚 {topic_count} chủ đề</span>
                <span>📝 {word_count} từ vựng</span>
            </div>
            <button class="btn btn-primary">Bắt đầu học →</button>
        </div>"""

    game_cards = ""
    for g in games:
        game_cards += f"""
        <div class="game-info-card">
            <div class="game-icon">{g['icon']}</div>
            <h4>{g['name_vi']}</h4>
            <p>{g['description_vi']}</p>
        </div>"""

    html = f"""{generate_head("Trang chủ", ".")}
<body>
{generate_nav(".")}
<main class="container">
    <section class="hero">
        <h1>🎓 Luyện Tiếng Anh</h1>
        <p class="hero-sub">Học từ vựng tiếng Anh qua các mini game vui nhộn!</p>
    </section>

    <section class="section">
        <h2 class="section-title">📖 Chọn cấp độ</h2>
        <div class="level-grid">
            {level_cards}
        </div>
    </section>

    <section class="section">
        <h2 class="section-title">🎮 Các mini game</h2>
        <div class="game-info-grid">
            {game_cards}
        </div>
    </section>
</main>
{generate_footer(".")}
</body>
</html>"""

    with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)


def generate_level_page(config, level_data, crossword_data, output_dir):
    """Generate the level index page with topics and games."""
    lvl = level_data['level']
    label = level_data['label']
    base_url = ".."
    level_dir = os.path.join(output_dir, f"level{lvl}")
    ensure_dir(level_dir)

    games = config['games']

    topic_cards = ""
    for topic in level_data['topics']:
        word_count = len(topic['words'])
        topic_cards += f"""
        <div class="topic-card" data-topic="{topic['id']}" onclick="window.location.href='topic-{topic['id']}.html'">
            <div class="topic-icon">{topic['icon']}</div>
            <h3>{topic['name_vi']}</h3>
            <p class="topic-en">{topic['name']}</p>
            <span class="word-count">{word_count} từ</span>
        </div>"""

    game_buttons = ""
    for g in games:
        if g['id'] == 'crossword':
            # Check if there are crosswords for this level
            level_crosswords = [c for c in crossword_data.get('crosswords', []) if c['level'] == lvl]
            if not level_crosswords:
                continue
            game_buttons += f"""
        <a href="crossword.html" class="game-card">
            <span class="game-icon">{g['icon']}</span>
            <span class="game-name">{g['name_vi']}</span>
        </a>"""
        else:
            game_buttons += f"""
        <a href="game-{g['id']}.html" class="game-card">
            <span class="game-icon">{g['icon']}</span>
            <span class="game-name">{g['name_vi']}</span>
        </a>"""

    html = f"""{generate_head(label, base_url)}
<body>
{generate_nav(base_url)}
<main class="container">
    <section class="hero hero-small">
        <h1>📖 {label}</h1>
        <p class="hero-sub">{level_data['description']}</p>
    </section>

    <section class="section">
        <h2 class="section-title">📚 Chủ đề từ vựng</h2>
        <div class="topic-grid" id="topic-grid">
            {topic_cards}
        </div>
    </section>

    <section class="exam-section">
        <a href="exam.html" class="btn-exam">📝 Kiểm tra (Exam)</a>
    </section>

    <section class="section">
        <h2 class="section-title">🎮 Mini Games</h2>
        <div class="game-grid">
            {game_buttons}
        </div>
    </section>
</main>
{generate_footer(base_url)}
<script>
(function() {{
    var levelId = "{lvl}";
    function updateProgressBadges() {{
        var cards = document.querySelectorAll('.topic-card[data-topic]');
        cards.forEach(function(card) {{
            var existing = card.querySelector('.topic-progress-badge');
            if (existing) existing.remove();
            if (typeof UserSystem === 'undefined' || !UserSystem.getCurrentUser()) return;
            var topicId = card.dataset.topic;
            var result = UserSystem.getExamResult(levelId, topicId);
            if (result) {{
                var badge = document.createElement('div');
                badge.className = 'topic-progress-badge ' + (result.passed ? 'badge-pass' : 'badge-fail');
                badge.textContent = (result.passed ? '✅ PASS ' : '❌ NOT PASS ') + result.percentage + '%';
                card.appendChild(badge);
            }}
        }});
    }}
    document.addEventListener('DOMContentLoaded', function() {{
        setTimeout(function() {{
            updateProgressBadges();
            if (typeof UserSystem !== 'undefined') {{
                UserSystem.onChange(updateProgressBadges);
            }}
        }}, 50);
    }});
}})();
</script>
</body>
</html>"""

    with open(os.path.join(level_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)

    # Generate topic pages
    for topic in level_data['topics']:
        generate_topic_page(topic, level_data, level_dir, base_url)

    # Generate game pages
    for game in games:
        if game['id'] == 'crossword':
            level_crosswords = [c for c in crossword_data.get('crosswords', []) if c['level'] == lvl]
            if level_crosswords:
                generate_crossword_page(level_crosswords, level_data, level_dir, base_url)
        else:
            generate_game_page(game, level_data, level_dir, base_url)

    # Generate exam page
    generate_exam_page(level_data, level_dir, base_url)


def generate_topic_page(topic, level_data, level_dir, base_url):
    """Generate a topic vocabulary review page."""
    lvl = level_data['level']
    word_cards = ""
    for w in topic['words']:
        word_data = {**w, '_level': str(lvl), '_topic': topic['id']}
        word_json_attr = escape_html_attr(json.dumps(word_data, ensure_ascii=False))
        example_vi_html = ""
        if w.get('example_vi'):
            example_vi_html = f'<p class="example-vi">🇻🇳 {w["example_vi"]}</p>'
        word_cards += f"""
        <div class="vocab-card">
            <div class="vocab-emoji">{w['image']}</div>
            <div class="vocab-info">
                <h3>{w['word']}</h3>
                <p class="phonetic">{w['phonetic']}</p>
                <p class="meaning">{w['meaning']}</p>
                <p class="example">"{w['example']}"</p>
                {example_vi_html}
                <button class="btn btn-sm btn-speak" onclick="speak('{w['word']}')">🔊 Nghe</button>
                <button class="btn btn-sm feedback-report-btn" data-word="{word_json_attr}">⚠️ Báo lỗi</button>
            </div>
        </div>"""

    html = f"""{generate_head(f"{topic['name_vi']} - {level_data['label']}", base_url,
        f'<link rel="stylesheet" href="{base_url}/css/feedback.css">')}
<body>
{generate_nav(base_url)}
<main class="container">
    <div class="breadcrumb">
        <a href="index.html">{level_data['label']}</a> &gt; {topic['name_vi']}
    </div>

    <section class="hero hero-small">
        <h1>{topic['icon']} {topic['name_vi']} ({topic['name']})</h1>
    </section>

    <div class="feedback-toolbar">
        <button class="btn btn-sm btn-secondary" onclick="FeedbackSystem.exportFeedback()">
            📥 Xuất phản hồi <span id="feedback-export-count" class="feedback-export-count">0</span>
        </button>
        <button class="btn btn-sm btn-secondary" onclick="FeedbackSystem.clearFeedback()">🗑️ Xóa phản hồi</button>
    </div>

    <div class="vocab-grid">
        {word_cards}
    </div>

    <div class="back-link">
        <a href="index.html" class="btn btn-secondary">← Quay lại</a>
    </div>
</main>
{generate_footer(base_url)}
<script>
function speak(text) {{
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-US';
    utterance.rate = 0.8;
    speechSynthesis.speak(utterance);
}}
</script>
<script src="{base_url}/js/feedback.js"></script>
</body>
</html>"""

    with open(os.path.join(level_dir, f"topic-{topic['id']}.html"), 'w', encoding='utf-8') as f:
        f.write(html)


def generate_game_page(game, level_data, level_dir, base_url):
    """Generate a game page for a specific level."""
    lvl = level_data['level']
    # Serialize all topics data for JS
    topics_json = json.dumps(level_data['topics'], ensure_ascii=False)

    html = f"""{generate_head(f"{game['name_vi']} - {level_data['label']}", base_url,
        f'<link rel="stylesheet" href="{base_url}/css/games.css">')}
<body>
{generate_nav(base_url)}
<main class="container">
    <div class="breadcrumb">
        <a href="index.html">{level_data['label']}</a> &gt; {game['name_vi']}
    </div>

    <section class="game-header">
        <h1>{game['icon']} {game['name_vi']}</h1>
        <p>{game['description_vi']}</p>
    </section>

    <div class="game-controls">
        <label for="topic-select">Chọn chủ đề:</label>
        <select id="topic-select" onchange="loadTopic()">
            <option value="all">📚 Tất cả</option>
        </select>
        <button class="btn btn-primary" id="start-btn" onclick="startGame()">▶️ Bắt đầu</button>
        <button class="btn btn-secondary" id="next-btn" onclick="nextQuestion()" style="display:none">Câu tiếp →</button>
    </div>

    <div class="score-bar" id="score-bar" style="display:none">
        <span id="score-text">Điểm: 0</span>
        <span id="progress-text">Câu: 0/0</span>
        <div class="progress-bar"><div class="progress-fill" id="progress-fill"></div></div>
    </div>

    <div id="game-area" class="game-area">
        <p class="game-placeholder">Chọn chủ đề và nhấn "Bắt đầu" để chơi!</p>
    </div>

    <div id="result-area" class="result-area" style="display:none">
        <div class="result-card">
            <h2 id="result-title">🎉 Hoàn thành!</h2>
            <p id="result-score"></p>
            <div class="result-stars" id="result-stars"></div>
            <button class="btn btn-primary" onclick="startGame()">🔄 Chơi lại</button>
            <a href="index.html" class="btn btn-secondary">← Quay lại</a>
        </div>
    </div>
</main>
{generate_footer(base_url)}
<script>
const GAME_ID = "{game['id']}";
const TOPICS_DATA = {topics_json};
</script>
<script src="{base_url}/js/utils.js"></script>
<script src="{base_url}/js/game-engine.js"></script>
<script src="{base_url}/js/games/{game['id']}.js"></script>
</body>
</html>"""

    with open(os.path.join(level_dir, f"game-{game['id']}.html"), 'w', encoding='utf-8') as f:
        f.write(html)


def generate_crossword_page(crosswords, level_data, level_dir, base_url):
    """Generate crossword puzzle page."""
    lvl = level_data['level']
    crosswords_json = json.dumps(crosswords, ensure_ascii=False)

    options_html = ""
    for i, cw in enumerate(crosswords):
        options_html += f'<option value="{i}">{cw["title_vi"]}</option>'

    html = f"""{generate_head(f"Ô chữ - {level_data['label']}", base_url,
        f'<link rel="stylesheet" href="{base_url}/css/games.css"><link rel="stylesheet" href="{base_url}/css/crossword.css">')}
<body>
{generate_nav(base_url)}
<main class="container">
    <div class="breadcrumb">
        <a href="index.html">{level_data['label']}</a> &gt; Ô chữ
    </div>

    <section class="game-header">
        <h1>📝 Ô chữ</h1>
        <p>Giải ô chữ theo chủ đề</p>
    </section>

    <div class="game-controls">
        <label for="crossword-select">Chọn ô chữ:</label>
        <select id="crossword-select">
            {options_html}
        </select>
        <button class="btn btn-primary" onclick="startCrossword()">▶️ Bắt đầu</button>
        <button class="btn btn-secondary" onclick="checkCrossword()">✅ Kiểm tra</button>
    </div>

    <div id="crossword-area" class="crossword-area">
        <div id="crossword-grid" class="crossword-grid"></div>
        <div id="crossword-clues" class="crossword-clues"></div>
    </div>

    <div id="crossword-result" class="result-area" style="display:none">
        <div class="result-card">
            <h2 id="cw-result-title"></h2>
            <p id="cw-result-text"></p>
            <button class="btn btn-primary" onclick="startCrossword()">🔄 Chơi lại</button>
        </div>
    </div>
</main>
{generate_footer(base_url)}
<script>
const CROSSWORDS_DATA = {crosswords_json};
</script>
<script src="{base_url}/js/utils.js"></script>
<script src="{base_url}/js/crossword.js"></script>
</body>
</html>"""

    with open(os.path.join(level_dir, 'crossword.html'), 'w', encoding='utf-8') as f:
        f.write(html)


def generate_exam_page(level_data, level_dir, base_url):
    """Generate an exam page for a level that tests all topics."""
    lvl = level_data['level']
    label = level_data['label']
    topics_json = json.dumps(level_data['topics'], ensure_ascii=False)
    topic_count = len(level_data['topics'])
    questions_per_topic = 3
    total_questions = topic_count * questions_per_topic

    html = f"""{generate_head(f"Kiểm tra - {label}", base_url,
        f'<link rel="stylesheet" href="{base_url}/css/games.css">')}
<body>
{generate_nav(base_url)}
<main class="container">
    <div class="breadcrumb">
        <a href="index.html">{label}</a> &gt; Kiểm tra
    </div>

    <div id="exam-intro" class="exam-intro">
        <div class="exam-intro-card">
            <h2>📝 Kiểm tra - {label}</h2>
            <p>Kiểm tra từ vựng tất cả chủ đề trong bài học</p>
            <ul class="exam-info-list">
                <li>📚 {topic_count} chủ đề</li>
                <li>❓ {total_questions} câu hỏi ({questions_per_topic} câu/chủ đề)</li>
                <li>✅ Đạt: ≥ 70% mỗi chủ đề</li>
            </ul>
            <button class="btn btn-primary" onclick="startExam()" style="font-size:1.1rem;padding:0.8rem 2rem">▶️ Bắt đầu kiểm tra</button>
        </div>
    </div>

    <div id="exam-area" style="display:none">
        <div class="exam-progress-bar">
            <span id="exam-progress-text">Câu 1/{total_questions}</span>
            <div class="progress-bar"><div class="progress-fill" id="exam-progress-fill"></div></div>
        </div>
        <div id="exam-question-area" class="game-area"></div>
    </div>

    <div id="exam-result" class="result-area" style="display:none"></div>
</main>
{generate_footer(base_url)}
<script>
const LEVEL_ID = "{lvl}";
const TOPICS_DATA = {topics_json};
</script>
<script src="{base_url}/js/utils.js"></script>
<script src="{base_url}/js/exam.js"></script>
</body>
</html>"""

    with open(os.path.join(level_dir, 'exam.html'), 'w', encoding='utf-8') as f:
        f.write(html)


def copy_static_assets(output_dir):
    """Copy CSS and JS files to output directory."""
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    for sub in ['css', 'js', 'js/games']:
        src = os.path.join(static_dir, sub)
        dst = os.path.join(output_dir, sub)
        if os.path.exists(src):
            ensure_dir(dst)
            for fname in os.listdir(src):
                src_file = os.path.join(src, fname)
                if os.path.isfile(src_file):
                    shutil.copy2(src_file, os.path.join(dst, fname))


def build_site(config_path="config.json"):
    """Main build function."""
    print("🔨 Building English Practice site...")

    config = load_json(config_path)
    output_dir = config.get('output_dir', 'docs')

    # Clean output
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    ensure_dir(output_dir)

    # Load data
    levels = []
    for level_file in config['levels']:
        levels.append(load_json(level_file))
        print(f"  📁 Loaded {level_file}")

    crossword_data = {}
    if config.get('crosswords'):
        crossword_data = load_json(config['crosswords'])
        print(f"  📁 Loaded crosswords")

    # Copy static assets
    copy_static_assets(output_dir)
    print("  📋 Copied static assets")

    # Generate pages
    generate_index_page(config, levels, output_dir)
    print("  📄 Generated index.html")

    for level_data in levels:
        generate_level_page(config, level_data, crossword_data, output_dir)
        lvl = level_data['level']
        topics = len(level_data['topics'])
        print(f"  📄 Generated level{lvl}/ ({topics} topics)")

    print(f"\n✅ Site built successfully in '{output_dir}/' directory!")
    print(f"   Open {output_dir}/index.html in a browser to preview.")


if __name__ == '__main__':
    config_path = sys.argv[1] if len(sys.argv) > 1 else 'config.json'
    build_site(config_path)
