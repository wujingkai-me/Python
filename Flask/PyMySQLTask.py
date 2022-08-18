import MySQL1
sql = "INSERT INTO user VALUE(%d, %s, %s)" % (3, 'kai', '333')
# print(sql)
MySQL1.execute(sql)
# MySQL1.execute("SELECT * FROM user")