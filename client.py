# coding: utf-8
#!/usr/bin/env python
import pygame
from pygame.locals import *
import math
import socket
from threading import Thread, RLock
import threading
import pickle
import time

#Variables
tir1=0
angle1=0
deplacement1=0
lock = RLock()
donnee = []

def setPos(lst):
    pos = lst

def raffraichissement():
    fenetre.blit(fond, (0,0))
    fenetre.blit(perso1, position_perso1_1)
    fenetre.blit(canon1_1, position_canon1_1)
    fenetre.blit(perso2, position_perso2_1)
    fenetre.blit(canon2_1, position_canon2_1)
    fenetre.blit(missile1_1, position_missile1_1)
    fenetre.blit(missile1_2, position_missile1_2)
    fenetre.blit(missile1_3, position_missile1_3)
    fenetre.blit(missile2_1, position_missile2_1)
    fenetre.blit(missile2_2, position_missile2_2)
    fenetre.blit(missile2_3, position_missile2_3)
    pygame.display.flip()

def connect(name):
        TCP_IP = "192.168.1.38"
        TCP_PORT = 7089

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send(name.encode('utf-8'))
        data = (s.recv(1024)).decode('utf-8')
        s.close()

        print("received data:", data)


        mdp = data[0]+data[1]+data[2]+data[3]
        IDjoueur = data[4]

        global password
        global ID
        password = int(mdp)
        ID = int(IDjoueur)

class udpSocket(threading.Thread):
        def __init__(self):
                threading.Thread.__init__(self)
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
                UDP_IP = "192.168.1.38"
                UDP_PORT = 12000
                self.sock.bind((UDP_IP, UDP_PORT))
                self.pos = [[1,0,0,40,30,60,0],[1,0,0,20,10,30,0],[1,0,0,50,100,190,0],[0,0,0,20,10,30,0],[1,0,0,400,300,200,1],[0,0,0,20,10,30,0],[0,0,0,20,10,30,0],[0,0,0,20,10,30,0]]

        def run(self):
                while(1):
                        with lock:
                                self.sock.sendto(pickle.dumps(donnee), ("192.168.1.38", 33108))
                        time.sleep(.035)
                        data, addr = self.sock.recvfrom(2048)
                        self.pos = pickle.loads(data)
                        print("\n",self.pos)



pygame.init()
fenetre = pygame.display.set_mode((1200,675))

#Menu
fond = pygame.image.load("MENUP.png").convert()
fenetre.blit(fond, (0,0))
pygame.display.flip()

#Collage du son
bip = pygame.mixer.Sound("Bip.wav")
boom = pygame.mixer.Sound("Boom.wav")
tir = pygame.mixer.Sound("Tir.wav")

continuer = 0
while continuer==0:
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[1] > 380 and event.pos[1]< 500 and event.pos[0] > 330 and event.pos[0] < 870:
                bip.play()
                continuer = 1
        if event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[1] > 550 and event.pos[0] > 1075:
                continuer=2
                bip.play()


#Collage des objets

#Chargement et collage du fond
fond = pygame.image.load("MAP2.png").convert()
fenetre.blit(fond, (0,0))

#Chargement et collage du personnage
perso1 = pygame.image.load("tank1.png").convert_alpha()
perso1_1=perso1
position_perso = perso1.get_rect()
position_perso1_1 = perso1.get_rect()
position_perso1_1 = position_perso.move(25,25)

canon1 = pygame.image.load("canon1.png").convert_alpha()
canon1_1=canon1
position_canon1 = canon1.get_rect()
position_canon1_1 = canon1.get_rect()
position_canon1_1 = position_perso1_1

#Chargement et collage du deuxieme personnage
perso2 = pygame.image.load("tank2.png").convert_alpha()
perso2_1=perso2
position_perso2_1 = perso2.get_rect()
position_perso2_1 = position_perso.move(1120,550)

canon2 = pygame.image.load("canon2.png").convert_alpha()
canon2_1=canon2
position_canon2 = canon2.get_rect()
position_canon2_1 = canon2.get_rect()
position_canon2_1 = position_perso2_1

#Chargement et collage des missiles des joueurs
missile1_1 = pygame.image.load("Missile.png").convert_alpha()
missile = missile1_1
position_missile = missile1_1.get_rect()
position_missile1_1 = missile1_1.get_rect()
position_missile1_1 = position_missile.move(200,645)

missile1_2 = pygame.image.load("Missile.png").convert_alpha()
position_missile1_2 = missile1_2.get_rect()
position_missile1_2 = position_missile.move(150,645)

missile1_3 = pygame.image.load("Missile.png").convert_alpha()
position_missile1_3 = missile1_3.get_rect()
position_missile1_3 = position_missile.move(100,645)

missile2_1 = pygame.image.load("Missile.png").convert_alpha()
position_missile2_1 = missile2_1.get_rect()
position_missile2_1=position_missile.move(400,645)

