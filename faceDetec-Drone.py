#João Pedro Mafaldo de Paula
#Engenharia da Computação P1 - CIn -UFPE 01/07/2022
#Nenhuma das bibliotecas utilizadas pertence ou foi desenvolvida pelo Autor do código
#UTILIZEI O MEDIAPIPE PARA FAZER O DRONE DJITELLOPY SEGUIR O MAIOR ROSTO DE UMA PESSOA DETECTADA PELA CAMERA DO DRONE

import cv2
import mediapipe as mp
import time
from djitellopy import tello                   

width=360
height=240
class mpFace:
    #having trouble in importing mediapipe in the class
    def __init__(self):
        self.myface=mp.solutions.face_detection.FaceDetection()
    def Marks(self,frame,):
        frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=self.myface.process(frameRGB)
        faceBoundBoxs=[]
        areaRostos=[]
        listaCentro=[]
        if results.detections != None:
            for face in results.detections:1
            -+
                #creating a shortcut
                bBox=face.location_data.relative_bounding_box
                topLeft=(int(bBox.xmin*width),int(bBox.ymin*height))
                bottomRight=(int((bBox.xmin+bBox.width)*width),int((bBox.ymin+bBox.height)*height))
                Xmin=int(bBox.xmin*width)
                Ymin=int(bBox.ymin*height)
                centerX=int(Xmin+(bBox.width*width)/2)
                centerY=int(Ymin+(bBox.height*height)/2)
                cv2.rectangle(frame,topLeft,bottomRight,(0,255,0),3)
                cv2.circle(frame,(centerX,centerY),5,(0,0,255),-1)
                faceBoundBoxs.append((topLeft,bottomRight)) #2 tuples in a list for each face
                areaFace=int((bBox.width*width)*int(bBox.height*height)) #talvez isso seja redundante   
                areaRostos.append(areaFace) #adicionando no array de areas para cada rosto reconhecido
                listaCentro.append([centerX, centerY])
            if len(areaRostos)!=0:
                i=areaRostos.index(max(areaRostos)) #achando o maior valor de area e retornando
                #medida de segurança para n retornar um valor errado ou mt pequeno
        #oq falta fazer?
        #adicionar uma lista para os centro no eixo X e Y, para ajustar lateralmente o drone
                return areaRostos[i], listaCentro[i] #faceBoundBoxs,
        else:
            return 0, [180,120]

fbRange = [6200, 6800] #os valores de area que eu peguei, levando em conta a dimensão total de 360x240 pixels
#basicamente, se a area for menor q 6200 e diferente de 0 o drone vai avançar
###Agora vamos definir um valor para ele ajustar os eixos verticais e horizontais
def calibracaoEixo(lista):
    #essa vai ser a nossa lista do eixo x e y
    eixoX=0
    eixoY=0
    uDown=0 ##valor de subir e descer do dronw
    yw=0
    if lista:
        eixoX=lista[0]
        eixoY=lista[1]
        if eixoX > 140 and eixoX<210:
            yw=0 ##nao vou fazer nada, ele esta no range desejado
    
        elif eixoX <140:
            yw=-30
    
        elif eixoX>210:
            yw=30
        ##agora os valores de height
        if eixoY > 100 and eixoY < 150:
            uDown=0
    
        elif eixoY<100:
            uDown=20

        elif eixoY>150:
            uDown=-20 ##o drone vai descer
        return uDown, yw
    else:
        return 0,0


findFace=mpFace()
me = tello.Tello() 
me.connect()
print(me.get_battery())
me.streamon()
me.takeoff()


while True:
    myframe = me.get_frame_read().frame
    myframe = cv2.resize(myframe, (360, 240))
    area, centroRosto=findFace.Marks(myframe)
    uD,yaw = calibracaoEixo(centroRosto)
    if area==0:
        fb=0
    if area > fbRange[0] and area < fbRange[1]:
        fb = 0

    elif area > fbRange[1]:
        fb = -20
 
    elif area < fbRange[0] and area != 0:
        fb = 20
    cv2.imshow("Image", myframe)
    print(centroRosto, area)
    me.send_rc_control(0,fb,uD,yaw) #n sei em qual parte colocar
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

me.streamoff()
me.takeoff()
