
from charm.toolbox.pairinggroup import PairingGroup, GT
from CA import CENTRAL_AUTHORITY
from BANK import BANK
from OFFICE import OFFICE
from charm.core.math.pairing import hashPair as extractor
from charm.toolbox.symcrypto import SymmetricCryptoAbstraction
import pickle
from loginForm import loginForm


login_Form= loginForm()
central  = CENTRAL_AUTHORITY()
bank = BANK(central)
OFFICE      = OFFICE(central)
public_keys = {'BANK': bank.public_key, 'OFFICE': OFFICE.public_key}
secret_keys = {'BANK': bank.secret_key, 'OFFICE': OFFICE.secret_key}
key = central.group.random(GT)
# serialize key
access_policy = '(Huy@BANK and 123@OFFICE) or DR007@BANK'




def encrypt_file(save_path, plaintext_path ):
#read plaintext from file
        sourcefile = open(plaintext_path, 'rb')
        msg = sourcefile.read()
        sourcefile.close()

                    
        user_keys = central.keyGenerator(secret_keys, access_policy)
        
# Create a random key              
        en = SymmetricCryptoAbstraction(extractor(key))
# encrypt the plaintext with AES
        ct = en.encrypt(msg)
#Save ciphertext to file
        ciphertext_path1= save_path + "/" +  plaintext_path[(plaintext_path.rfind('/')+1):-(plaintext_path.rfind('.')-1)]+"_Encrypted"+ plaintext_path[(plaintext_path.rfind('.')):]
        encryptedfile = open(ciphertext_path1, 'wb')
        pickle.dump(ct, encryptedfile)

        print("Create encrypted file successfully!")
        print(ciphertext_path1)
        encryptedfile.close()
#Encrypt the AES key with CPABE               
        cipher_key = central.maabe.encrypt(central.public_parameters, public_keys, key, access_policy)
    
#save keys
        userkeys_path= save_path + "/key1.txt"
        decryptedfile = open(userkeys_path, "w")
        decryptedfile.write(str(user_keys))
        decryptedfile.close()

        ckey_path= save_path+"/key2.txt"
        keyfile= open(ckey_path, "w")
        keyfile.write(cipher_key)
        keyfile.close()

         
        

def decrypt_file( save_path, ciphertext_path,user_keys, cipher_key):
       
       #Decrypt the key
        decrypted_key = central.maabe.decrypt(central.public_parameters, user_keys, cipher_key)
        de = SymmetricCryptoAbstraction(extractor(decrypted_key))


        sourcefile = open(ciphertext_path, 'rb')
        ct = sourcefile.read()
        sourcefile.close()
        pt=de.decrypt(str(ct))

        decryptedfile_path= save_path + "/" +  plaintext_path[(plaintext_path.rfind('/')+1):-(plaintext_path.rfind('.')-1)]+"_Decrypted"+ plaintext_path[(plaintext_path.rfind('.')):]
        
        decryptedfile = open(decryptedfile_path, 'wb')
        decryptedfile.write(pt)

        print("Create decrypted file successfully!")
        print(decryptedfile_path)


        sourcefile = open(plaintext_path, 'rb')
        msg = sourcefile.read()
        decryptedfile_path= save_path + "/" +  plaintext_path[(plaintext_path.rfind('/')+1):-(plaintext_path.rfind('.')-1)]+"_123Decrypted"+ plaintext_path[(plaintext_path.rfind('.')):]
        decryptedfile = open(decryptedfile_path, 'wb')
        decryptedfile.write(msg)
        decryptedfile.close()      
      




if __name__=="__main__":
        if (central.login()): 
                print ("\n\t\t\t\tWelcome ")
                print ("Type \"1\", \"2\" : ")
                print ("\t1. Encrypt")
                print ("\t2. Decrypt")
                option = input("Your option: ")
        
                if (option == "1"):
                        print("Path file to encrypt:\t")
                        plaintext_path = input()
                        print("Path file to save:\t")
                        save_path = input()
                        print("-------------------------------------------------------------------------------")
                        print("Enter access policies: (Example: ( CFO@BANK  or Management@OFFICE )")
                        #access_policy = input()
                        print("\n-------------------------------------------------------------------------------")
                        encrypt_file(save_path,plaintext_path)
                elif (option == "2"):
                        print("Path file to decrypt:\t")
                        ciphertext_path = input()
                        print("Path file to save:\t")
                        save_path = input()
                        print("\n-------------------------------------------------------------------------------")
                        decrypt_file(save_path,ciphertext_path)
                

                
        else:
                print("Username or Password is incorrect!!!")
        
        

