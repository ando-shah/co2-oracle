from flask import Flask, g
import sqlite3

app = Flask(__name__)


# Database helper functions
DATABASE = './output-table.db'

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('output-table-schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def seed_db():
    with app.app_context():
        db = get_db()
        db.execute("INSERT INTO output (parameter, timestamp, co2_ppm) VALUES (?, ?, ?)", ("ss", "1635416378000", "100"))
        db.execute("INSERT INTO output (parameter, timestamp, co2_ppm) VALUES (?, ?, ?)", ("g", "1635416378000", "200"))
        db.execute("INSERT INTO output (parameter, timestamp, co2_ppm) VALUES (?, ?, ?)", ("ssrt", "1635416378000", "300"))
        db.execute("INSERT INTO output (parameter, timestamp, co2_ppm) VALUES (?, ?, ?)", ("grt", "1635416378000", "400"))

        db.commit()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    db.row_factory = sqlite3.Row
    return db

# parser functions

def parse_row(cursor):
    rowObj = cursor.fetchall()[0]

    return {
        "parameter": rowObj["parameter"],
        "timestamp": rowObj["timestamp"],
        "co2_ppm": rowObj["co2_ppm"]
    }

# app routes

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.before_request
def before_request():
    g.cursor = get_db().cursor()

@app.route('/')
def readMe():
    return 'whatever we need here'

@app.route('/ss')
def singleSource():
    g.cursor.execute('SELECT * FROM output WHERE parameter = "ss"')
    return parse_row(g.cursor)

@app.route('/g')
def combinedGlobal():
    g.cursor.execute('SELECT * FROM output WHERE parameter = "g"')
    return parse_row(g.cursor)

@app.route('/ssrt')
def singleSourceRealTime():
    g.cursor.execute('SELECT * FROM output WHERE parameter = "ssrt"')
    return parse_row(g.cursor)

@app.route('/grt')
def combinedGlobalRealTime():
    g.cursor.execute('SELECT * FROM output WHERE parameter = "grt"')
    return parse_row(g.cursor)


# main driver function
if __name__ == '__main__':
    app.run()