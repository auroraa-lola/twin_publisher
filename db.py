import sqlite3

DB_PATH = "qa.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS qa (
                id INTEGER PRIMARY KEY,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                category TEXT,
                reviewed INTEGER NOT NULL DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Migrate a database created before the reviewed column existed
        cols = [r["name"] for r in conn.execute("PRAGMA table_info(qa)")]
        if "reviewed" not in cols:
            conn.execute("ALTER TABLE qa ADD COLUMN reviewed INTEGER NOT NULL DEFAULT 0")


def add_qa(question, answer, category=None):
    # LLM-written rows always start unreviewed
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO qa (question, answer, category, reviewed) VALUES (?, ?, ?, 0)",
            (question, answer, category),
        )


def search_qa(text, limit=5):
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, question, answer, reviewed FROM qa "
            "WHERE question LIKE ? OR answer LIKE ? "
            "ORDER BY reviewed DESC, id DESC LIMIT ?",
            (f"%{text}%", f"%{text}%", limit),
        ).fetchall()
    return [dict(r) for r in rows]


# ---------- Human review ----------
def list_unreviewed():
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, question, answer FROM qa WHERE reviewed = 0 ORDER BY id"
        ).fetchall()
    return [dict(r) for r in rows]


def approve_qa(qa_id):
    with get_conn() as conn:
        conn.execute("UPDATE qa SET reviewed = 1 WHERE id = ?", (qa_id,))


def delete_qa(qa_id):
    with get_conn() as conn:
        conn.execute("DELETE FROM qa WHERE id = ?", (qa_id,))