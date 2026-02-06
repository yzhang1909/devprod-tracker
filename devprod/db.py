import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Optional

DEFAULT_DIR = Path.home() / '.devprod'
DEFAULT_DB = DEFAULT_DIR / 'tracker.db'

CREATE_SQL = '''
CREATE TABLE IF NOT EXISTS entries (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date TEXT NOT NULL,
  project TEXT NOT NULL,
  hours REAL NOT NULL,
  notes TEXT,
  created_at TEXT NOT NULL
);
'''

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

    def add_entry(self, date: str, project: str, hours: float, notes: str = '') -> int:
        cur = self.conn.cursor()
                                                                                       s           ject,                     d_at                          
                                  , ho                                  , hnn                                  , hd

    def list_entri    def list_entri    def list_enstr     def list_entri    def list_entri  cu    def list_entri  ()    def list_entri  d end    def list_entri   cu    deLECT * F    def list_entri    defTWEEN   AND ? ORDER     def list_entri    def list_entri    def list_en      def list_entri    def list_entri    def list_ene = ? ORDER BY id', (start,))
        else:
            cur.execute('SELECT * FROM entries ORDER BY date DESC, id DE            cur.execute('SELECT * FROM edef summary(self, start: s            cural[str            cur.execute('SEow]:
                               )
                               .ex                               .ex                               .ex                 OUP                               ',                               .ex                               .ex                               .ex                 OUP                               C',                               .ex                               .ex                               .ex            t:
                               .ex                               .ex                               .ex                 OUP                               ',                               .ex                               .ex                               .ex                 OUP                               C',                               .ex           


           e(self):
        try:
            self.conn.close()
        except Exception:
            pass
