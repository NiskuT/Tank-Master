import pygame
import math

pygame.init()

#charger la map dans un tableau en 3 dimensions
map = open("Map2_2.txt", "r")
coordonnes = map.read()
ligne2 = coordonnes.split("\n")
tableau = []

for ligne_y in range(0,625):
	for ligne_x in range(0,1200):
		if ligne2[ligne_y][ligne_x] == "1":
			co = [ligne_x, ligne_y]
			tableau.append(co)
		print("x= ", ligne_x,"y= ", ligne_y)
	

print(tableau[3])

map.close()

#initialisation de la fenetre
screen_width=1200
screen_height=750
screen=pygame.display.set_mode([screen_width, screen_height])


#initialisation des entitées , Partie de Lucas
perso = pygame.image.load("Missile.png").convert_alpha()
perso_x = 600
perso_y = 325
screen.blit(perso, (perso_x,perso_y))

tank1 = pygame.image.load("tank1.png").convert_alpha()
mur_x = 600 
mur_y = 375
screen.blit(tank1, (mur_x,mur_y))

fond = pygame.image.load("MAP2.png").convert_alpha()

angle = 36

#Donnée que j'ai grâce à quentin
angle_rad = math.radians(angle)
b_size_missile_x = 16
b_size_missile_y = 6
entite1 = perso
#	Sa postion en x et y et l'angle 

entite2 = tank1
#	Sa position en x et y et son angle




vecteur = [math.cos(angle_rad), math.sin(angle_rad)]


#entite1 => missile
#pos_x/y1 => position du missile b_size_x/y1 => hitbox du missile en rectangle en fonction de l'angle du tir, fait avec trigo.
#entité2 => soit les coordonnées des murs soit les coordonnées d'un autre char 
#pos_x/y2 => positiion de l'entitée 2, b_size => tank ont une hitbox carré, donc le coté y = x , les murs ont une hitbox égale à 0

def collision_mur(entite1, pos_x, pos_y, b_size_x, b_size_y):
	coll = 1
	pos = [[pos_x, pos_y], [pos_x+b_size_x, pos_y], [pos_x+b_size_x, pos_y+b_size_y], [pos_x, pos_y+b_size_y]]
	for n in range(0, 3):
		try:
			tableau.index(pos[n])
			print("Pos =", pos)
			print("collision mur")
			return 0
			break	
		except ValueError:
			print("iln'y a pas de mur")
			return 1

def collision(entite1, pos_x1,pos_y1,b_size_x, b_size_y, entité2, pos_x2, pos_y2, b_size_x2, b_size_y2):
	if pos_x1 <= pos_x2 and pos_x1 + b_size_x >= pos_x2:
		if pos_y1 <= pos_y2 and pos_y1 + b_size_y >= pos_y2:
			conti = 0
			print("conti")
			return conti
	elif pos_x2 <= pos_x1 and pos_x2 + b_size_x2 >= pos_x1:
		if pos_y2 <= pos_y1 and pos_y2 + b_size_y2 >= pos_y1:
			conti = 0
			print("conti2")
			return conti
	return 1

pygame.display.flip()
conti = 1
while conti == 1:
	perso_x = math.ceil(perso_x + vecteur[0]*5)
	perso_y = math.ceil(perso_y + vecteur[1]*5)
	mur_x = math.ceil(mur_x + 0)
	mur_y = math.ceil(mur_y + 0)
	
	
	print("x= ", perso_x, "y = ", perso_y)
	print("x= ", mur_x, "y = ", mur_y)
	print(vecteur[0], vecteur[1])

	b_size_x= math.ceil(b_size_missile_x * math.cos(angle_rad))
	b_size_y = math.ceil(b_size_missile_y * math.sin(angle_rad))
	print("hitbox x = ", b_size_x, " y = ", b_size_y)


	conti = collision(perso, perso_x, perso_y, b_size_x, b_size_y, tank1, mur_x, mur_y, 0, 0)
	conti = collision_mur(tank1, mur_x, mur_y, 56, 56)
	conti = collision_mur(perso, perso_x, perso_y, b_size_x, b_size_y)
	

	screen.blit(fond, (0,0))	
	screen.blit(tank1, (mur_x, mur_y))
	screen.blit(perso, (perso_x,perso_y))
	pygame.display.flip()
	pygame.time.wait(50)
