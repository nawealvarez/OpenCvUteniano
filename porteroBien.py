# Buscar --rev para ir comentando lo que no se que hace

import face_recognition
from cv2 import cv2
import numpy as np

#AGREGADO POR JUAN
import glob
import os

#Agregado por nico
import sys
import time

contador_circulo_click = 0
color_circulo_click = ''

# Función que 
ix,iy = -1,-1
def save_face_click(event,x,y,flags,param):
    global ix,iy,contador_circulo_click,color_circulo_click, known_face_encodings, known_face_names, listadoImagenes
    
    if event == cv2.EVENT_LBUTTONDOWN: 
        ix,iy = x,y
        contador_circulo_click = 5
        color_circulo_click = (0,0,255)
        for foto_desconocido in fotos_desconocidos:
            if ix >= foto_desconocido[1]['left'] and ix <= foto_desconocido[1]['right'] \
                and iy >= foto_desconocido[1]['top'] and iy <= foto_desconocido[1]['bottom']:
                
                color_circulo_click = (0,255,0)
                (video_x, video_y, video_w, video_h) = cv2.getWindowImageRect('Video')
                nombreImagen = input("Ingrese el nombre de la imagen: ")
                cv2.imwrite("img/"+nombreImagen+".jpg" , foto_desconocido[0])
                known_face_encodings, known_face_names, listadoImagenes = cargaImagenes()


# Load pictures and learn how to recognize it. MEJORADO POR JUAN
def cargaImagenes():
    listadoImagenes = glob.glob("img/*.*") #trae las rutas de cada imagen dentro de la carpeta img
    known_face_encodings = []
    known_face_names = []
    for i in listadoImagenes:
        imagen = face_recognition.load_image_file(str(i))# Carga la imagen como arreglo vectorial ?
        try:
            known_face_encodings=known_face_encodings+[face_recognition.face_encodings(imagen)[0]] #Busca las caras ?
            known_face_names = known_face_names+[os.path.splitext(os.path.basename(str(i)))[0]] #Agrega el nombre del archivo a los nombres conocidos
        except:
            print ('La siguiente imagen no contiene un rostro reconocible:'+[os.path.splitext(os.path.basename(str(i)))[0]][0])
    return known_face_encodings, known_face_names, listadoImagenes

known_face_encodings, known_face_names, listadoImagenes = cargaImagenes()

    
print('Personas cargadas con imágenes:')
print(known_face_names)

# Get a reference to webcam #0 0 es la cámara de la note, 2 es la camara USB en mi caso.
video_capture = cv2.VideoCapture(0)

#inicializamos frame grilla (pantalla negra para mostrar datos de los usuarios)
grilla = np.zeros((480,1366-640,3), np.uint8)

#Inicializamos el arreglo de ids(nombres) que están siendo captados por la cámara
ids_encontrados = []

#inicializo la lista de fotos con el nombre de cada persona encontrada
fotos_individuales = []
fotos_anteriores = []
nombres_fotos_individuales = []
fotos_desconocidos = []

#Bandera para hacer parpadear los colores de la lista
bandera_color = True

#Buscar que hacen --rev
roi=0
#flagCaptura = False

