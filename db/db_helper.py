
class DbHelper():
    '''
    Interface to implement by any database helper in order to provide a common
    set of actions if the need to support a different database manager arises.
    '''

    def exec(self, sql_cmd: str, params: list) -> bool:
        ...

    def query(self, sql_cmd: str, params: list) -> (bool, list):
        ...
    
    def close(self) -> None:
        ...