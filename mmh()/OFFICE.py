import mysql.connector
import re

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="yes",
  port='3306',
  database='OFFICE'
)

class OFFICE:
  def __init__(self, central=None):
    self.central = central
    self.public_key = None
    self.secret_key = None
    if (self.central != None):
      (self.public_key, self.secret_key) = central.maabe.authsetup(central.public_parameters, 'OFFICE')
  
  def getPublicKey(self):
    return self.public_key

  def getSecretKey(self):
    return self.secret_key
  
  def register(self, gid):
    print ("OFFICE AUTHORITY ####################################")
    id       = input("Id:            ")
    name     = input("Name:          ")
    role     = input("Role:          ")
    year     = input("Year of birth: ")

    _cursor  = db.cursor()
    query    = ("INSERT INTO OFFICE (GID, ID, NAME, ROLE, YEAR_OF_DATE) "
               "VALUES ('%s', '%s', '%s', '%s', '%s')")
    _cursor.execute(query%(gid, id, name, role, year))
    db.commit()

  def attributes_list(self, gid):
      _cursor = db.cursor()
      query = ("SELECT GID, ID, NAME,  ROLE, YEAR_OF_DATE FROM OFFICE " 
              "WHERE GID = '" + gid + "'")
      _cursor.execute(query)
      x = []
      for (_gid, id, name, role, year) in _cursor:
        x.append(id+"@OFFICE")
        x.append(name+"@OFFICE")
        x.append(role+"@OFFICE")
        x.append(year+"@OFFICE")
      _cursor.close()
      return x