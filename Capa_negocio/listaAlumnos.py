from Capa_datos.alumnos import AlumnoData
import pickle

class AlumnoNeg():
    def listado():
        lista_alumnos = []
        lista_alumnos = AlumnoData.traerAlumnos()
        #list_econdings = []
        for i in lista_alumnos:
            i['imagen']= pickle.loads(i['imagen'])
            #list_econdings.append(img)
        return lista_alumnos

a = AlumnoNeg()
a.listado()