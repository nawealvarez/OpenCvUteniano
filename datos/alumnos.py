from bson.binary import Binary
import pickle
from cv2 import cv2
import pymongo
from datos.connection import Connection
import face_recognition
from cv2 import cv2
import numpy as np

import glob
import os


class AlumnoData():
    
    @staticmethod
    def crearAlumno(alumno):
        db = Connection.connect()
        nuevo =db.alumnos
        nuevo.insert_one(alumno)

    @staticmethod
    def traerAlumnos():
        db = Connection.connect()
        lista = db.alumnos.find({})
        return lista





