# All features about flask in _Flask library. example "url_for" and so on.
from ast import parse
import json
import _Flask
import MySQL
# import Path library, even if never use it.
import Path

@_Flask.app.route("/user", methods=["post"])
def user():
  # temppoary direct enter.
  params = {
      "user": "admin"
  }
  
  return _Flask.render_template("Welcom.html", params=params)
  # Get a username and password for post method.
  username = _Flask.request.form["username"]
  password = _Flask.request.form["password"]

  # Get user name and password in MySQL databases.
  usernameFormDatabase, passwordFormDatabase = MySQL.execute("SELECT user_name, password FROM user")

  # Verify user name and password are correct or not.
  if username == usernameFormDatabase and password == passwordFormDatabase:
    params = json.dumps({
      "UserName": username
    })
    print(params["UserName"])
    return _Flask.render_template("Welcom.html", params = params)
  else:
    return _Flask.redirect(_Flask.url_for("root", error = "用户名和密码可能错误"))

# Running flask app with debugger param.
_Flask.app.run(debug=True)