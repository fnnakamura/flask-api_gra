import jaydebeapi

row = {'year': 1989, 'title': "Can''t Stop the Music", 'studios': 'Associated Film Distribution',
       'producers': 'Allan Carr', 'winner': True}

connection = jaydebeapi.connect(
    "org.h2.Driver",
    "jdbc:h2:mem:.",
    ["SA", ""],
    "./infra/h2-2.1.212.jar")
cursor = connection.cursor()
cursor.execute(
    ("DROP TABLE IF EXISTS movies")
)
cursor.execute(
    ("CREATE TABLE IF NOT EXISTS movies ("
     "   id INTEGER PRIMARY KEY AUTO_INCREMENT,"
     "   release_year INTEGER NOT NULL,"
     "   title VARCHAR NOT NULL,"
     "   studios VARCHAR NOT NULL,"
     "   producers VARCHAR NOT NULL,"
     "   winner BOOLEAN,"
     "   created_date DATETIME NOT NULL)")
)
cursor.execute(
    ("INSERT INTO movies VALUES (DEFAULT, {year}, \'{title}\', \'{studios}\', \'{producers}\', {winner}, CURRENT_TIMESTAMP)"
     .format(**row))
)
cursor.execute(
    ("SELECT * FROM movies")
)
print(cursor.fetchall())
cursor.close()
connection.close()
