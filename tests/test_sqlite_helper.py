import unittest
from db.sqlite import SqliteHelper

class TestSqliteHelper(unittest.TestCase):

    def setUp(self):
        self.helper = SqliteHelper()
    
    def tearDown(self):
        self.helper.close()


    def test_count_tables(self):
        sql = '''select count(*) as total_tables from sqlite_master where type="table";'''
        ok, rows = self.helper.query(sql)
        self.assertTrue(ok)
        self.assertEqual(len(rows), 1)
        self.assertTrue('total_tables' in rows[0].keys())
        self.assertTrue(isinstance(rows[0]['total_tables'], int))


    def test_create_table(self):
        sql = '''CREATE TABLE "dummy" (
            "id" INTEGER NOT NULL,
            "name" VARCHAR(50),
            PRIMARY KEY ("id")
        );'''
        before = self.__count_tables()
        ok, info = self.helper.exec(sql)
        self.assertTrue(ok)
        self.assertTrue('last_id' in info.keys())
        self.assertTrue('row_count' in info.keys())
        after = self.__count_tables()
        self.assertEqual(after, before + 1)
    

    def __count_tables(self):
        _, rows = self.helper.query('select count(*) as count from sqlite_master where type="table";')
        return rows[0]['count']
