# Contributing Guide - Luyện Tiếng Anh 🎓

Hướng dẫn đóng góp cho dự án English Practice: kiến trúc tổng quan và các tác vụ thường gặp.

---

## 📐 Kiến trúc dự án

### Tech Stack

| Thành phần | Công nghệ | Mô tả |
|------------|-----------|-------|
| Build tool | Python (`build.py`) | Sinh web tĩnh từ dữ liệu JSON |
| Frontend | HTML / CSS / Vanilla JS | Không dùng framework |
| Lưu trữ | `localStorage` | Dữ liệu người dùng & tiến trình (client-side) |
| Hosting | GitHub Pages | Deploy tự động qua GitHub Actions |
| CI/CD | `.github/workflows/deploy.yml` | Build & deploy khi push lên `main` |

### Luồng dữ liệu

```
config.json + data/*.json
        │
        ▼
    build.py (sinh HTML tĩnh)
        │
        ▼
    docs/ (output)
        │
        ▼
    GitHub Actions → GitHub Pages
        │
        ▼
    Trình duyệt (localStorage lưu tiến trình)
```

### Cấu trúc thư mục

```
practice_english/
├── config.json               # Cấu hình site, danh sách level & game
├── build.py                  # Script sinh web tĩnh
├── data/                     # Dữ liệu từ vựng
│   ├── level1.json           # Từ vựng lớp 1
│   ├── level3.json           # Từ vựng lớp 3
│   ├── level5.json           # Từ vựng nâng cao
│   ├── levelA.json           # CEFR A1-A2
│   ├── levelB.json           # CEFR B1-B2
│   ├── levelC.json           # CEFR C1-C2
│   ├── leveltoefl.json       # TOEFL
│   └── crosswords.json       # Dữ liệu ô chữ
├── static/
│   ├── css/                  # Stylesheets
│   │   ├── style.css         # CSS chung
│   │   ├── games.css         # CSS cho game
│   │   ├── user-exam.css     # CSS cho user & exam
│   │   ├── feedback.css      # CSS cho feedback
│   │   └── crossword.css     # CSS cho ô chữ
│   └── js/
│       ├── utils.js          # Hàm tiện ích (shuffle, speak, escapeHtml)
│       ├── game-engine.js    # Engine quản lý game chung
│       ├── user.js           # Hệ thống người dùng (localStorage)
│       ├── exam.js           # Engine bài kiểm tra
│       ├── progress.js       # Trang tiến trình & huy chương
│       ├── feedback.js       # Hệ thống phản hồi
│       ├── crossword.js      # Engine ô chữ
│       └── games/            # Các mini game
│           ├── word-image.js
│           ├── image-word.js
│           ├── fill-letter.js
│           ├── word-guess.js
│           ├── memory-cards.js
│           ├── word-scramble.js
│           ├── speed-challenge.js
│           └── sentence-builder.js
├── docs/                     # Output (được gitignore)
└── .github/workflows/
    └── deploy.yml            # GitHub Actions auto deploy
```

### Cách build.py hoạt động

`build.py` đọc `config.json` và các file `data/*.json`, rồi sinh ra toàn bộ trang HTML tĩnh trong thư mục `docs/`:

- **index.html** — Trang chủ với danh sách level & game
- **{level}/index.html** — Trang tổng quan level với các topic
- **{level}/topic-{id}.html** — Trang ôn từ vựng theo topic
- **{level}/game-{id}.html** — Trang mini game
- **{level}/exam.html** — Trang bài kiểm tra (3 câu/topic)
- **{level}/crossword.html** — Trang ô chữ
- **progress.html** — Trang tiến trình & thành tích

### Build & chạy local

```bash
python build.py
# Mở docs/index.html trong trình duyệt
```

---

## 👤 Thêm người dùng mới

Hệ thống người dùng hoạt động hoàn toàn ở phía client, không có backend. Danh sách người dùng mặc định được định nghĩa trong `static/js/user.js`.

### Các bước

1. **Mở file** `static/js/user.js`

2. **Tìm mảng `DEFAULT_USERS`** (dòng 8):

   ```javascript
   DEFAULT_USERS: ['Linh', 'Long', 'Test'],
   ```

3. **Thêm tên người dùng mới** vào mảng:

   ```javascript
   DEFAULT_USERS: ['Linh', 'Long', 'Test', 'TênMới'],
   ```

