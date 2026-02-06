import unittest
import tempfile
from pathlib import Path
from devprod.db import DB

class TestDB(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tmpdir.name) / 'test.db'
        self.db = DB(str(self.db_path))

    def tearDown(self):
        self.db.close()
        self.tmpdir.cleanup()

    def test_add_and_list(self):
        rid = self.db.add_entry('2024-01-01', 'project-a', 2.5, 'test note')
        self.assertIsNotNone(rid)
        rows = self.db.list_entries()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['project'], 'project-a')
        self.assertEqual(rows[0]['hours'], 2.5)
        self.assertEqual(rows[0]['notes'], 'test note')

if __name__ == '__main__':
    unittest.main()
