from bson.binary import Binary
import pickle
from cv2 import cv2
import pymongo
from connection import Connection
import face_recognition
from cv2 import cv2
import numpy as np

import glob
import os

class AlumnoData():
    
    '''def crearAlumno(alumno):
        db = Connection.connect()
        nuevo =db.alumnos
        nuevo.insert_one(alumno)'''
    @staticmethod
    def traerAlumnos():
        db = Connection.connect()
        lista = db.alumnos.find()
        return lista

'''img_O = cv2.imread('img/Fabri.jpg')   # reads an image in the BGR format
img_O = cv2.cvtColor(img_O, cv2.COLOR_BGR2RGB)   # BGR -> RGB
img_L = cv2.imread('img/nico.jpg')   # reads an image in the BGR format
img_L = cv2.cvtColor(img_L, cv2.COLOR_BGR2RGB)

b = {'nombre': 'Barack', 'apellido': 'Obama', 'dni': '789456132'}
#print('Obama:\n ',len(img_O), '\n','Lucho:\n ', len(img_L))
# Convert numpy array to Binary
a['imagen'] = Binary(pickle.dumps(img_O, protocol=2), subtype=128)
b['imagen'] = Binary(pickle.dumps(img_L, protocol=2), subtype=128)'''
'''contador = 0
listadoImagenes = glob.glob("img/dataset/crop_part1/*.*")
known_face_encodings = []
known_face_names = []
alu = AlumnoData()
for i in listadoImagenes:
    contador += 1
    imagen = face_recognition.load_image_file(str(i))# Carga la imagen como arreglo vectorial ?
    try:
        cara_reconocida = [face_recognition.face_encodings(imagen)[0]]
        known_face_encodings=known_face_encodings+cara_reconocida #Busca las caras ?
        a = {'nombre': contador, 'apellido': contador}
        a['imagen'] = Binary(pickle.dumps(cara_reconocida, protocol=2), subtype=128)
        alu.crearAlumno(a)
    except:
        pass
    print(contador)
    if contador == 200:
        break
print(len(listadoImagenes),len(known_face_encodings))'''

'''img2_O = pickle.loads(a['imagen'])
img2_L = pickle.loads(b['imagen'])
print('Obama:\n ', len(img2_O), '\n','Lucho:\n ', len(img2_L))'''