#saltear frames
busca = 0

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]

    if busca == 0:
        # Find all the faces and face enqcodings in the frame of video
        face_locations = face_recognition.face_locations(rgb_frame,0)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    
    if busca == 8:
        busca = 0
    else:
        busca += 1

    font = cv2.FONT_HERSHEY_DUPLEX #Fuente para las letras de los recuadros

    #hay que sacar el otro? --rev
    roi = 0

    fotos_individuales = []
    nombres_fotos_individuales = []
    fotos_desconocidos = []
    
    # Loop through each face in this frame of video
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

        #top, right, bottom, left vienen del face location de cada cara

        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Desconocida/o"
        
        # If a match was found in known_face_encodings, just use the first one.
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index] #asigna a name el nombre del archivo de la imagen con la que coinicidió   
            ids_encontrados.append(name) #agrega el nombre de coincidencia al arreglo de personas encontradas.
            fotos_individuales.append([frame[top:bottom, left:right],name,{"top": top,"bottom": bottom,"left":left,"right":right}]) #agrego la foto de de la cara a un arreglo de caras encontradas
        else:
            fotos_desconocidos.append([frame[top:bottom, left:right],{"top": top,"bottom": bottom,"left":left,"right":right}]) #agrego la foto de de la cara a un arreglo de caras encontradas desconocidas

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # --rev
        roi = frame[top:bottom, left:right]

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, top - 20), (right, top), (0, 0, 255), cv2.FILLED)

        cv2.putText(frame, name, (left + 6, top - 6), font, 0.4, (104, 197, 219), 1)

        
    for nombre in fotos_individuales:
        nombres_fotos_individuales.append(nombre[1])    
    
    if fotos_anteriores:
        for face in fotos_anteriores:
            if face not in nombres_fotos_individuales:
                cv2.destroyWindow(face)
    
    fotos_anteriores = []

    # Display the resulting image
    cv2.putText(frame, 'CANTIDAD DE PERSONAS AUTORIZADAS: '+str(len(listadoImagenes)), (20, 20), font, 0.5, (255, 255, 255), 1)
    
    #nos fijamos si se hizo click(que contador sea > 0 ) y mostramos el circulo durante x cantidad de framse

    if contador_circulo_click > 0:
        cv2.circle(frame, (ix,iy), 60, color_circulo_click, thickness=-1, lineType=8, shift=0) 
        contador_circulo_click -= 1


    #Este for es para mostrar los nombres, lo reemplazo con los cuadritos.

    cv2.imshow('Video', frame)

    #Funcion para guardar la cara con un click
    cv2.setMouseCallback('Video',save_face_click)

    cv2.imshow('Video', frame)

    #estas 2 lineas son para sacar la barra de la imagen
    cv2.namedWindow('Video',cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Video', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    cv2.moveWindow('Video', -35, -20)
    datos_ventana_video = cv2.getWindowImageRect('Video') #This will return a tuple of (x, y, w, h)

    #Esto es la grilla con fondo negro y datos
    cv2.imshow('grilla',grilla)

    #estas 2 lineas son para sacar la barra de la imagen
    cv2.namedWindow('grilla',cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('grilla', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    #linea para mover la ventana y acomodarlas en la pantalla
    cv2.moveWindow('grilla', datos_ventana_video[0]+datos_ventana_video[2], -20)

    pos_y = 0 #inicia con la posicion en el borde superior
    color = (0,0,208) # establece el color rojo de los rectńgulos

    #Para cada nombre cargado en la carpeta de imágenes, vamos a dibujar un rectángulo, una línea divisora y el nombre de la persona
    for name in known_face_names:
        if ids_encontrados:
            if name == ids_encontrados[-1]:   
                bandera_color = not bandera_color        
        if name in ids_encontrados:
            if bandera_color:
                color = (37,212,107)             
            else:
                color = (255,30,100)
        cv2.rectangle(grilla,(0,pos_y),(20,pos_y+20),color,-1)

        pos_y = pos_y +20
        pos_name = (30,pos_y)
        cv2.putText(grilla, name, pos_name, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (99,111,19), 0, cv2.LINE_AA)
        cv2.line(grilla,(0,pos_y+1),(800,pos_y+1),(97,76,8))
        pos_y = pos_y +2

        color = (0,0,255)

    ids_encontrados = []

    Pos_x_ventanas_individuales = -35
    for face in fotos_individuales:
        cv2.imshow(face[1], cv2.imread('img/'+face[1]+'.jpg'))
        #estas 2 lineas son para sacar la barra de la imagen
        cv2.namedWindow(face[1],cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(face[1], cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        alto_ventanas_individuales = 768-480-20
        Pos_x_ventanas_individuales += alto_ventanas_individuales
        
        cv2.resizeWindow(face[1],alto_ventanas_individuales,alto_ventanas_individuales)#uso el mismo para que sea cuadrada
        cv2.moveWindow(face[1], Pos_x_ventanas_individuales, datos_ventana_video[3])

        fotos_anteriores.append(face[1])


    k = cv2.waitKey(1)
    
    if k == ord('s'):
        if len(fotos_desconocidos) == 1:
            (video_x, video_y, video_w, video_h) = cv2.getWindowImageRect('Video')
            print(video_x, video_y, video_w, video_h)
            print(roi)
            '''
            if not flagCaptura:
                if ((top-20)<):
                    top = 0
                if ((bottom+20)>
                
                if ((left-20)
            '''  
            nombreImagen = input("Ingrese el nombre de la imagen: ")
            cv2.imwrite("img/"+nombreImagen+".jpg" , roi)
            known_face_encodings, known_face_names, listadoImagenes = cargaImagenes()
            flagCaptura= not flagCaptura
        else:
            cv2.putText(frame, 'Para realizar una carga solo debe aparecer una persona en el video', (50, 50), font, 0.8, (0, 0, 0), 2)

    #else:
        #flagCaptura= not flagCaptura	
            
    elif k== ord('q'):
        break
    elif k == ord('a'):
        print(ix,iy)
    


# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()

'''
try:
    print(face_locations[0][2].__name__,face_locations[0][3].__name__)
except:
    pass
'''