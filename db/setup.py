from db.db_helper import DbHelper

class MigrationsException(Exception):
    def __str__(self) -> str:
        return "ERR - An error ocurred while running migrations. See log for details."

def run_migrations(dbhelper: DbHelper) -> None:
    '''
    Runs every statement found in "migrations.sql" one by one.
    This function is meant to be called before anything else in
    order to provide initial database structure and data.
    '''
    print('INF - Running migrations using DbHelper: ' + str(dbhelper))
    script = ""
    statements = []
    with open('migrations.sql', mode='r', encoding='utf-8') as file:
        for line in file:
            if line.endswith(';\n'):
                statements.append(script + line)
                script = ""
            else:
                script += line
    ok = True
    for statement in statements:
        ok = ok and dbhelper.exec(statement)
    if ok:
        print('INF - Migrations applied!')
    else:
        raise(MigrationsException())