from flask import Flask, g
import urllib, json, sqlite3, re
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
    url = "http://www.speedrun.com/api/v1/games?embed=categories&max=200"
    response = urllib.urlopen(url)
    data = json.loads(response.read())

    print 'test'

    db = get_db()

    for x in data['data']:
      name = x['names']['international']
      name = re.sub('[^A-Za-z0-9 ()%]+', ' ', name).lstrip()
      consoles = str(x['platforms'])
      logourl = x['assets']['cover-large']['uri']
      for y in x['categories']['data']:
        if y['type'] == 'per-game':
          category = y['name']
          category = re.sub('[^A-Za-z0-9 ()%]+', ' ', category).lstrip()
          lburl = y['weblink']
          print name + ' ' + category
          sql = 'INSERT INTO games VALUES ("' + name + '", "' + consoles + '", "' + category + '", "' + logourl + '", "' + lburl + '")'
          print sql
          db.cursor().execute(sql)
          db.commit()

@app.route("/")
def hello():
  db = get_db()

  page = []
  page.append('<html><body><table bgcolor="#bfbfbf">')
  sql = 'SELECT * FROM games'
  for row in db.cursor().execute(sql):
    page.append('<tr>')
    page.append('<td>')
    page.append(row[0])
    page.append('</td>')
    page.append('<td>')
    page.append(row[2])
    page.append('</td>')
    page.append('<td><a href="')
    page.append(row[4])
    page.append('"><img src="')
    page.append(row[3])
    page.append('"/></a></td>')
    page.append('</tr>')

  page.append('</table></body></html>')
  return ''.join(page)

if __name__ == "__main__":
  app.run(host='0.0.0.0')
