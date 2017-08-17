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

@app.route("/")
def hello():
  url = "http://www.speedrun.com/api/v1/games?embed=categories"
  response = urllib.urlopen(url)
  data = json.loads(response.read())

  output = ''

  for x in data['data']:
    name = x['names']['international']
    consoles = x['platforms']
    categories = []
    for y in x['categories']['data']:
      if y['type'] == 'per-game':
        categories.append(y['name'])
    output = output + name + str(consoles) + str(categories) + '<br>'

  return output

if __name__ == "__main__":
  app.run(host='0.0.0.0')
