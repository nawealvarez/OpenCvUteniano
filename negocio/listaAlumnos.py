from datos.alumnos import AlumnoData
import pickle

imagenes = []
lista_alumnos = []
                
cursor = AlumnoData.traerAlumnos()
for i in cursor:
    lista_alumnos.append(i)
for i in lista_alumnos:
    imagen = pickle.loads(i["imagen"])
    i.update((k, imagen) for k, v in i.items() if k == "imagen")
for document in lista_alumnos:
    print(document["nombre"], "imagen: ", document["imagen"])

print(type(lista_alumnos))