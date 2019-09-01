from bson.binary import Binary
import pickle
from cv2 import cv2
import pymongo
from connection import Connection

class AlumnoData():
    @staticmethod
    def crearAlumno(alumno):
        db = Connection.connect()
        nuevo =db.alumnos
        nuevo.insert_one(alumno)

img_O = cv2.imread('img/Barack_Obama.png')   # reads an image in the BGR format
img_O = cv2.cvtColor(img_O, cv2.COLOR_BGR2RGB)   # BGR -> RGB
img_L = cv2.imread('img/Luciano_Babaglio.png')   # reads an image in the BGR format
img_L = cv2.cvtColor(img_L, cv2.COLOR_BGR2RGB)
a = {'nombre': 'Barack', 'apellido': 'Obama', 'dni': '789456132'}
b = {'nombre': 'Barack', 'apellido': 'Obama', 'dni': '789456132'}
print('Obama:\n ',len(img_O), '\n','Lucho:\n ', len(img_L))
# Convert numpy array to Binary
a['imagen'] = Binary(pickle.dumps(img_O, protocol=2), subtype=128)
b['imagen'] = Binary(pickle.dumps(img_L, protocol=2), subtype=128)

# alu = AlumnoData()
# alu.crearAlumno(a)

img2_O = pickle.loads(a['imagen'])
img2_L = pickle.loads(b['imagen'])
print('Obama:\n ', len(img2_O), '\n','Lucho:\n ', len(img2_L))






