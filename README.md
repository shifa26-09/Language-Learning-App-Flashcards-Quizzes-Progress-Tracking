# 🌍 LinguaLeap — Language Learning App

A beautifully designed, fully interactive language learning app that works **instantly in any browser** — no installation, no server required. All progress is saved automatically using localStorage.

---

## 🚀 How to Run

### Option 1: Standalone (Recommended — Zero Setup)
1. Open `Task4_LanguageLearning_Standalone.html` in any modern browser (Chrome, Firefox, Edge, Safari)
2. That's it — fully functional immediately!

### Option 2: Flask Backend
```bash
cd flask_backend
pip install flask
python app.py
```
Open: **http://localhost:5004**

---

## ✨ Features

### 🌍 Language Selection
- Choose from **5 languages**: Spanish 🇪🇸, French 🇫🇷, Japanese 🇯🇵, German 🇩🇪, Italian 🇮🇹
- Per-language progress bars showing words mastered
- Overall stats dashboard on the home screen

### 📚 Flashcard Mode
- Flip cards with smooth 3D animation (English → Translation)
- Shows pronunciation guide and example sentences
- Filter by **language** and **category** (Greetings, Food, Numbers, Colors, Travel)
- Mark words as **"Still Learning"** or **"Got It!"**
- 5 correct marks = Word **Mastered** 🏆 (+10 XP)
- Mastered word counter updates in real time

### 🧠 Quiz Mode
- Multiple-choice quiz with 4 answer options
- Choose question count: 5, 10, 15, or 20 questions
- Filter by language and category
- Instant correct/wrong feedback with color highlighting
- XP rewards: +5 XP per correct answer
- Final score screen with performance message
- Session history saved automatically

### 📖 Vocabulary Browser
- Full word list for any language + category
- **Live search** — filter as you type
- Shows: English word, translation, pronunciation, example sentence
- Mastered badge shown on completed words

### 📊 Progress Tracker
- Total words mastered across all languages
- XP earned & current level (100 XP per level)
- Animated XP progress bar
- Average quiz score
- **8 Achievements** to unlock:
  - 🌱 First Word, 📚 Bookworm, 🧠 Polyglot Apprentice
  - 🎯 Quiz Taker, 🏅 Quiz Master, ⭐ High Achiever
  - 💫 Century XP, 💎 XP Legend
- Recent quiz sessions log (last 5 sessions)

---

## 📦 What's Included

```
Task4_LanguageLearning/
├── Task4_LanguageLearning_Standalone.html   ← Open this in browser (zero setup)
└── flask_backend/
    ├── app.py                               ← Flask backend server
    ├── requirements.txt                     ← pip install flask
    └── README.md                            ← This file
```

---

## 🗂️ Vocabulary Categories

| Category   | Languages Covered              |
|------------|-------------------------------|
| Greetings  | ES, FR, JA, DE, IT            |
| Food       | ES, FR, JA, DE, IT            |
| Numbers    | ES, FR, JA, DE, IT            |
| Colors     | ES, FR, JA, DE, IT            |
| Travel     | ES, FR, IT, DE                |

**Total words pre-loaded:** ~75 words across 5 languages

---

## 🎮 XP & Leveling System

| Action              | XP Earned |
|---------------------|-----------|
| Flashcard correct   | +2 XP     |
| Word mastered (5×)  | +10 XP    |
| Quiz correct answer | +5 XP     |
| Quiz score ≥ 80%    | +25 XP    |
| Perfect quiz score  | +50 XP    |

**Level up every 100 XP** — track your progress on the Progress page.

---

## 🛠️ Tech Stack

| Layer     | Technology                        |
|-----------|----------------------------------|
| Frontend  | Vanilla HTML5, CSS3, JavaScript  |
| Storage   | localStorage (no DB needed)      |
| Backend   | Python + Flask + SQLite (optional)|
| Fonts     | Google Fonts (Inter)             |
| Icons     | Emoji (no icon library needed)   |

---

## 📸 Pages Overview

| Page        | Description                                      |
|-------------|--------------------------------------------------|
| 🌍 Languages | Pick a language, see per-language progress        |
| 📚 Flashcards| Flip-card study mode with pronunciation + examples|
| 🧠 Quiz      | Multiple-choice quiz with scoring & XP           |
| 📖 Vocabulary| Browse & search all words with mastery status    |
| 📊 Progress  | XP, levels, achievements, quiz history           |

---

## 💡 Tips for Best Experience

- Start with **Flashcards** to learn words, then test yourself with **Quiz**
- Use the **category filter** to focus on one topic at a time (e.g. just "Food")
- Check **Progress** page to see which achievements you've unlocked
- All data persists — close the tab and come back anytime!

---

## 📬 Contact / Credits

Built for the **CodeAlpha App Development Internship**
- Task 4: Language Learning App
- Framework: Flask (backend) + Vanilla JS (frontend)
- Data: Persistent via localStorage / SQLite

> *"The limits of my language mean the limits of my world."* — Ludwig Wittgenstein
