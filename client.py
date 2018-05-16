import pygame
from pygame.locals import *
import math

pygame.init()
d=2
fenetre = pygame.display.set_mode((1200,675),FULLSCREEN)
x1=25
y1=25
x2=1120
y2=550
missile1=3

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


#Chargement et collage du deuxieme personnage
perso2 = pygame.image.load("tank2.png").convert_alpha()
position_perso2 = perso2.get_rect()
fenetre.blit(perso2, position_perso2)
position_perso2 = position_perso2.move(x2,y2)

canon2 = pygame.image.load("canon2.png").convert_alpha()
position_canon2 = canon2.get_rect()
fenetre.blit(canon2, position_canon2)
position_canon2 = position_canon2.move(x2,y2)
angle2=180
ori2_1="hor"
canon2_1 = pygame.transform.rotate(canon2,-angle2)


#Chargement et collage des missiles du menu
missilemenu1 = pygame.image.load("MissileMenu.png").convert_alpha()
position_missilemenu1 = missilemenu1.get_rect()
fenetre.blit(missilemenu1, position_missilemenu1)
position_missilemenu1 = position_missilemenu1.move(645,100)

position_missilemenu2 = missilemenu2.get_rect()
fenetre.blit(missilemenu2, position_missilemenu2)
position_missilemenu2 = position_missilemenu2.move(645,150)

position_missilemenu3 = missilemenu3.get_rect()
fenetre.blit(missilemenu3, position_missilemenu3)
position_missilemenu3 = position_missilemenu3.move(645,200)


#Chargement et collage des missiles des joueurs
missile1 = pygame.image.load("Missile.png").convert_alpha()
position_missile1 = missile1.get_rect()
fenetre.blit(missile1, position_missile1)
position_missile1 = position_missile1.move(645,100)

missile2 = pygame.image.load("Missile.png").convert_alpha()
position_missile2 = missile2.get_rect()
fenetre.blit(missile2, position_missile2)
position_missile2 = position_missile2.move(645,100)

#Rafraîchissement de l'écran
fenetre.blit(fond, (0,0))
fenetre.blit(perso1, position_perso1)
fenetre.blit(canon1_1, position_perso1)
fenetre.blit(perso2, position_perso2)
fenetre.blit(canon2, position_perso2)
pygame.display.flip()

#BOUCLE INFINIE
pygame.key.set_repeat(400, 7)
continuer = 1
while continuer==1:
        for event in pygame.event.get():	#Attente des événements
                depx2 = 0
                depy2 = 0
                ori2_2 = "vert"
                cursx2= 0
                cursy2 = 0
                canon2_x = cursx2 - x2 - (canon2_1.get_height()/2)
                canon2_y = cursy2 - y2 - (canon2_1.get_height()/2)
                if (canon2_x)!=0:
                        angle2 = math.degrees(math.atan((canon2_y)/(canon2_x)))
                if canon2_x<0:
                        angle2 = angle2+180
                canon2_1 = pygame.transform.rotate(canon2,-angle2)
                position_perso2 = position_perso2.move(depx2-x2,depy2-y2)
                x2=depx2
                y2=depy2
                if ori2_1 != ori2_2:
                        perso2 = pygame.transform.rotate(perso2,90)
                        if ori2_2== "hor":
                                ori2_1="hor"
                        else:
                                ori2_1="vert"
                position_canon2_1=position_perso2
                position_canon2_1 = position_canon2_1.move(-(canon2_1.get_height()-56)/2,-(canon2_1.get_height()-56)/2)
                     
                
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
                                continuer=0
								

				if missile1 > 0:
						fenetre.blit(missilemenu1,position_missilemenu1)
						if missile1 > 1:
								fenetre.blit(missilemenu1,position_missilemenu2)
								if missile1 > 2:
										fenetre.blit(missilemenu1,position_missilemenu3)
				#Re-collage
				fenetre.blit(fond, (0,0))
				fenetre.blit(perso1, position_perso1)
				fenetre.blit(canon1_1, position_canon1_1)
				fenetre.blit(perso2, position_perso2)
				fenetre.blit(canon2_1, position_canon2_1)
				#Rafraichissement
pygame.display.flip()
