from flask import Flask, g
import urllib, json, sqlite3
app = Flask(__name__)
db_location = 'var/games.db'

def get_db():
  db = getattr(g, 'db', None)
  if db is None:
    db = sqlite3.connect(db_location)
    g.db = db
  return db

def init_db():
  with app.app_context():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
      db.cursor().executescript(f.read())
    db.commit()

def populate_db():
  with app.app_context():
    url = "http://www.speedrun.com/api/v1/games?embed=categories"
    response = urllib.urlopen(url)
    data = json.loads(response.read())

    print 'test'

    db = get_db()

    for x in data['data']:
      name = x['names']['international']
      consoles = str(x['platforms'])
      for y in x['categories']['data']:
        if y['type'] == 'per-game':
          db.cursor().execute('INSERT INTO games VALUES ("' + name + '", "' +
          consoles + '", "' + y['name'] + '")')
          db.commit()

@app.route("/")
def hello():
  db = get_db()

  page = []
  page.append('<html><body><table>')
  sql = 'SELECT * FROM games'
  for row in db.cursor().execute(sql):
    page.append('<tr>')
    page.append('<td>')
    page.append(row[0])
    page.append('</td>')
    page.append('<td>')
    page.append(row[2])
    page.append('</td>')
    page.append('</tr>')

  page.append('</table></body></html>')
  return ''.join(page)

if __name__ == "__main__":
  app.run(host='0.0.0.0')
