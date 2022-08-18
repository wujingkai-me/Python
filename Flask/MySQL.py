import pymysql

MySQLDB = pymysql.Connect(
    host="localhost",
    port=3306,
    user="root",
    passwd="123123",
    db="flask_app",
    charset="utf8"
)
# 上次执行结果
previous = list()
# print(MySQLDB.cursor())
cursor = MySQLDB.cursor()

def execute(sql:str):
  global cursor, previous
  cursor.execute(sql)
  previous = cursor.fetchall()
  if "SELECT" in sql or "select" in sql:
    return select()

  MySQLDB.commit()

def select():
  values = []
  for statement in previous:
    for inStatement in statement:
      print(inStatement)
  return previous

  return ('admin', 'admin1312')

def close():
  cursor.close()

execute("SELECT * FROM user;")