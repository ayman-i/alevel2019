#Written by Ayman Islam (https://www.linkedin.com/in/aymansislam/) between 2017-2019

#Importing the SQL library.
import sqlite3

#Establishing a connection to the database file.
conn = sqlite3.connect("SavesDbase.sqlite")

#Creating a cursor used to execute commands on the database file.
c = conn.cursor()

#Creates the database.
def create_tables():
  c.execute("DROP TABLE IF EXISTS Saves")
  c.execute("CREATE TABLE Saves(save_name text,\
            mapOwned boolean,\
            goldCount integer,\
            lives integer,\
            health integer,\
            key1Found boolean,\
            key2Found boolean,\
            key3Found boolean,\
            medCount integer)")

#Function that returns all of the rows of the database.
def view_table_values(tablename):
  output=[]
  for row in c.execute('SELECT * FROM ("%s")' %tablename):
    output.append(row)
  return output

#Method used to insert another row into the table.
def add_save(save_name,mapOwned,goldCount,lives,health,key1Found,key2Found,key3Found,medCount):
  c.execute("INSERT INTO Saves VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(save_name,mapOwned,goldCount,lives,health,key1Found,key2Found,key3Found,medCount))
  conn.commit()

#Method used to delete rows from the table.
def delete_save(save_name):
  c.execute("DELETE FROM Saves WHERE save_name = '{}';".format(save_name))
  conn.commit()
