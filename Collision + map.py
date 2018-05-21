#charger la map

map = open("Map2_2.txt", "r")
coordonnes = map.read()
ligne2 = coordonnes.split("\n")
tableau = []

for ligne_y in range(0,625):
	for ligne_x in range(0,1200):
		if ligne2[ligne_y][ligne_x] == "1":
			co = [ligne_x, ligne_y]
			tableau.append(co)
		
	

print(tableau[3])

map.close()

#hitbox du missile, angle en radians


def hitbox_missile(self, angle):
	self.b_size_missile_x = 16
	self.b_size_missile_y = 6
	self.b_size_x = math.ceil(self.b_size_missile_x * math.cos(angle))
	self.b_size_y = math.ceil(b_size_missile_y * math.sin(angle))
	return self.b_size_x, self.b_size_y

# collision des murs, les coordonnées arrondies à l'entier
#l'angle est en radian
#les positions sont en entiers

def collision_mur(self, pos_x, pos_y):
	
	pos = [[math.ceil(pos_x), math.ceil(pos_y)], [math.ceil(pos_x+b_size_x), math.ceil(pos_y)], [math.ceil(pos_x+b_size_x), math.ceil(pos_y+b_size_y)], [math.ceil(pos_x), math.ceil(pos_y+b_size_y)]]
	for n in range(0, 3):
		try:
			tableau.index(pos[n])
			return 0
			break	
		except ValueError:
			return 1



#collision entre les entitées

def collision(pos_x1,pos_y1,b_size_x, b_size_y, pos_x2, pos_y2, b_size_x2, b_size_y2):




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





