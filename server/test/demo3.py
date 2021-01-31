from server.dbs.db import engine_psql, session_psql\

for i in range(111):
    engine_psql.execute("INSERT INTO COMPANY (NAME,AGE,ADDRESS,SALARY) VALUES ('Paul', 32, 'California', 20000.00 );".format(i + 3))
