from flask import Flask, render_template, request, jsonify, session
import sqlite3, os, random, json
from datetime import date, timedelta

app = Flask(__name__)
app.secret_key = 'langlearn-secret-2024'
DB = os.path.join(os.path.dirname(__file__), 'language.db')

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.executescript('''
        CREATE TABLE IF NOT EXISTS languages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            flag TEXT DEFAULT '🌐',
            code TEXT NOT NULL UNIQUE
        );
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lang_id INTEGER NOT NULL,
            category TEXT DEFAULT 'General',
            english TEXT NOT NULL,
            translation TEXT NOT NULL,
            pronunciation TEXT DEFAULT '',
            example_en TEXT DEFAULT '',
            example_tr TEXT DEFAULT '',
            difficulty INTEGER DEFAULT 1,
            FOREIGN KEY (lang_id) REFERENCES languages(id)
        );
        CREATE TABLE IF NOT EXISTS user_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word_id INTEGER NOT NULL UNIQUE,
            correct_count INTEGER DEFAULT 0,
            wrong_count INTEGER DEFAULT 0,
            last_seen TEXT,
            mastered INTEGER DEFAULT 0,
            FOREIGN KEY (word_id) REFERENCES words(id)
        );
        CREATE TABLE IF NOT EXISTS daily_streak (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            practice_date TEXT NOT NULL UNIQUE,
            words_practiced INTEGER DEFAULT 0,
            score_pct REAL DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS quiz_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lang_id INTEGER,
            category TEXT,
            total INTEGER DEFAULT 0,
            correct INTEGER DEFAULT 0,
            duration_secs INTEGER DEFAULT 0,
            played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        # Seed languages
        cur = conn.execute("SELECT COUNT(*) FROM languages")
        if cur.fetchone()[0] == 0:
            langs = [('Spanish','🇪🇸','es'),('French','🇫🇷','fr'),('Japanese','🇯🇵','ja'),('German','🇩🇪','de'),('Italian','🇮🇹','it')]
            conn.executemany("INSERT INTO languages (name,flag,code) VALUES (?,?,?)", langs)
            # Spanish words
            es_id = conn.execute("SELECT id FROM languages WHERE code='es'").fetchone()[0]
            es_words = [
                ('Greetings','Hello','Hola','OH-la','Hello!','¡Hola!',1),
                ('Greetings','Good morning','Buenos días','BWEH-nos DEE-as','Good morning!','¡Buenos días!',1),
                ('Greetings','Good night','Buenas noches','BWEH-nas NO-chess','Good night!','¡Buenas noches!',1),
                ('Greetings','Thank you','Gracias','GRA-see-as','Thank you very much.','Muchas gracias.',1),
                ('Greetings','Please','Por favor','por fa-VOR','Please help me.','Por favor ayúdame.',1),
                ('Food','Water','Agua','AH-gwa','I want water.','Quiero agua.',1),
                ('Food','Food','Comida','co-MEE-da','The food is good.','La comida es buena.',1),
                ('Food','Bread','Pan','pahn','I like bread.','Me gusta el pan.',1),
                ('Food','Coffee','Café','ca-FEH','One coffee please.','Un café por favor.',2),
                ('Numbers','One','Uno','OO-no','One person.','Una persona.',1),
                ('Numbers','Two','Dos','dos','Two cats.','Dos gatos.',1),
                ('Numbers','Three','Tres','tres','Three houses.','Tres casas.',1),
                ('Travel','Airport','Aeropuerto','ay-ro-PWER-to','Where is the airport?','¿Dónde está el aeropuerto?',2),
                ('Travel','Hotel','Hotel','oh-TEL','I need a hotel.','Necesito un hotel.',2),
                ('Colors','Red','Rojo','RO-ho','The car is red.','El coche es rojo.',1),
                ('Colors','Blue','Azul','ah-SOOL','I like blue.','Me gusta el azul.',1),
                ('Colors','Green','Verde','VER-deh','The tree is green.','El árbol es verde.',1),
            ]
            conn.executemany("INSERT INTO words (lang_id,category,english,translation,pronunciation,example_en,example_tr,difficulty) VALUES (?,?,?,?,?,?,?,?)",
                             [(es_id,)+w for w in es_words])
            # French words
            fr_id = conn.execute("SELECT id FROM languages WHERE code='fr'").fetchone()[0]
            fr_words = [
                ('Greetings','Hello','Bonjour','bon-ZHOOR','Hello sir!','Bonjour monsieur!',1),
                ('Greetings','Good evening','Bonsoir','bon-SWAHR','Good evening.','Bonsoir.',1),
                ('Greetings','Thank you','Merci','mer-SEE','Thank you!','Merci!',1),
                ('Greetings','Yes','Oui','wee','Yes, please.','Oui, s\'il vous plaît.',1),
                ('Greetings','No','Non','nohn','No, thank you.','Non, merci.',1),
                ('Food','Bread','Pain','pan','French bread.','Pain français.',1),
                ('Food','Wine','Vin','van','Red wine please.','Vin rouge s\'il vous plaît.',2),
                ('Food','Cheese','Fromage','fro-MAZH','I love cheese.','J\'adore le fromage.',1),
                ('Colors','Black','Noir','nwahr','Black cat.','Chat noir.',1),
                ('Colors','White','Blanc','blahn','White dress.','Robe blanche.',1),
                ('Numbers','One','Un','uh','One apple.','Une pomme.',1),
                ('Numbers','Two','Deux','duh','Two birds.','Deux oiseaux.',1),
                ('Travel','Train','Train','tran','The train is late.','Le train est en retard.',2),
                ('Travel','Beach','Plage','plazh','I love the beach.','J\'adore la plage.',1),
            ]
            conn.executemany("INSERT INTO words (lang_id,category,english,translation,pronunciation,example_en,example_tr,difficulty) VALUES (?,?,?,?,?,?,?,?)",
                             [(fr_id,)+w for w in fr_words])
            # Japanese words
            ja_id = conn.execute("SELECT id FROM languages WHERE code='ja'").fetchone()[0]
            ja_words = [
                ('Greetings','Hello','こんにちは (Konnichiwa)','kon-NEE-chee-wah','Hello!','こんにちは！',1),
                ('Greetings','Thank you','ありがとう (Arigatou)','ah-ree-GAH-toh','Thank you very much.','どうもありがとう。',1),
                ('Greetings','Good morning','おはよう (Ohayou)','oh-hah-YOH','Good morning!','おはようございます！',1),
                ('Food','Water','水 (Mizu)','mee-ZOO','Water please.','お水をください。',1),
                ('Food','Rice','ご飯 (Gohan)','go-HAN','Japanese rice.','日本のご飯。',1),
                ('Numbers','One','一 (Ichi)','ee-chee','One cat.','猫一匹。',1),
                ('Numbers','Two','二 (Ni)','nee','Two dogs.','犬二匹。',1),
                ('Colors','Red','赤 (Aka)','ah-kah','Red flower.','赤い花。',1),
                ('Colors','Blue','青 (Ao)','ah-oh','Blue sky.','青い空。',1),
            ]
            conn.executemany("INSERT INTO words (lang_id,category,english,translation,pronunciation,example_en,example_tr,difficulty) VALUES (?,?,?,?,?,?,?,?)",
                             [(ja_id,)+w for w in ja_words])
        conn.commit()

# ── Routes ────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/languages')
def languages():
    with get_db() as conn:
        rows = conn.execute("SELECT l.*, COUNT(w.id) as word_count FROM languages l LEFT JOIN words w ON w.lang_id=l.id GROUP BY l.id").fetchall()
        return jsonify([dict(r) for r in rows])

@app.route('/api/languages/<int:lang_id>/categories')
def categories(lang_id):
    with get_db() as conn:
        rows = conn.execute("SELECT category, COUNT(*) as cnt FROM words WHERE lang_id=? GROUP BY category", (lang_id,)).fetchall()
        return jsonify([dict(r) for r in rows])

@app.route('/api/words/<int:lang_id>')
def words(lang_id):
    cat = request.args.get('category')
    with get_db() as conn:
        if cat and cat != 'All':
            rows = conn.execute("SELECT w.*, COALESCE(p.correct_count,0) as correct_count, COALESCE(p.wrong_count,0) as wrong_count, COALESCE(p.mastered,0) as mastered FROM words w LEFT JOIN user_progress p ON p.word_id=w.id WHERE w.lang_id=? AND w.category=? ORDER BY w.id", (lang_id,cat)).fetchall()
        else:
            rows = conn.execute("SELECT w.*, COALESCE(p.correct_count,0) as correct_count, COALESCE(p.wrong_count,0) as wrong_count, COALESCE(p.mastered,0) as mastered FROM words w LEFT JOIN user_progress p ON p.word_id=w.id WHERE w.lang_id=? ORDER BY w.id", (lang_id,)).fetchall()
        return jsonify([dict(r) for r in rows])

@app.route('/api/quiz/<int:lang_id>')
def quiz(lang_id):
    cat = request.args.get('category', 'All')
    n = int(request.args.get('n', 10))
    with get_db() as conn:
        if cat != 'All':
            rows = conn.execute("SELECT * FROM words WHERE lang_id=? AND category=?", (lang_id, cat)).fetchall()
        else:
            rows = conn.execute("SELECT * FROM words WHERE lang_id=?", (lang_id,)).fetchall()
        if len(rows) < 4:
            return jsonify({'error': 'Not enough words. Need at least 4.'}), 400
        selected = random.sample(rows, min(n, len(rows)))
        quiz_qs = []
        for word in selected:
            # Build wrong options from same language
            others = [r for r in rows if r['id'] != word['id']]
            wrong = random.sample(others, min(3, len(others)))
            options = [word['translation']] + [w['translation'] for w in wrong]
            random.shuffle(options)
            quiz_qs.append({
                'id': word['id'],
                'english': word['english'],
                'correct': word['translation'],
                'options': options,
                'pronunciation': word['pronunciation'],
                'example_en': word['example_en'],
                'example_tr': word['example_tr'],
                'category': word['category']
            })
        return jsonify(quiz_qs)

@app.route('/api/progress', methods=['POST'])
def update_progress():
    data = request.json
    word_id = data['word_id']
    correct = data['correct']
    with get_db() as conn:
        conn.execute('''INSERT INTO user_progress (word_id, correct_count, wrong_count, last_seen)
            VALUES (?,?,?,date('now'))
            ON CONFLICT(word_id) DO UPDATE SET
              correct_count = correct_count + ?,
              wrong_count = wrong_count + ?,
              last_seen = date('now'),
              mastered = CASE WHEN correct_count + ? >= 5 THEN 1 ELSE 0 END''',
            (word_id, 1 if correct else 0, 0 if correct else 1,
             1 if correct else 0, 0 if correct else 1, 1 if correct else 0))
        conn.commit()
    return jsonify({'success': True})

@app.route('/api/quiz/complete', methods=['POST'])
def quiz_complete():
    data = request.json
    today = str(date.today())
    with get_db() as conn:
        conn.execute("INSERT INTO quiz_sessions (lang_id,category,total,correct,duration_secs) VALUES (?,?,?,?,?)",
                     (data['lang_id'], data.get('category','All'), data['total'], data['correct'], data.get('duration_secs',0)))
        pct = round(data['correct']/data['total']*100) if data['total'] else 0
        conn.execute('''INSERT INTO daily_streak (practice_date,words_practiced,score_pct)
            VALUES (?,?,?) ON CONFLICT(practice_date) DO UPDATE SET
            words_practiced=words_practiced+?,score_pct=(score_pct+?)/2''',
            (today, data['total'], pct, data['total'], pct))
        conn.commit()
    return jsonify({'success': True})

@app.route('/api/stats')
def stats():
    with get_db() as conn:
        total_words = conn.execute("SELECT COUNT(*) FROM words").fetchone()[0]
        mastered = conn.execute("SELECT COUNT(*) FROM user_progress WHERE mastered=1").fetchone()[0]
        practiced = conn.execute("SELECT COUNT(*) FROM user_progress WHERE correct_count+wrong_count>0").fetchone()[0]
        sessions = conn.execute("SELECT COUNT(*), COALESCE(AVG(correct*100.0/total),0) FROM quiz_sessions WHERE total>0").fetchone()
        streak = get_study_streak()
        recent = conn.execute("SELECT * FROM quiz_sessions ORDER BY played_at DESC LIMIT 5").fetchall()
        return jsonify({
            'total_words': total_words, 'mastered': mastered, 'practiced': practiced,
            'total_sessions': sessions[0], 'avg_score': round(sessions[1], 1),
            'streak': streak,
            'recent_sessions': [dict(r) for r in recent]
        })

def get_study_streak():
    with get_db() as conn:
        rows = conn.execute("SELECT practice_date FROM daily_streak ORDER BY practice_date DESC").fetchall()
        if not rows: return 0
        streak = 0
        today = date.today()
        for i, r in enumerate(rows):
            if date.fromisoformat(r['practice_date']) == today - timedelta(days=i):
                streak += 1
            else: break
        return streak

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5004)
