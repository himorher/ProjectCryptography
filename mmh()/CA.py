from charm.toolbox.pairinggroup import PairingGroup
from maabeRW15 import MaabeRW15
import mysql.connector
from charm.toolbox.pairinggroup import *
import re
from OFFICE import OFFICE            # get uit attributes
from BANK import BANK  # get  attributes
from charm.toolbox.pairinggroup import *


db=mysql.connector.connect(host="localhost",
  user="root",
  password="yes",
  port='3306',
  database='CENTRAL_AUTHORITY')

class CENTRAL_AUTHORITY:
        def __init__(self, gid=None):
            # share parameter
            self.group = PairingGroup('SS512')
            self.maabe = MaabeRW15(self.group)
            self.public_parameters = self.maabe.setup()
            #self.secret_key_dict = None
            # user session
            self.gid = gid
        
        def user_is_exist(self, username):
            _cursor = db.cursor()
            query = ("SELECT USER_NAME FROM LOGIN "
                    "WHERE USER_NAME='%s'")
            _cursor.execute(query%(username))
            for (_user) in _cursor:
                print(_user)
                if (_user != None):
                    return True
            return False
        
        def register(self):
            print ("########### AUTHORITY REGISTER ###########")
            username = input("user name: ")
            while (self.user_is_exist(username)):
                print ("User already exists. Try another username.")
                username = input("user name: ")
            password = input("password:  ")
            _cursor = db.cursor()
            if (True):
                if (True):
                    query = ("INSERT INTO LOGIN (USER_NAME, PASSWORD) "
                            "VALUES ('%s', '%s')")
                    _cursor.execute(query%(username, password))
                    db.commit()                   
                    author = "" # to save the user authorities
                    # create attribute list in hospital
                    choose = input("Set attributes for Bank? [yes/no]")
                    while (choose == "yes" or choose == "no"):
                        if (choose == "yes"):
                            author  += "BANK"
                            Bank = BANK()
                            Bank.register(username)
                            break
                        elif (choose == "no"):
                            break
                        else:
                            choose = input("Please type \"yes\" or \"no\":")

                    if (author != ""):
                        author += ", "

                    # create attribute list in uit
                    choose = input("Set attributes for OFFICE? [yes/no]")
                    while (choose == "yes" or choose == "no"):
                        if (choose == "yes"):
                            author += "OFFICE"
                            OFFICE = OFFICE()
                            OFFICE.register(username)
                            break
                        elif (choose == "no"):
                            break
                        else:
                            choose = input("Please type \"yes\" or \"no\"")
                    query = ("INSERT INTO AUTHORITIES (GID, AUTHORITIES) "
                            "VALUES ('%s', '%s')")
                    _cursor.execute(query%(username, author))
                    db.commit()
                    return True
            return False
        
        def login(self):
            print ("\t\t\t\t Login User ")
            username = input("User name: ")

            password = input("Password:  ")
            _cursor = db.cursor()
            query = ("SELECT USER_NAME, PASSWORD FROM LOGIN "
                    "WHERE USER_NAME='%s'")
            _cursor.execute(query%(username))
            for (user, pswd) in _cursor:
                #print ('pswd: '+pswd)
                if (password == pswd):
                    self.gid = username
                    return True
            return False


        def authority_list(self):
            _cursor = db.cursor()
            query = ("SELECT AUTHORITIES FROM AUTHORITIES " 
                    "WHERE GID = '" + self.gid + "'")
            _cursor.execute(query)
            x = None
            for (b) in _cursor:
                x = re.split(r', ', b[0])
            _cursor.close()
            return x
        
        def keyGenerator(self, secret_key_dict=None, attributes_list_str=None):
            if ( secret_key_dict != None and attributes_list_str != None):
                user_keys  = []
                _bank  = []
                _OFFICE       = []
                authorList = []
                policy = self.maabe.util.createPolicy(attributes_list_str)
            
                attributes_list = self.maabe.util.getAttributeList(policy)

                for attr_auth in attributes_list:
                    (_, auth) = re.split(r"@",attr_auth)
                    if (auth == "BANK"):
                        _bank.append(attr_auth)
                        if (auth not in authorList):
                            authorList.append(auth)
                    elif (auth == "OFFICE"):
                        _OFFICE.append(attr_auth)
                        if (auth not in authorList):
                            authorList.append(auth)
                
                for author in authorList:
                        if (author == "BANK"):
                                #gid = self.gid
                                attributes = _bank
                                user_key = self.maabe.multiple_attributes_keygen(self.public_parameters, 
                                                                                secret_key_dict["BANK"], 
                                                                                self.gid, 
                                                                                attributes)
                                user_keys.append(user_key)

                        elif (author == "OFFICE"):
                                attributes = _OFFICE
                                user_key = self.maabe.multiple_attributes_keygen(self.public_parameters, 
                                                                                secret_key_dict["OFFICE"], 
                                                                                self.gid, 
                                                                                attributes)
                                user_keys.append(user_key)
                return {'GID': self.gid, 'keys': MaabeRW15.merge_dicts(user_keys)}
