import sqlite3
from db.db_helper import DbHelper
from api.utils import (
    log,
    truncate_str
)

class SqliteHelper(DbHelper):

    def __init__(self, in_memory: bool = False):
        '''
        Creates an in-memory database
        '''
        dbname = 'dronery.db' if not in_memory else ':memory:'
        self.conn = sqlite3.connect(dbname)
    

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
            log(f'Sucessful query: {truncate_str(select_query)}')
        except Exception as ex:
            ok = False
            log(str(ex), 'ERROR')
        return ok, rows


    def exec(self, sql_cmd: str, params: list = []) -> (bool, dict):
        '''
        This method is meant for data modification queries.
        It commits if no error ocurred or rolls back if something happened.
        '''
        ok = True
        cur_info = {}
        try:
            self.cur = self.conn.cursor()
            self.cur.execute(sql_cmd, params)
            self.conn.commit()
            cur_info['last_id'] = self.cur.lastrowid
            cur_info['row_count'] = self.cur.rowcount
            log(f'Successful exec: {truncate_str(sql_cmd)}')
        except Exception as ex:
            ok = False
            self.conn.rollback()
            log(str(ex), 'ERROR')
        return ok, cur_info


    def close(self) -> None:
        '''
        Closes the database.
        '''
        self.cur.close()
        self.conn.close()
    

    def exists_table(self, table_name:str) -> bool:
        sql = '''select count(*) as count from sqlite_master 
            where type = "table" and name = ?;'''
        ok, rows = self.query(sql, [table_name,])
        return ok and rows and rows[0]['count'] == 1
    

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


helper = None