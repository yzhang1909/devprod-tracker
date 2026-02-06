import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Optional

DEFAULT_DIR = Path.home() / ".devprod"
DEFAULT_DB = DEFAULT_DIR / "tracker.db"

CREATE_SQL = """
CREATE TABLE IF NOT EXISTS entries (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date TEXT NOT NULL,
  project TEXT NOT NULL,
  hours REAL NOT NULL,
  notes TEXT,
  created_at TEXT NOT NULL
);
"""

class DB:
    def __init__(self, path: Optional[Path] = None):
        self.path = Path(path) if path else DEFAULT_DB
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.path))
        self.conn.row_factory = sqlite3.Row
        self._init()

    def _init(self):
        cur = self.conn.cursor()
        cur.executescript(CREATE_SQL)
        self.conn.commit()

    def add_entry(self, date: str, project: str, hours: float, notes: str = "") -> int:
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO entries (date, project, hours, notes, created_at) VALUES (?, ?, ?, ?, ?)",
            (date, project, hours, notes, datetime.now().isoformat())
        )
        self.conn.commit()
        return cur.lastrowid

    def list_entries(self, start: Optional[str] = None, end: Optional[str] = None) -> List:
        cur = self.conn.cursor()
        if start and not end:
            cur.execute("SELECT * FROM entries WHERE date >= ? ORDER BY date DESC, id DESC", (start,))
        elif start and end:
            cur.execute("SELECT * FROM entries WHERE date BETWEEN ? AND ? ORDER BY date DESC, id DESC", (start, end))
        else:
            cur.execute("SELECT * FROM entries ORDER BY date DESC, id DESC")
        return cur.fetchall()

    def summary(self, start: Optional[str] = None, end: Optional[str] = None) -> List:
        cur = self.conn.cursor()
        if start and not end:
            cur.execute("SELECT project, SUM(hours) as total FROM entries WHERE date >= ? GROUP BY project ORDER BY total DESC", (start,))
        elif start and end:
            cur.execute("SELECT project, SUM(hours) as total FROM entries WHERE date BETWEEN ? AND ? GROUP BY project ORDER BY total DESC", (start, end))
        else:
            cur.execute("SELECT project, SUM(hours) as total FROM entries GROUP BY project ORDER BY total DESC")
        return cur.fetchall()

    def total_hours(self, start: Optional[str] = None, end: Optional[str] = None) -> float:
        cur = self.conn.cursor()
        if start and not end:
            cur.execute("SELECT SUM(hours) FROM entries WHERE date >= ?", (start,))
        elif start and end:
            cur.execute("SELECT SUM(hours) FROM entries WHERE date BETWEEN ? AND ?", (start, end))
        else:
            cur.execute("SELECT SUM(hours) FROM entries")
        result = cur.fetchone()
        return result[0] or 0.0

    def close(self):
        try:
            self.conn.close()
        except Exception:
            pass
