import json
import Amazon
import os
from flask import Flask
from flask import render_template
from flask import url_for
app = Flask(__name__)


@app.route("/")
def root():
    return render_template("html/index.html")


@app.route("/English")
def English():
    return render_template("html/EnglishRemove.html")


@app.route("/Format")
def Format():
    return render_template("html/Format.html")


@app.route("/getkeyword/<keyword>/<countryName>", methods=["get"])
@app.route("/getkeyword")
def getKeyword(keyword="", countryName="AMAZON_CO_UK"):
    if keyword == "":
        return ["Keyword Error!"]
    return Amazon.returnKeywordList(countryName, keyword)


@app.route("/Download/<data>", methods=["get"])
def Download(data):
    data = json.loads(data)
    for i in data:
        print(data)

    return ""


if __name__ == "__main__":
    # automatic open brower
    os.system(
        '"C:\Program Files\Google\Chrome\Application\chrome.exe" http://localhost:5000')
    app.run(debug=True)
