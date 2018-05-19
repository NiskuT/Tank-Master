import pygame
from pygame.locals import *
import math

#Variables
tir1="0"

def raffraichissement():
    fenetre.blit(fond, (0,0))
    fenetre.blit(perso1, position_perso1)
    fenetre.blit(canon1_1, position_canon1_1)
    fenetre.blit(perso2, position_perso2)
    fenetre.blit(canon2, position_canon2_1)
    fenetre.blit(missile1_1, position_missile1_1)
    fenetre.blit(missile1_2, position_missile1_2)
    fenetre.blit(missile1_3, position_missile1_3)
    fenetre.blit(missile2_1, position_missile2_1)
    fenetre.blit(missile2_2, position_missile2_2)
    fenetre.blit(missile2_3, position_missile2_3)
    pygame.display.flip()


pygame.init()
fenetre = pygame.display.set_mode((1200,675))

#Menu
fond = pygame.image.load("MENUP.png").convert()
fenetre.blit(fond, (0,0))
pygame.display.flip()

continuer = 0
while continuer==0:
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[1] > 380 and event.pos[1]< 500 and event.pos[0] > 330 and event.pos[0] < 870:
            continuer = 1
        if event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[1] > 550 and event.pos[0] > 1075:
            continuer=2

#ID JOUEUR
ID="2525"

#Collage des objets

#Chargement et collage du fond
fond = pygame.image.load("MAP2.png").convert()
fenetre.blit(fond, (0,0))

#Chargement et collage du personnage
perso1 = pygame.image.load("tank1.png").convert_alpha()
position_perso1 = perso1.get_rect()
position_perso1_1 = perso1.get_rect()
position_perso1_1 = position_perso1.move(25,25)

canon1 = pygame.image.load("canon1.png").convert_alpha()
position_canon1 = canon1.get_rect()
position_canon1_1 = canon1.get_rect()

#Chargement et collage du deuxieme personnage
perso2 = pygame.image.load("tank2.png").convert_alpha()
position_perso2 = perso2.get_rect()
position_perso2_1 = perso2.get_rect()
position_perso2_1 = position_perso2.move(1120,550)

canon2 = pygame.image.load("canon2.png").convert_alpha()
position_canon2 = canon2.get_rect()
position_canon2_1 = canon2.get_rect()

#Chargement et collage des missiles des joueurs
missile1_1 = pygame.image.load("Missile.png").convert_alpha()
position_missile1_1 = missile1_1.get_rect()
missile = missile1_1.get_rect()
position_missile1_1 = position_missile.move(200,645)

missile1_2 = pygame.image.load("Missile.png").convert_alpha()
position_missile1_2 = missile1_2.get_rect()
position_missile1_2 = position_missile.move(150,645)

missile1_3 = pygame.image.load("Missile.png").convert_alpha()
position_missile1_3 = missile1_3.get_rect()
position_missile1_3 = position_missile.move(100,645)

missile2_1 = pygame.image.load("Missile.png").convert_alpha()
position_missile2_1 = missile2_1.get_rect()

missile2_2 = pygame.image.load("Missile.png").convert_alpha()
position_missile2_2 = missile2_2.get_rect()

missile2_3 = pygame.image.load("Missile.png").convert_alpha()
position_missile2_3 = missile2_3.get_rect()

raffraichissement()

#BOUCLE INFINIE
pygame.key.set_repeat(400, 7)
while continuer==1:

        #Attente des événements
        for event in pygame.event.get():
            tableau[]=[liste1[],liste2[],liste3[],liste4[],liste5[],liste6[],liste7[],liste8[])
            #liste[]=[Etat,X,Y,Angle,Chenille]

            #Tank1
            liste[]=tableau[0]
            position_perso1_1=position_perso1.move(liste[1],liste[2])
            canon1_1 = pygame.transform.rotate(canon1,-liste[3])
            position_canon1_1 = position_perso1_1.move(-((canon1_1.get_height()-56)/2),-((canon1_1.get_height()-56)/2))

            #Tank2
            liste[]=tableau[4]
            position_perso2_1=position_perso2.move(liste[1]),liste[2])
            canon2_1 = pygame.transform.rotate(canon2,-liste[3])
            position_canon2_1 = position_perso2_1.move(-((canon2_1.get_height()-56)/2),-((canon2_1.get_height()-56)/2))

            #Missile1_1
            liste[]=tableau[1]
            if liste[0]==0:
                position_missile1_1=position_perso1.move(100,645)
            else:
                position_missile1_1=position_perso2.move(liste[1],liste[2])
                missile1_1 = pygame.transform.rotate(missile,-liste[3])

            
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                tir="1"
            
            if event.type == MOUSEMOTION:
                canon1_x=event.pos[0]-x1-(canon1_1.get_height()/2)
                canon1_y=event.pos[1]-y1-(canon1_1.get_height()/2)
                if (canon1_x)!=0:
                        angle1 = math.degrees(math.atan((canon1_y)/(canon1_x)))
                if canon1_x<0:
                        angle1 = angle1+180

            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                    deplacement1="1"
                if event.key == K_RIGHT:
                    deplacement1="2"
                if event.key == K_UP:
                    deplacement1="3"
                if event.key == K_LEFT:
                    deplacement1="4"

            if event.key == K_ESCAPE:
                continuer=2

            liste2=str(str(angle1)+deplacement1+tir)

            raffraichissement()

