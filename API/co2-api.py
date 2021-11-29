from flask import Flask, g
import os
import sqlite3
import time
import atexit
#from apscheduler.schedulers.background import BackgroundScheduler


# app = Flask(__name__, instance_relative_config=True)
app = Flask(__name__)
app.url_map.strict_slashes = False


DATABASE = './output-table.db'

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('output-table-schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def seed_db():
    """Seed with dummy data"""
    epochTime = int(time.time())
    with app.app_context():
        db = get_db()
        db.execute("INSERT INTO output (parameter, timestamp, co2_ppm) VALUES (?, ?, ?)", ("smoothed", epochTime, 999999))
        db.execute("INSERT INTO output (parameter, timestamp, co2_ppm) VALUES (?, ?, ?)", ("trend", epochTime, 777777))
        db.commit()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# Routes
def parse_row(cursor):
    rowObj = cursor.fetchall()[0]

    return {
        "parameter": rowObj["parameter"],
        "timestamp": rowObj["timestamp"],
        "co2_ppm": rowObj["co2_ppm"]
    }

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    seed_db()
    print('Initialized the database') 

@app.cli.command('seeddb')
def initdb_command():
    """Seed the database with dummy data"""
    seed_db()
    print('Seeded the database') 

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.before_request
def before_request():
    db = get_db()
    g.cursor = db.cursor()

@app.route('/')
def readMe():
    return 'Welcome to the CO2 PPM Oracle'

@app.route('/smoothed')
def singleSource():
    g.cursor.execute('SELECT * FROM output WHERE parameter = "smoothed"')
    return parse_row(g.cursor)

@app.route('/trend')
def combinedGlobal():
    g.cursor.execute('SELECT * FROM output WHERE parameter = "trend"')
    return parse_row(g.cursor)


# sched = BackgroundScheduler(daemon = True)
# sched.add_job(scraper, 'interval', seconds=10)
# sched.start()

# Shutdown your cron thread if the web process is stopped
# atexit.register(lambda: sched.shutdown(wait=False))

# main driver function
if __name__ == '__main__':
    db = get_db()
    app.run(use_reloader=False)