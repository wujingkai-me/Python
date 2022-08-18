import flask
from flask import render_template
import os

app = flask.Flask(__name__)

@app.route("/")
def root():
  
  return render_template("html/root.html")

# breasts entrance
@app.route("/breasts")
def breasts():
  rootDir = "static/image/breasts"
  rootDirsFiles = os.listdir(rootDir)
  urls = list()
  for file in rootDirsFiles:
    urls.append(rootDir + "/" + file)

  return render_template("html/breasts.html", urls=urls)


# vaginas entrance
@app.route("/vaginas")
def vagina():
  rootDir = "static/image/vaginas"
  rootDirFiles = os.listdir(rootDir)
  vagina = list()
  for file in rootDirFiles:
    vagina.append(rootDir + "/" + file)
  return render_template("html/vaginas.html", vaginas=vagina)

app.run(debug=True)