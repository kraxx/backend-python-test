"""AlayaNotes

Usage:
  main.py [run]
  main.py initdb
  main.py migratedb
"""
from docopt import docopt
import subprocess
import os

from alayatodo import app


def _run_sql(filename):
    try:
        subprocess.check_output(
            "sqlite3 %s < %s" % (app.config['DATABASE'], filename),
            stderr=subprocess.STDOUT,
            shell=True
        )
    except subprocess.CalledProcessError as ex:
        print(ex.output)
        os.exit(1)


if __name__ == '__main__':
    args = docopt(__doc__)
    if args.get('initdb'):
        _run_sql('resources/database.sql')
        _run_sql('resources/fixtures.sql')
        print("AlayaTodo: Database initialized.")
    elif args.get('migratedb'):
        _run_sql('resources/migrate.sql')
        print("AlayaTodo: Database migration applied.")
    else:
        app.run(use_reloader=True)
