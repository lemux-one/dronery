import sqlite3
from db.db_helper import DbHelper

class SqliteHelper(DbHelper):

    def __init__(self):
        '''
        Creates an in-memory database
        '''
        self.conn = sqlite3.connect(':memory:')
    

    def query(self, select_query):
        '''
        This method is meant for simple SELECT queries.
        It does not commit and does not rollback on errors.
        '''
        rows = []
        ok = True
        try:
            self.cur = self.conn.cursor()
            self.cur.execute(select_query)
            rows = self.__zip_records()
        except Exception as ex:
            ok = False
            print('ERR - ' + ex)
        return ok, rows


    def exec(self, sql_cmd):
        '''
        This method is meant for data modification queries.
        It commits if no error ocurred or rolls back if something happened.
        '''
        ok = True
        try:
            self.cur = self.conn.cursor()
            self.cur.execute(sql_cmd)
            self.conn.commit()
        except Exception as ex:
            ok = False
            self.conn.rollback()
            print('ERR - ' + ex)
        return ok


    def close(self) -> None:
        '''
        Closes the database.
        '''
        self.cur.close()
        self.conn.close()
    

    def __zip_records(self) -> list:
        '''
        Utility to map every record item to its corresponding description header.
        '''
        rows = []
        headers = [x[0] for x in self.cur.description]
        records = self.cur.fetchall()
        for record in records:
            rows.append(dict(zip(headers, record)))
        return rows


helper = SqliteHelper()