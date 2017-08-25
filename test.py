from flask import Flask, g, render_template, request
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
    flag = True
    url = "http://www.speedrun.com/api/v1/games?embed=categories&max=200"
    while flag:
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
            category = re.sub('[^A-Za-z0-9 ()%+]+', ' ', category).lstrip()
            lburl = y['weblink']
            print name + ' ' + category
            noExactParticipants = 0
            noUpToParticipants = 0

            if y['players']['type'] == 'exactly':
              noExactParticipants = y['players']['value']
            elif y['players']['type'] == 'up-to':
              noUpToParticipants = y['players']['value']

            sql = 'INSERT INTO games VALUES ("' + name + '", "' + consoles + '", "' + category + '", "' + logourl + '", "' + lburl + '",' + str(noExactParticipants)  + ',' + str(noUpToParticipants) + ')'
            print sql
            db.cursor().execute(sql)
            db.commit()
      flag = False
      for x in data['pagination']['links']:
        if x['rel'] == 'next':
          flag = True
          url = x['uri']

def populate_consoles():
  with app.app_context():
    consoleurl = 'http://www.speedrun.com/api/v1/platforms?max=120'
    response = urllib.urlopen(consoleurl)
    consoledata = json.loads(response.read())

    db = get_db()

    for x in consoledata['data']:
      db.cursor().execute('INSERT INTO consoles VALUES ("' + x['name'] + '", "' + x['id'] + '")')
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
    page.append('<td>')
    page.append(str(row[5]) + ',' + str(row[6]))
    page.append('</td>')
    page.append('</tr>')

  page.append('</table></body></html>')
  return ''.join(page)

@app.route("/player/<count>")
def hello2(count):
  db = get_db()

  page = []
  page.append('<html><body><table bgcolor="#bfbfbf">')
  sql = 'SELECT * FROM games WHERE exactParticipants = ' + count + ' OR upToParticipants >= ' + count 
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
    page.append('<td>')
    page.append(str(row[5]) + ',' + str(row[6]))
    page.append('</td>')
    page.append('</tr>')

  page.append('</table></body></html>')
  return ''.join(page)

@app.route("/test/")
def test():
  db = get_db()

  page = []
  page.append('<html><body><table bgcolor="#bfbfbf" border="1">')
  sql = 'SELECT * FROM games'
  for row in db.cursor().execute(sql):
    page.append('<tr>')
    page.append('<td>')
    page.append(row[0])
    page.append('</td>')
    page.append('<td>')
    page.append(row[1])
    page.append('</td>')
    page.append('<td>')
    page.append(row[2])
    page.append('</td>')
    page.append('<td>')
    page.append(row[3])
    page.append('</td>')
    page.append('<td>')
    page.append(row[4])
    page.append('</td>')
    page.append('<td>')
    page.append(str(row[5]))
    page.append('</td>')
    page.append('<td>')
    page.append(str(row[6]))
    page.append('</td>')
    page.append('</tr>')

  page.append('</table></body></html>')
  return ''.join(page)

@app.route("/form/", methods=['GET', 'POST'])
def form():
  if request.method == 'POST':
    consoleIDs = []
    for console in request.form:
      consoleIDs.append(console)

    sql = 'SELECT * FROM games WHERE '
    for ID in consoleIDs:
      sql += 'consoles LIKE \'%' + ID + '%\' OR '

    sql = sql[:-3]

    sql += 'ORDER BY RANDOM() LIMIT 1'

    db = get_db()

    game = ''
    print sql
    for row in db.cursor().execute(sql):
      game = str(row)

    return game
  else:
    db = get_db()

    sql = 'SELECT * FROM consoles'
    consoles = []
    for row in db.cursor().execute(sql):
      consoles.append(row)

    return render_template('test.html', consoles=consoles)

@app.route("/html/")
def html():
    db = get_db()

    basesql = 'SELECT * FROM consoles '
    letters = ['0%\' OR name LIKE \'1%\' OR name LIKE \'2%\' OR name LIKE \'3%\' OR name LIKE \'4%\' OR name LIKE \'5%\' OR name LIKE \'6%\' OR name LIKE \'7%\' OR name LIKE \'8%\' OR name LIKE \'9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    consoles = []
    for i in range(27):
      consoles.append([])
      sql = basesql + 'WHERE lower(name) LIKE \'' + letters[i]  + '%\''
      for row in db.cursor().execute(sql):
        consoles[i].append(row)

    return render_template('index.html', consoles=consoles)

@app.route("/result/", methods=['POST'])
def result():
  return str(request.form)

if __name__ == "__main__":
  app.run(host='0.0.0.0')
