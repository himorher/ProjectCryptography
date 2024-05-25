import pyrebase

firebaseConfig = {
  'apiKey': "AIzaSyB4JVRrM7E2Wg5zz3B111-lNCfYS2sq6A4",
  'authDomain': "matmahoc.firebaseapp.com",
  'projectId': "matmahoc",
  'databaseURL': "https://matmahoc-default-rtdb.firebaseio.com/",
  'storageBucket': "matmahoc.appspot.com",
  'messagingSenderId': "1049703086848",
  'appId': "1:1049703086848:web:c59f95aef94bb34839d1e5",
  'measurementId': "G-GVPDCK6DM7"
};

firebase = pyrebase.initialize_app(firebaseConfig)
database= firebase.database()
data= {"IDEmployee": "EM001", "IDEmployee": "EM002"}
database.child("Users").child("GD").set(data)