missile2_2 = pygame.image.load("Missile.png").convert_alpha()
position_missile2_2 = missile2_2.get_rect()
position_missile2_2=position_missile.move(450,645)

missile2_3 = pygame.image.load("Missile.png").convert_alpha()
position_missile2_3 = missile2_3.get_rect()
position_missile2_3=position_missile.move(500,645)

raffraichissement()

#BOUCLE INFINIE
pygame.key.set_repeat(400, 7)

connect("Michelle")
monSocket = udpSocket()
monSocket.start()

while continuer==1:
        #Attente des événements
        tableau = monSocket.pos
        for event in pygame.event.get():
            
            #[[1,40,30,60,0],[1,20,10,30,0],[1,50,100,190,0],[0,20,10,30,0],[1,400,300,200,1],[0,20,10,30,0],[0,20,10,30,0],[0,20,10,30,0]]
            #liste[]=[Etat,X,Y,Angle,Chenille]
            #Tank1

            try:
                liste=tableau[0]
            except:
                pass

            #print(liste)
            if liste[0]==2:
                boom.play()
            x1=liste[3]
            y1=liste[4]
            position_perso1_1=position_perso.move(x1,y1)
            canon1_1 = pygame.transform.rotate(canon1,-math.degrees(liste[5]))
            position_canon1_1 = position_perso1_1.move(-((canon1_1.get_height()-56)/2),-((canon1_1.get_height()-56)/2))
            if liste[6]==1:
                perso1 = perso1_1
                perso1 = pygame.transform.rotate(perso1_1, 90)
                

            #Tank2
            if liste[0]==2:
                boom.play()
            liste=tableau[4]
            x2=liste[3]
            y2=liste[4]
            position_perso2_1=position_perso.move(x2,y2)
            canon2_1 = pygame.transform.rotate(canon2,-math.degrees(liste[5]))
            position_canon2_1 = position_perso2_1.move(-((canon2_1.get_height()-56)/2),-((canon2_1.get_height()-56)/2))
            if liste[6]==1:
                perso2 = perso2_1
                perso2 = pygame.transform.rotate(perso2_1, 90)
                
            #Missile1_1
            liste=tableau[1]
            if liste[0]==0:
                position_missile1_1=position_missile.move(100,645)
            else:
                position_missile1_1=position_missile.move(liste[3],liste[4])
                missile1_1 = pygame.transform.rotate(missile,-math.degrees(liste[5]))

            #Missile1_2
            liste=tableau[2]
            if liste[0]==0:
                position_missile1_2=position_missile.move(150,645)
            else:
                position_missile1_2=position_missile.move(liste[3],liste[4])
                missile1_2 = pygame.transform.rotate(missile,-math.degrees(liste[5]))


            #Missile1_3
            liste=tableau[3]
            if liste[0]==0:
                position_missile1_3=position_missile.move(200,645)
            else:
                position_missile1_3=position_missile.move(liste[3],liste[4])
                missile1_3 = pygame.transform.rotate(missile,-math.degrees(liste[5]))


            #Missile2_1
            liste=tableau[5]
            if liste[0]==0:
                position_missile2_1=position_missile.move(400,645)
            else:
                position_missile2_1=position_missile.move(liste[3],liste[4])
                missile2_1 = pygame.transform.rotate(missile,-math.degrees(liste[5]))


            #Missile2_2
            liste=tableau[6]
            if liste[0]==0:
                position_missile2_2=position_missile.move(450,645)
            else:
                position_missile2_2=position_missile.move(liste[3],liste[4])
                missile2_2 = pygame.transform.rotate(missile,-math.degrees(liste[5]))


            #Missile2_3
            liste=tableau[7]
            if liste[0]==0:
                position_missile2_3=position_missile.move(500,645)
            else:
                position_missile2_3=position_missile.move(liste[3],liste[4])
                missile2_3 = pygame.transform.rotate(missile,-math.degrees(liste[5]))

            #Evenements
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                tir1=1
            
            if event.type == MOUSEMOTION:
                canon1_x=event.pos[0]-x1-(canon1_1.get_height()/2)
                canon1_y=event.pos[1]-y1-(canon1_1.get_height()/2)
                if (canon1_x)!=0:
                        angle1 = math.degrees(math.atan((canon1_y)/(canon1_x)))
                if canon1_x<0:
                        angle1 = angle1+180

            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                    deplacement1=1
                if event.key == K_RIGHT:
                    deplacement1=2
                if event.key == K_UP:
                    deplacement1=3
                if event.key == K_LEFT:
                    deplacement1=4
                if event.key == K_ESCAPE:
                    continuer=2

            if tir1==1:
                tir.play()
                
            with lock:
                donnee=[ID, password, round(angle1,2),deplacement1,tir1,continuer]
            tir1=0
            deplacement1=0
            raffraichissement()


pygame.quit()
