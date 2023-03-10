from db.db_helper import DbHelper

def run_migrations(dbhelper: DbHelper) -> None:
    print('INF - Running migrations using DbHelper: ' + str(dbhelper))