4. **Build lại site**:

   ```bash
   python build.py
   ```

### Lưu ý

- Tên người dùng được hiển thị trực tiếp trên giao diện chọn user.
- Mỗi người dùng có dữ liệu tiến trình riêng biệt trong `localStorage` (key: `ep_progress`).
- Không cần mật khẩu — người dùng chỉ cần chọn tên để đăng nhập.
- Tiến trình bài kiểm tra được lưu theo cấu trúc `{username: {levelId_topicId: result}}`.

---

## 📝 Thêm từ vựng mới

Từ vựng được lưu trong các file JSON ở thư mục `data/`. Mỗi file tương ứng với một level, chứa nhiều topic, mỗi topic chứa danh sách từ.

### Cấu trúc một từ

```json
{
  "word": "elephant",
  "meaning": "con voi",
  "phonetic": "/ˈelɪfənt/",
  "image": "🐘",
  "audio": "",
  "example": "The elephant is big.",
  "example_vi": "Con voi rất to.",
  "hint": "Largest land animal"
}
```

| Trường | Bắt buộc | Mô tả |
|--------|----------|-------|
| `word` | ✅ | Từ tiếng Anh |
| `meaning` | ✅ | Nghĩa tiếng Việt |
| `phonetic` | ✅ | Phiên âm IPA |
| `image` | ✅ | Emoji đại diện (ký tự Unicode) |
| `audio` | ❌ | URL file audio (để trống nếu dùng Web Speech API) |
| `example` | ✅ | Câu ví dụ tiếng Anh |
| `example_vi` | ❌ | Câu ví dụ tiếng Việt (dùng cho level CEFR & TOEFL) |
| `hint` | ✅ | Gợi ý cho game đoán từ |

### Các bước thêm từ vào topic có sẵn

1. **Mở file level** tương ứng, ví dụ `data/level1.json`

2. **Tìm topic** cần thêm từ (theo `id`):

   ```json
   {
     "id": "animals",
     "name": "Animals",
     "name_vi": "Động vật",
     "icon": "🐾",
     "words": [
       // ... từ hiện có
     ]
   }
   ```

3. **Thêm object từ mới** vào mảng `words`:

   ```json
   {
     "word": "elephant",
     "meaning": "con voi",
     "phonetic": "/ˈelɪfənt/",
     "image": "🐘",
     "audio": "",
     "example": "The elephant is big.",
     "hint": "Largest land animal"
   }
   ```

4. **Build lại site**:

   ```bash
   python build.py
   ```

### Thêm topic mới vào level có sẵn

Thêm object topic mới vào mảng `topics` trong file level:

```json
{
  "id": "weather",
  "name": "Weather",
  "name_vi": "Thời tiết",
  "icon": "🌤️",
  "words": [
    {
      "word": "sunny",
      "meaning": "nắng",
      "phonetic": "/ˈsʌni/",
      "image": "☀️",
      "audio": "",
      "example": "It is sunny today.",
      "hint": "Bright and warm"
    }
  ]
}
```

### Thêm level mới

1. **Tạo file** `data/levelX.json` theo cấu trúc:

   ```json
   {
     "level": "X",
     "label": "Tên Level",
     "description": "Mô tả level",
     "topics": []
   }
   ```

2. **Thêm đường dẫn** vào `config.json` > `"levels"`:

   ```json
   "levels": [
     "data/level1.json",
     "data/levelX.json"
   ]
   ```

3. **Build lại site**: `python build.py`

---

## 🎮 Thêm mini game mới

Hệ thống game sử dụng kiến trúc plugin: mỗi game là một file JS riêng, implement hàm `initGameRound()` được gọi bởi game engine chung (`game-engine.js`).

### Kiến trúc game engine

```
game-engine.js (quản lý chung)
    │
    ├── gameState (trạng thái: words, score, currentIndex)
    ├── startGame() → gọi initGameRound()
    ├── onCorrectAnswer() → tăng điểm
    ├── onWrongAnswer() → không tăng điểm
    ├── nextQuestion() → gọi initGameRound()
    └── showResult() → hiển thị kết quả
    │
    ▼
games/{game-id}.js (implement cụ thể)
    └── initGameRound() → render UI câu hỏi
```

### Các bước thêm game mới

