from db.db_helper import DbHelper
from api.utils import log

class MigrationsException(Exception):
    def __str__(self) -> str:
        return "Unable to run migrations. See previous logs for details."

def run_migrations(dbhelper: DbHelper) -> None:
    '''
    Runs every statement found in "migrations.sql" one by one.
    This function is meant to be called before anything else in
    order to provide initial database structure and data.
    '''
    log('Running migrations using DbHelper: ' + str(dbhelper.__class__))
    script = ""
    statements = []
    with open('migrations.sql', mode='r', encoding='utf-8') as file:
        for line in file:
            if line.endswith(';\n') or line.endswith(';'):
                if line.endswith('\n'):
                    line = line[:-1]
                statements.append(script + line)
                script = ""
            elif line != '\n':
                script += line
    ok = True
    for statement in statements:
        ok = ok and dbhelper.exec(statement)
    if ok:
        log('Migrations applied!')
    else:
        raise(MigrationsException())