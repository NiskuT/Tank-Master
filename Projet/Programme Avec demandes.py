import pygame
from pygame.locals import *
import math

pygame.init()
rotation = "hor"
d=2
angle=0
fenetre = pygame.display.set_mode((1200,675),FULLSCREEN)
x1=25
y1=25
canon1_x=0
canon1_y=0


#Chargement et collage du fond
fond = pygame.image.load("MAP2.png").convert()
fenetre.blit(fond, (0,0))

#Chargement et collage du personnage
perso1 = pygame.image.load("tank4.png").convert_alpha()
position_perso1 = perso1.get_rect()
fenetre.blit(perso1, position_perso1)
position_perso1 = position_perso1.move(x1,y1)


canon1 = pygame.image.load("canon4.png").convert_alpha()
position_canon1 = canon1.get_rect()
fenetre.blit(canon1, position_canon1)
position_canon1 = position_canon1.move(25,25)
orientation1 = 0

canon1_1 = pygame.transform.rotate(canon1,-angle)
position_canon1_1 = canon1.get_rect()

#Chargement et collage des autres personnages
perso2 = pygame.image.load("tank2.png").convert_alpha()
position_perso2 = perso2.get_rect()
fenetre.blit(perso2, position_perso2)
position_perso2 = position_perso2.move(1120,25)

canon2 = pygame.image.load("canon2.png").convert_alpha()
position_canon2 = canon2.get_rect()
fenetre.blit(canon2, position_canon2)
position_canon2 = position_canon2.move(1120,25)
orientation2 = 180

perso3 = pygame.image.load("tank3.png").convert_alpha()
position_perso3 = perso3.get_rect()
fenetre.blit(perso3, position_perso3)
position_perso3 = position_perso3.move(25,550)

canon3 = pygame.image.load("canon3.png").convert_alpha()
position_canon3 = canon3.get_rect()
fenetre.blit(canon3, position_canon3)
position_canon3 = position_canon3.move(25,550)
orientation3 = 180

perso4 = pygame.image.load("tank4.png").convert_alpha()
position_perso4 = perso4.get_rect()
fenetre.blit(perso4, position_perso4)
position_perso4 = position_perso4.move(1120,550)

canon4 = pygame.image.load("canon4.png").convert_alpha()
position_canon4 = canon4.get_rect()
fenetre.blit(canon4, position_canon4)
position_canon4 = position_canon4.move(1120,550)
orientation4 = 0


#Rafraîchissement de l'écran
pygame.display.flip()

#BOUCLE INFINIE
pygame.key.set_repeat(40, 3)
continuer = 1
while continuer==1:
        for event in pygame.event.get():	#Attente des événements
                if event.type == MOUSEMOTION:
                        canon1_x=event.pos[0]-x1-(canon1_1.get_height()/2)
                        canon1_y=event.pos[1]-y1-(canon1_1.get_height()/2)
                        if (canon1_x)!=0:
                                angle = math.degrees(math.atan((canon1_y)/(canon1_x)))

                        if canon1_x<0:
                                angle = angle+180
                                                
                        canon1_1 = pygame.transform.rotate(canon1,-angle)
                        
                if event.type == KEYDOWN:
                        if event.key == K_DOWN:
                                position_perso1 = position_perso1.move(0,d)
                                position_canon1_1 = position_canon1_1.move(0-((canon1_1.get_height()-56)/2),d-((canon1_1.get_height()-56)/2))
                                y1=y1+d
                                if rotation != "vert":
                                        perso1 = pygame.transform.rotate(perso1, 90)
                                        rotation = "vert"
                        if event.key == K_RIGHT:
                                position_perso1 = position_perso1.move(d,0)
                                position_canon1_1 = position_canon1_1.move(0-((canon1_1.get_height()-56)/2),d-((canon1_1.get_height()-56)/2))
                                x1=x1+d
                                if rotation == "vert":
                                        perso1 = pygame.transform.rotate(perso1, -90)
                                        rotation = "hor"
                        if event.key == K_LEFT:
                                position_perso1 = position_perso1.move(-d,0)
                                position_canon1_1 = position_canon1_1.move(0-((canon1_1.get_height()-56)/2),d-((canon1_1.get_height()-56)/2))
                                x1=x1-d
                                if rotation == "vert":
                                        perso1 = pygame.transform.rotate(perso1, -90)
                                        rotation = "hor"
                        if event.key == K_UP:
                                position_perso1 = position_perso1.move(0,-d)
                                position_canon1_1 = position_canon1_1.move(0-((canon1_1.get_height()-56)/2),d-((canon1_1.get_height()-56)/2))
                                y1=y1-d
                                if rotation != "vert":
                                        perso1 = pygame.transform.rotate(perso1, 90)
                                        rotation = "vert"

        #Re-collage
        fenetre.blit(fond, (0,0))
        fenetre.blit(perso1, position_perso1)
        fenetre.blit(canon1_1, position_perso1)
        fenetre.blit(perso2, position_perso2)
        fenetre.blit(canon2, position_perso2)
        fenetre.blit(perso3, position_perso3)
        fenetre.blit(canon3, position_perso3)
        fenetre.blit(perso4, position_perso4)
        fenetre.blit(canon4, position_perso4)
        #Rafraichissement
        pygame.display.flip()


