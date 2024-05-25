
#login form
import pyrebase
import requests

#Configure and Connext to Firebase

firebaseConfig = {
    'apiKey': "AIzaSyB4JVRrM7E2Wg5zz3B111-lNCfYS2sq6A4",
    'authDomain': "matmahoc.firebaseapp.com",
    'projectId': "matmahoc", 
    'storageBucket': "matmahoc.appspot.com",
    'messagingSenderId': "1049703086848",
    'appId': "1:1049703086848:web:c59f95aef94bb34839d1e5",
    'measurementId': "G-GVPDCK6DM7",
    'databaseURL': "https://matmahoc-default-rtdb.firebaseio.com/"
 };

firebase=pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()


#firebase=pyrebase.initialize_app(firebaseConfig)
auth= firebase.auth()

#Login function
email=""
password=""
class loginForm:
    def login(self):
        print("Log in...")
        email=input("Enter email: ")
        password=input("Enter password: ")
        try:
            login = auth.sign_in_with_email_and_password(email, password)
            print("Successfully logged in!")
            return True
        except:
            print("Invalid email or password")
        return False
    
    def getEmail(self):
        return self.email
    def getPass(self):
        return self.password


 

  



        



