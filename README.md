# English Practice - Luyện Tiếng Anh 🎓

Tool sinh web tĩnh để luyện từ vựng tiếng Anh qua mini game, deploy lên GitHub Pages.

## 🎮 Mini Games

| # | Game | Mô tả |
|---|------|--------|
| 1 | 🖼️ Chọn từ với hình ảnh | Xem hình, chọn từ đúng |
| 2 | 🔍 Chọn hình ảnh ứng với từ | Xem từ, chọn hình đúng |
| 3 | ✏️ Điền chữ cái | Điền chữ cái còn thiếu |
| 4 | 📝 Ô chữ | Giải ô chữ theo chủ đề |
| 5 | 💡 Đoán từ | Đoán từ từ các gợi ý |
| 6 | 🃏 Lật thẻ ghi nhớ | Ghép cặp từ-hình |
| 7 | 🔀 Xáo trộn chữ cái | Sắp xếp lại chữ cái |

## 📁 Cấu trúc project

```
english_practice/
├── config.json           # Cấu hình site & danh sách game
├── build.py              # Script sinh web tĩnh
├── data/
│   ├── level1.json       # Dữ liệu từ vựng lớp 1
│   ├── level3.json       # Dữ liệu từ vựng lớp 3
│   └── crosswords.json   # Dữ liệu ô chữ
├── static/
│   ├── css/
│   │   ├── style.css     # CSS chung
│   │   ├── games.css     # CSS cho game
│   │   └── crossword.css # CSS cho ô chữ
│   └── js/
│       ├── utils.js      # Hàm tiện ích
│       ├── game-engine.js # Engine quản lý game chung
│       ├── crossword.js  # Engine ô chữ
│       └── games/
│           ├── word-image.js
│           ├── image-word.js
│           ├── fill-letter.js
│           ├── word-guess.js
│           ├── memory-cards.js
│           └── word-scramble.js
├── docs/                 # Output (web tĩnh đã sinh)
└── .github/workflows/
    └── deploy.yml        # GitHub Actions auto deploy
```

## 🚀 Sử dụng

### Build local

```bash
python build.py
```

Web tĩnh sẽ được sinh ra trong thư mục `docs/`. Mở `docs/index.html` để xem.

### Deploy lên GitHub

1. Tạo repo trên GitHub
2. Push code lên nhánh `main`
3. Vào **Settings > Pages > Source**: chọn **GitHub Actions**
4. Web sẽ tự động được build & deploy khi push code

### Thêm từ vựng mới

Chỉnh sửa file JSON trong thư mục `data/`:

```json
{
  "word": "elephant",
  "meaning": "con voi",
  "phonetic": "/ˈelɪfənt/",
  "image": "https://example.com/elephant.png",
  "audio": "",
  "example": "The elephant is big.",
  "hint": "Largest land animal"
}
```

### Thêm level mới

1. Tạo file `data/levelX.json` theo format giống `level1.json`
2. Thêm đường dẫn vào `config.json` > `"levels"`
3. Chạy `python build.py`

### Thêm ô chữ mới

Thêm vào `data/crosswords.json`:

```json
{
  "level": 1,
  "topic": "colors",
  "title": "Color Crossword",
  "title_vi": "Ô chữ Màu sắc",
  "size": 8,
  "words": [
    {"word": "red", "clue": "Color of apple", "clue_vi": "Màu của táo", "row": 0, "col": 0, "direction": "across"}
  ]
}
```

## 🔧 Mở rộng

Để thêm mini game mới:

1. Tạo file JS trong `static/js/games/ten-game.js`
2. Implement hàm `initGameRound()` (được gọi mỗi câu hỏi)
3. Thêm game vào `config.json` > `"games"`
4. Chạy `python build.py`

## 📱 Responsive

Web hoạt động tốt trên cả desktop và mobile.
