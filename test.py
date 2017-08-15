from flask import Flask
import urllib, json
app = Flask(__name__)


@app.route("/")
def hello():
  url = "http://www.speedrun.com/api/v1/games?embed=categories"
  response = urllib.urlopen(url)
  data = json.loads(response.read())
  return str(json.loads(json.dumps(data)))
  #return "test"

if __name__ == "__main__":
  app.run(host='0.0.0.0')
