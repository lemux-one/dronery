from threading import Timer
from api.utils import log
from db.sqlite import SqliteHelper
import bottle

LOW_LEVEL = 25

def run():
    if not bottle.DEBUG:
        dbhelper = SqliteHelper()
        ok, drones = dbhelper.query('select * from drones;')
        if not ok:
            log('Audit failed: Database query failed. See above logs for details.', 'ERROR')
        else:
            low_batt = 0
            for drone in drones:
                if drone['battery_capacity'] < LOW_LEVEL:
                    low_batt += 1
            log(f'Audit report: Low battery for {low_batt}/{len(drones)} drones', 'AUDIT')
        dbhelper.close()
        Timer(5, run).start()
    else:
        log('Audit logs are disabled when DEBUG mode is ON')


if __name__ == "__main__":
    run()