#### Bước 1: Tạo file game JS

Tạo file `static/js/games/{game-id}.js` và implement hàm `initGameRound()`:

```javascript
/**
 * Game: Tên Game (Tên tiếng Việt)
 * Mô tả ngắn
 */

function initGameRound() {
    const area = document.getElementById('game-area');
    const currentWord = gameState.words[gameState.currentIndex];

    // Lấy tất cả từ để tạo đáp án sai
    const allWords = getAllWords(TOPICS_DATA);

    // --- Render giao diện câu hỏi ---
    // Sử dụng area.innerHTML để hiển thị nội dung

    // --- Xử lý đáp án ---
    // Gọi onCorrectAnswer() khi đúng
    // Gọi onWrongAnswer() khi sai
}

function checkAnswer(btn, selected, correct) {
    if (!gameState.isPlaying) return;

    // Vô hiệu hóa tất cả nút
    const buttons = document.querySelectorAll('.option-btn');
    buttons.forEach(b => b.classList.add('disabled'));

    if (selected === correct) {
        btn.classList.add('correct');
        onCorrectAnswer();
    } else {
        btn.classList.add('wrong');
        buttons.forEach(b => {
            if (b.textContent === correct) b.classList.add('correct');
        });
        onWrongAnswer();
    }
}
```

**Các biến và hàm có sẵn từ engine:**

| Biến/Hàm | Mô tả |
|-----------|-------|
| `gameState.words` | Mảng từ đã shuffle cho lượt chơi |
| `gameState.currentIndex` | Index câu hỏi hiện tại |
| `gameState.isPlaying` | Game đang chạy hay không |
| `gameState.total` | Tổng số câu (tối đa 10) |
| `TOPICS_DATA` | Dữ liệu tất cả topic của level (JSON) |
| `onCorrectAnswer()` | Gọi khi trả lời đúng (tăng điểm) |
| `onWrongAnswer()` | Gọi khi trả lời sai |
| `getAllWords(TOPICS_DATA)` | Lấy tất cả từ (từ `utils.js`) |
| `shuffle(array)` | Xáo trộn mảng (từ `utils.js`) |
| `speak(text)` | Đọc từ bằng Web Speech API (từ `utils.js`) |
| `escapeHtml(text)` | Escape HTML để tránh XSS (từ `utils.js`) |

#### Bước 2: Đăng ký game trong config.json

Thêm object game mới vào mảng `"games"` trong `config.json`:

```json
{
  "id": "ten-game",
  "name": "Game Name",
  "name_vi": "Tên Game Tiếng Việt",
  "icon": "🎯",
  "description": "English description",
  "description_vi": "Mô tả tiếng Việt"
}
```

> **Quan trọng:** Giá trị `id` phải trùng với tên file JS (không có `.js`). Ví dụ: `id: "ten-game"` → file `static/js/games/ten-game.js`.

#### Bước 3: Build và kiểm tra

```bash
python build.py
```

Mở `docs/{level}/game-{game-id}.html` để kiểm tra game mới.

### Ví dụ tham khảo

- **Game đơn giản:** `static/js/games/word-image.js` (~53 dòng) — xem hình, chọn từ đúng
- **Game trung bình:** `static/js/games/fill-letter.js` — điền chữ cái còn thiếu
- **Game phức tạp:** `static/js/games/memory-cards.js` — lật thẻ ghi nhớ

### Lưu ý quan trọng

- Luôn dùng `escapeHtml()` khi hiển thị dữ liệu từ JSON trong HTML để tránh lỗi XSS.
- Game tự động nhận tối đa 10 từ mỗi lượt chơi (do `game-engine.js` giới hạn).
- CSS cho game nằm trong `static/css/games.css` — sử dụng các class có sẵn (`.option-btn`, `.correct`, `.wrong`, `.disabled`, `.question-image`, `.options-grid`).
- Sau khi thêm xong, push lên nhánh `main` để GitHub Actions tự động build & deploy.

---

## 🚀 Deploy

Khi push code lên nhánh `main`, GitHub Actions sẽ tự động:

1. Checkout code
2. Chạy `python build.py`
3. Upload thư mục `docs/` lên GitHub Pages
4. Website được cập nhật trong vài phút

Không cần build thủ công hay upload file — mọi thứ đều tự động.
