#João Pedro Mafaldo de Paula
#Engenharia da Computação P1 - CIn -UFPE 01/07/2022
#Nenhuma das bibliotecas utilizadas pertence ou foi desenvolvida pelo Autor do código


#OBJETIVO DO PROGRAMA:
#Receber os valores de dois potenciômetros, 3 botões e um joystick analógico(potenciometro 1 pra o eixo x e pot 2 para o eixo y)
#E transformar esses valores em parâmetros que possam ser utilizados pelas funções: tello.send_rc_control() -- Controle do drone, drone.takeoff(), drone.land()
#E também o recebimento da imagem paralelo ao controle do drone, o que é o verdadeiro desafio aqui
#Tentei resolver o problema usando python threads mas depois que eu invoco a camera (linha 51), o programa para de esperar
#Os valores do analog read para ler e assim controlar o drone

import time
from djitellopy import tello
import serial
import cv2
from threading import Thread

def valDrone(leftRight,frontBackwards,upDown,giroDrone):
    speed=50
#definindo os valores de velocidade com base no input do arduino
    if leftRight<=20:
        leftRight=speed*(-1)
    elif leftRight>=1020:
        leftRight=speed
    else:
        leftRight=0
    
    if frontBackwards<=20: #eixo x do potenciometro que retorna 0 a 1023 em analogRead()
        frontBackwards=speed
    elif frontBackwards>=1020:
        frontBackwards=speed*(-1)
    else:
        frontBackwards=0
    
    if upDown<=20:
        upDown=speed*(-1)
    elif upDown>=1020:
        upDown=speed
    else:
        upDown=0

    if giroDrone<=20:
        giroDrone=speed*(-1)
    elif giroDrone>=1023:
        giroDrone=speed
    else:
        giroDrone=0
    commandList=[leftRight,frontBackwards,upDown,giroDrone]
    #return commandList Acredito que a função nao precisa retornar nada

def botaoVal(flipVal,landVal,takeoffVal):
    if flipVal==0:
        drone.flip_forward()
    if landVal==0:
        drone.land()
    elif takeoffVal==0:
        drone.takeoff()
    listaBotoes=[]
    listaBotoes=[flipVal,landVal,takeoffVal]
    return listaBotoes

drone=tello.Tello()#estabelecendo conexão com o objeto e criando tbm
drone.connect()
arduino=serial.Serial('com7',9600) #como a comunicação com o arduino vai acontecer
time.sleep(1)#para evitar problemas 
drone.streamon()

while True:
    while (arduino.inWaiting()==0): #enquanto a data for igual a 0 o programa vai continuar esperando receber algo pra prosseguir
        pass
    dataPacket=arduino.readline() #recebendo os dados, uma linha do Serial
    #convertendo os dados para o formato desejado
    dataPacket=str(dataPacket, 'utf-8')
    dataPacket=dataPacket.strip('\r\n')
    splitPacket=dataPacket.split(",")
    #me retorna uma lista com strings dos numeros que o arduino me dá
   
    #Agora eu vou transformar cada item[index] da lista em uma variável para usar o send_rc_control do tello
    leftRight=int(splitPacket[0]) #valor do eixo x do joystick
    frontBackwards=int(splitPacket[1]) #valor do eixo y do joystick
    upDown=int(splitPacket[2]) #valor do potenciometro 1
    giroDrone=int(splitPacket[3])
    flipVal=int(splitPacket[4])
    landVal=int(splitPacket[5])
    takeoffVal=int(splitPacket[6])
   
    
    speed=50
#definindo os valores de velocidade e dos botoes com base no input do arduino
   
   #(((((((((((((((((iniciando a thread uma vez
    #if cont==0:
       # botoesThread=Thread(target=botaoVal(camVal,landVal,takeoffVal))
        #botoesThread.daemon=True
       # botoesThread.start()
        #cont=1
    #print(cont))))))))))))))))))
    #NAO CONSEGUI RESOLVER COM UMA THREAD!!!!!!!!
    
    ########AQUI QUE O CÓDIGO COMEÇA DE VERDADE, EM RELAÇÃO AOS VALORES DO ARDUINO E OS COMANDOS DE CONTROLE DO DRONE
    #agora vou converter o analogRead em valores que eu possa utilizar pra controlar o drone
    if leftRight<=20:
        leftRight=speed*(-1)
    elif leftRight>=1020: #Coloquei 1020 em vez de 1023 mas por um pouco de segurança mesmo
        leftRight=speed
    else:
        leftRight=0
    
    if frontBackwards<=20: #eixo x do potenciometro que retorna 0 a 1023 em analogRead()
        frontBackwards=speed
    elif frontBackwards>=1020:
        frontBackwards=speed*(-1)
    else:
        frontBackwards=0
    
    if upDown<=20:
        upDown=speed*(-1)
    elif upDown>=1020:
        upDown=speed
    else:
        upDown=0

    if giroDrone<=20:
        giroDrone=speed*(-1)
    elif giroDrone>=1023:
        giroDrone=speed
    else:
        giroDrone=0
    #Sim, eu poderia ter feito essa parte numa função, mas fiquei com medo de nao dar certo, mas acho que dá sim, por isso ela já tá definida lá em cima :)
    #img = drone.get_frame_read().frame ###remover pra ficar mais leve
    #img = cv2.resize(img, (360, 240)) ###remover pra ficar mais leve
    #cv2.imshow("Image", img) ###remover pra ficar mais leve
    
    drone.send_rc_control(leftRight,frontBackwards,upDown,giroDrone)
    print(leftRight,frontBackwards,upDown,giroDrone)
    botaoVal(flipVal,landVal,takeoffVal)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
    
drone.land()
drone.streamoff()
 
 