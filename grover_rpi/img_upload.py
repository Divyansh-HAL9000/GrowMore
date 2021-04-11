import os
from time import sleep
import pyrebase
from firebase import firebase

config = {
    "apiKey": "AIzaSyBjiVMyfvhmMd8U26RU96UYAyuQUZRamPE",
    "authDomain": "igrow-ac1d6.firebaseapp.com",
    'databaseURL': "https://igrow-ac1d6-default-rtdb.firebaseio.com",
    'serviceAccount': "serviceAccount.json",
    'projectId': "igrow-ac1d6",
    'storageBucket': "igrow-ac1d6.appspot.com",
    'messagingSenderId': "110645239562",
    'appId': "1:110645239562:web:ac01445a7fb4326eece4f3",
    'measurementId': "G-4G8HE784QV",
  }
img_dir = "./imgs/"

firebase = firebase.FirebaseApplication('https://igrow-ac1d6-default-rtdb.firebaseio.com/', None)
firebase_ = pyrebase.initialize_app(config)
storage = firebase_.storage()

path_on_cloud = "images/"

def get_imgs():
    images = os.listdir(img_dir)
    return images


if __name__ == "__main__":
    images_old = get_imgs()
    for image in images_old:
        storage.child(path_on_cloud+image).put(img_dir+image)

    while True:
        images_new = get_imgs()
        if images_old != images_new:
            print("new images received, uploading")
            for image in images_old:
                storage.delete(path_on_cloud+image)
            for image in images_new:
                storage.child(path_on_cloud+image).put(img_dir+image)
            images_old = images_new
        else:
            print("same old images ", images_old)
        sleep(5)
