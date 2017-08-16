from flask import Flask
import urllib, json
app = Flask(__name__)


@app.route("/")
def hello():
  url = "http://www.speedrun.com/api/v1/games?embed=categories"
  response = urllib.urlopen(url)
  data = json.loads(response.read())

  output = ''

  for x in data['data']:
    output = output + x['names']['international'] + '\n'

  return output

if __name__ == "__main__":
  app.run(host='0.0.0.0')
