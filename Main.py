import flask

app = flask.Flask(__name__, template_folder="./")


@app.route("/")
def root():
    return flask.render_template("testajax.html")


@app.route("/ajax", methods=["get"])
def ajax():
    return "OK"


app.run()
