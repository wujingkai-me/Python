from distutils.log import error
import _Flask

@_Flask.app.route("/")
def root(error=""):
  print("error=",error)
  return _Flask.render_template("index.html", error=error)