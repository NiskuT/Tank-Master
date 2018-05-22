import pygame
from pygame.locals import *
import math

pygame.init()
d=1
fenetre = pygame.display.set_mode((1200,675),FULLSCREEN)
x1=25
y1=25
x2=1120
y2=550
boom=0

#Ajout des sons
bip = pygame.mixer.Sound("Bip.wav")
poom = pygame.mixer.Sound("Boom.wav")
tir = pygame.mixer.Sound("Tir.wav")

#Def Colision
def tank_colision(x,y,E):
    boom = 0
    for i in range (56):
        if E[y1][i+x1]==1:
            boom=1
        else:
            if E[y1+56][i+x1]==1:
                boom=1
            else:
                E[y1+56][i+x1]=2
                E[y1][i+x1]=2

    if boom != 0:
        for i in range (56):
            if E[i+y1][x1]==1:
                boom=1
            else:
                if E[i+y1][x1+56]==1:
                    boom=1
                else:
                    E[i+y1][x1]=2
                    E[i+y1][x1+56]=2
    return(boom,E)

fond = pygame.image.load("MENUP.png").convert()
fenetre.blit(fond, (0,0))
pygame.display.flip()

continuer = 0
while continuer==0:
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[1] > 380 and event.pos[1]< 500 and event.pos[0] > 330 and event.pos[0] < 870:
            continuer = 1
            bip.play()
        if event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[1] > 550 and event.pos[0] > 1075:
            continuer=2
            bip.play()

#Création de la map dans un tableau
filin = open('MAP2_2.txt','r')
E=[]
for i in range(675):
    sl=[]
    c = filin.readline()
    #print(c)
    for j in range(len(c)):
        if (c[j] != ' ') and (c[j]!='\n'):
            sl.append(int(c[j]))
    E.append(sl)
filin.close()

#Chargement et collage du fond
fond = pygame.image.load("MAP2.png").convert()
fenetre.blit(fond, (0,0))

#Chargement et collage du personnage
perso1 = pygame.image.load("tank1.png").convert_alpha()
position_perso1 = perso1.get_rect()
fenetre.blit(perso1, position_perso1)
position_perso1 = position_perso1.move(x1,y1)


canon1 = pygame.image.load("canon1.png").convert_alpha()
position_canon1 = canon1.get_rect()
fenetre.blit(canon1, position_canon1)
position_canon1 = position_canon1.move(x1,y1)
position_canon1_1 = canon1.get_rect()
angle1=0
ori1="hor"
canon1_1 = pygame.transform.rotate(canon1,-angle1)

#Chargement et collage des missiles du menu
missile1_1 = pygame.image.load("Missile.png").convert_alpha()
missile = missile1_1
position_missile = missile1_1.get_rect()
position_missile1_1 = missile1_1.get_rect()
position_missile1_1 = position_missile.move(200,645)


#Rafraîchissement de l'écran
fenetre.blit(fond, (0,0))
fenetre.blit(perso1, position_perso1)
fenetre.blit(canon1_1, position_perso1)
fenetre.blit(missile1_1, position_missile1_1)

#BOUCLE INFINIE
pygame.key.set_repeat(400, 7)
while continuer==1:
        for event in pygame.event.get():	#Attente des événements

                tir1=0
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    tir1=1
                    tir.play()
                    
                if event.type == MOUSEMOTION:
                        canon1_x=event.pos[0]-x1-(canon1_1.get_height()/2)
                        canon1_y=event.pos[1]-y1-(canon1_1.get_height()/2)
                        if (canon1_x)!=0:
                                angle1 = math.degrees(math.atan((canon1_y)/(canon1_x)))

                        if canon1_x<0:
                                angle1 = angle1+180
                                                
                        canon1_1 = pygame.transform.rotate(canon1,-angle1)
                        position_canon1_1=position_perso1
                        position_canon1_1 = position_canon1_1.move(-(canon1_1.get_height()-56)/2,-(canon1_1.get_height()-56)/2)
                        
                if event.type == KEYDOWN:
                        if event.key == K_DOWN:
                                position_perso1 = position_perso1.move(0,d)
                                position_canon1_1=position_perso1
                                position_canon1_1 = position_canon1_1.move(0-((canon1_1.get_height()-56)/2),d-((canon1_1.get_height()-56)/2))
                                y1=y1+d
                                if ori1 != "vert":
                                        perso1 = pygame.transform.rotate(perso1, 90)
                                        ori1 = "vert"

                        if event.key == K_RIGHT:
                                position_perso1 = position_perso1.move(d,0)
                                position_canon1_1=position_perso1
                                position_canon1_1 = position_canon1_1.move(0-((canon1_1.get_height()-56)/2),d-((canon1_1.get_height()-56)/2))
                                x1=x1+d
                                if ori1 == "vert":
                                        perso1 = pygame.transform.rotate(perso1, -90)
                                        ori1 = "hor"
                        if event.key == K_LEFT:
                                position_perso1 = position_perso1.move(-d,0)
                                position_canon1_1=position_perso1
                                position_canon1_1 = position_canon1_1.move(0-((canon1_1.get_height()-56)/2),d-((canon1_1.get_height()-56)/2))
                                x1=x1-d
                                if ori1 == "vert":
                                        perso1 = pygame.transform.rotate(perso1, -90)
                                        ori1 = "hor"

                        if event.key == K_UP:
                                position_perso1 = position_perso1.move(0,-d)
                                position_canon1_1=position_perso1
                                position_canon1_1 = position_canon1_1.move(0-((canon1_1.get_height()-56)/2),d-((canon1_1.get_height()-56)/2))
                                y1=y1-d
                                if ori1 != "vert":
                                        perso1 = pygame.transform.rotate(perso1, 90)
                                        ori1 = "vert"
                        if event.key == K_ESCAPE:
                                continuer=2
                                                        
                #Test Colision
                U = E
                boom,U = tank_colision(x1,y1,U)
                if boom == 1:
                    poom.play()
                
                            

                #Re-collage
                fenetre.blit(fond, (0,0))
                fenetre.blit(missile1_1, position_missile1_1)
                fenetre.blit(perso1, position_perso1)
                fenetre.blit(canon1_1, position_canon1_1)
                #Rafraichissement
                pygame.display.flip()

pygame.quit()
