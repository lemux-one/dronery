import sqlite3
from db.db_helper import DbHelper

class SqliteHelper(DbHelper):

    def __init__(self):
        '''
        Creates an in-memory database
        '''
        self.conn = sqlite3.connect(':memory:')
    

    def query(self, select_query: str, params: list = []) -> (bool, list):
        '''
        This method is meant for simple SELECT queries.
        It does not commit and does not rollback on errors.
        '''
        rows = []
        ok = True
        try:
            self.cur = self.conn.cursor()
            self.cur.execute(select_query, params)
            rows = self.__zip_records()
        except Exception as ex:
            ok = False
            print('ERR - ' + str(ex))
        return ok, rows


    def exec(self, sql_cmd: str, params: list = []) -> bool:
        '''
        This method is meant for data modification queries.
        It commits if no error ocurred or rolls back if something happened.
        '''
        ok = True
        try:
            self.cur = self.conn.cursor()
            self.cur.execute(sql_cmd, params)
            self.conn.commit()
        except Exception as ex:
            ok = False
            self.conn.rollback()
            print('ERR - ' + str(ex))
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