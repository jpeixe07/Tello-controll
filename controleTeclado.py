#João Pedro Mafaldo de Paula
#Engenharia da Computação P1 - CIn -UFPE 01/07/2022
#Nenhuma das bibliotecas utilizadas pertence ou foi desenvolvida pelo Autor do código


import cv2 #display da imagem e resize do frame recebidos do drone
#import mediapipe #reconhecimento facial otimizado no drone
from djitellopy import tello #controle e conexão do Drone-PC
import keyboard #para receber o input das teclas pelo usuário 
import time #usando um delay para facilitar o controle do Drone
#definir Funções para usar no While True - onde iremos receber imagem e esperar os controles pelo usuário
def KeyboardControle():
    velocidade=50
    leftRight, fowardBackwards, upDown, Giro = 0, 0, 0, 0,
    spdVal=[leftRight,fowardBackwards,upDown,Giro]
    #De acordo com a biblioteca djitellopy, esses são os parâmetros da função
    # drone.send_rc_control(lR, fB, uD, Giro)-- Usaremos esses parâmetros para controlar o drone
    if keyboard.read_key('down')=='down': #Tecla down vai fazer o drone ir para tras
        fowardBackwards = -velocidade
    elif keyboard.read_key('up')=='up': #Tecla up vai fazer o drone ir para frente
        fowardBackwards = velocidade
    if keyboard.read_key('left')=='left': #Tecla left vai fazer o drone ir para esquerda
        leftRight = -velocidade
    elif keyboard.read_key('right')=='right': #Tecla right vai fazer o drone ir para direita
        leftRight = velocidade
    if keyboard.read_key('w')=='w': #tecla w vai fazer o drone subir
        upDown = velocidade
    elif keyboard.read_key('s')=='s': #tecla s vai fazer o drone descer
        upDown = -velocidade
    if keyboard.read_key('a')=='a': #tecla a vai fazer o drone girar
        Giro = -velocidade
    elif keyboard.read_key('d')=='d':
        Giro = velocidade
    ########## Decolar, descer e tirar foto pelo teclado
    
    
    spdVal=[leftRight,fowardBackwards,upDown,Giro]
    print(spdVal)
    return spdVal #o programa ira retornar os valores de direção e velocidade no formato lista
    
width=360
height=240

##conexão com o drone antes do while Loop 
drone = tello.Tello()
drone.connect()
print(drone.get_battery())
#drone.streamon()
while True:
    #myframe=drone.get_frame_read().frame
    #myframe=cv2.resize(myframe,(360,240))
    #if keyboard.read_key('0'):
    ##cv2.imshow("Drone View", myframe)
        ##break 

 #  #      ^^^^^^^^^^^^^^^^^^^^^^
    ######NOVAMENTE, O DILEMA ENTRE CONTROLAR O TELLO E RECEBER SUA IMAGEM, NESSE CASO, É PELO CONFLITO 
    ###DO CVV2.WAITKEY(1) E O KEYBOARD.READ_KEY() (EU ACHO NEH)
    spdVal=[0,0,0,0]
    drone.send_rc_control(spdVal[0],spdVal[1],spdVal[2],spdVal[3])
    spdVal=KeyboardControle()
    drone.send_rc_control(spdVal[0],spdVal[1],spdVal[2],spdVal[3])
    time.sleep(0.5)
    if keyboard.read_key('o')=='o':
        drone.takeoff()
    if keyboard.read_key('l')=='l':
        drone.land()
