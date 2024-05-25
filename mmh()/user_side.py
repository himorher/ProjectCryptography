from CA import CENTRAL_AUTHORITY

from OFFICE import OFFICE
from BANK import BANK
import os
from charm.core.math.pairing import hashPair as extractor


central_user = CENTRAL_AUTHORITY()

OFFICE          = OFFICE(central_user)
bank     = BANK(central_user)
group = central_user.group
maabe = central_user.maabe
public_parameters = central_user.public_parameters
public_keys = {'BANK': bank.public_key, 'OFFICE': OFFICE.public_key}
secret_keys = {'BANK': bank.secret_key, 'OFFICE': OFFICE.secret_key}
attributes_list = None


def CA_get_attribute(central_user, i = 0):
    author_List = central_user.authority_list()
    attribute_list = []
    if (i == 0 ):
        for author in author_List:
            if (author == "BANK"):
                print ("############## BANK ##############")
                list = bank.attributes_list(central_user.gid)
                for item in list:
                    print (item)
            elif (author == "OFFICE"):
                print ("############## OFFICE ##############")
                list = OFFICE.attributes_list(central_user.gid)
                for item in list:
                    print (item)
        return
    else:
        for author in author_List:
            if (author == "BANK"):
                list = bank.attributes_list(central_user.gid)
                for item in list:
                    attribute_list.append(item)
            elif (author == "OFFICE"):
                list = OFFICE.attributes_list(central_user.gid)
                for item in list:
                    attribute_list.append(item)
            
        return attribute_list
    
def CA_working_screen():
    while (True):
        os.system("clear")
        print ("########### CENTRAL AUTHORITY ###########")
        print ("User: "+central_user.gid)
        print ("\t1. See your attributes.")
        print ("\t2. Get your attributes.")
        print ("\t3. Exit")
        option = input("Type \"1\", \"2\" or \"3\": ")
        while(True):
            if (option == "1"):
                CA_get_attribute(central_user)
                # press anykey to exit
                press = input("Press any key to exit.")
                break
            elif (option == "2"):
                global attributes_list
                attributes_list = CA_get_attribute(central_user=central_user, i = 1)
                print (attributes_list)
                press = input("Press any key to exit.")
                break
            elif (option == "3"):
                central_user.gid = None
                return
            else:
                option = input("Type \"1\", \"2\" or \"3\": ")

def CA_login_screen():
    #login = True
    while (True):
        os.system("clear")
        if(central_user.login()):
            
            os.system("clear")
            CA_working_screen()
            return
        else:
            option = input("Login faild. Do you want to login again? \"y\" or \"n\": ")
            while (True):
                if (option == "y"):
                    break
                elif (option == "n"):
                    return
                else:
                    option = input("Type \"y\" or \"n\": ")

def CA_register_screen():
    while (True):
        central_user.register()
        os.system("clear")
        print ("Create accout successfull")
        press = input("Press any key to exit.")
        return

def CA_first_screen():
    while (True):
        os.system("clear")
        print ("########### CENTRAL AUTHORITY ###########")
        print ("Type \"1\", \"2\" or \"3\": ")
        print ("\t1. Login")
        print ("\t2. Register")
        print ("\t3. Exit")
        option = input ("Your option: ")
        while (True):
            if (option == "1"):
                os.system("clear")
                CA_login_screen()
                break
            if (option == "2"):
                os.system("clear")
                CA_register_screen()
                break
            if (option == "3"):
                os.system("clear") 
                return
            else:
                option = input ("Your option: ")




def BANK_register_screen():
    while (True):
        bank.register()
        os.system("clear")
        print ("Create accout successfull")
        press = input("Press any key to exit.")
        return

def BANK_first_screen():
    while (True):
        os.system("clear")
       
        print ("Type \"1\", \"2\": ")
        print ("\t1. Register")
        print ("\t2. Exit")
        option = input ("Your option: ")
        while (True):
            if (option == "1"):
                os.system("clear")
                BANK_register_screen()
                break
            if (option == "2"):
                os.system("clear") 
                return
            else:
                option = input ("Your option: ")


def main():
    while (True):
        os.system("clear")
    
        print("Central Authority: ")
       
        CA_first_screen()
            
if __name__=="__main__":
    main()
