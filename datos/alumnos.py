from datos.connection import Connection


class AlumnoData():

    @staticmethod
    def crearAlumno(alumno):
        db = Connection.connect()
        nuevo = db.alumnos
        nuevo.insert_one(alumno)

    @staticmethod
    def traerAlumnos():
        db = Connection.connect()
        lista = db.alumnos.find({})
        return lista
