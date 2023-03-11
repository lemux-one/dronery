from db.db_helper import DbHelper

def run_migrations(dbhelper: DbHelper) -> None:
    print('INF - Running migrations using DbHelper: ' + str(dbhelper))
    script = ""
    statements = []
    with open('migrations.sql', 'r') as file:
        while line := file.readline():
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
        print('ERR - Failed to apply migrations. See log for details.')