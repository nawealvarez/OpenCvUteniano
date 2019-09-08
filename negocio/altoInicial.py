from bson.binary import Binary
import pickle
import face_recognition
import glob
from datos.alumnos import AlumnoData

'''img_O = cv2.imread('img/Fabri.jpg')   # reads an image in the BGR format
img_O = cv2.cvtColor(img_O, cv2.COLOR_BGR2RGB)   # BGR -> RGB
img_L = cv2.imread('img/nico.jpg')   # reads an image in the BGR format
img_L = cv2.cvtColor(img_L, cv2.COLOR_BGR2RGB)

b = {'nombre': 'Barack', 'apellido': 'Obama', 'dni': '789456132'}
#print('Obama:\n ',len(img_O), '\n','Lucho:\n ', len(img_L))
# Convert numpy array to Binary
b['imagen'] = Binary(pickle.dumps(img_L, protocol=2), subtype=128)
'''
contador = 0
listadoImagenes = glob.glob("img/*.*")
known_face_encodings = []
known_face_names = []
for i in listadoImagenes:
    contador += 1
    imagen = face_recognition.load_image_file(str(i))  # Carga la imagen como arreglo vectorial ?
    try:
        cara_reconocida = [face_recognition.face_encodings(imagen)[0]]
        known_face_encodings = known_face_encodings + cara_reconocida  # Busca las caras ?
        a = {'nombre': contador, 'apellido': contador,
             'imagen': Binary(pickle.dumps(cara_reconocida, protocol=2), subtype=128)}
        AlumnoData.crearAlumno(a)
    except:
        pass
    print(contador)
    # if contador == 200:
    #    break
print(len(listadoImagenes), len(known_face_encodings))
