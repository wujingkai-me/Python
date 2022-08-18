import pymysql

connection = pymysql.connect(host='localhost',
                            user='root',
                            password='123123',
                            db='flask_app',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)

def execute(sql):
  with connection:
    possibleParam = ["SELECT", "select"]
    
    if sql.split(" ")[0] in possibleParam:
      with connection.cursor() as cursor:
        cursor.execute(sql)
        for items in cursor.fetchall():
          for key, value in items.items():
            print(key + ": " + str(value))
    else:
      with connection.cursor() as cursor:
        cursor.execute(sql)
      connection.commit()
      print("OK")