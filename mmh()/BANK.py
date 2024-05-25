import mysql.connector
import re

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="yes",
  port='3306',
  database='BANK'
)

class BANK:
  def __init__(self, central=None):
    self.central = central
    self.public_key = None
    self.secret_key = None
    if (self.central != None):
      (self.public_key, self.secret_key) = self.central.maabe.authsetup(self.central.public_parameters, 'BANK')

  def getPublicKey(self):
    return self.public_key

  def getSecretKey(self):
    return self.secret_key

  def register(self, gid):
    print ("BANK AUTHORITY ###########################")
    id       = input("Id:            ")
    name     = input("Name:          ")
    year     = input("Year of birth: ")
    role     = input("Role:          ")

    _cursor  = db.cursor()
    query    = ("INSERT INTO BANK (GID, ID, NAME, ROLE, YEAR_OF_BIRTH ) "
            "VALUES ('%s', '%s', '%s', '%s', '%s')")
    _cursor.execute(query%(gid, id, name, role, year))
    db.commit()

  def attributes_list(self, gid):
    query = ("SELECT GID, ID, NAME, ROLE, YEAR_OF_BIRTH FROM BANK " 
            "WHERE GID = '" + gid + "'")
    _cursor = db.cursor()

    _cursor.execute(query)
    x = []
    for (_gid, id, name, role, year) in _cursor:
      x.append(id+"@BANK")
      x.append(name+"@BANK")
      x.append(role+"@BANK")
      x.append(year.date+"@BANK")      
    _cursor.close()
    return x
