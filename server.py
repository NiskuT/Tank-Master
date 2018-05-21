#!/usr/bin/env python
# coding: utf-8
import math
import socket
from threading import Thread, RLock
import threading
from random import randrange, randint
import time
import pickle

nbPlayer = 0
nbMaxPlayer = 4
lock = RLock()
mainLock = RLock()
workLocker = RLock()
player = []
needToDO =[]
allIP =["192.168.1.38"]
b_size_missile_x = -16
b_size_missile_y = -6



socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketTCP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socketTCP.bind(("", 7089))

socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socketUDP.bind(("192.168.1.38", 33108))



#def collision(XA,YA, a, ID, xb, yb, ab, idb):

#def check():
#	collision joueur joueur
#	collision joueur map
#	collision joueur missile
#	collision missile map
#	collision missile missile


def initMap():
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
	

	print(tableau)

	map.close()

class waitForConnection(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		while True:
			socketTCP.listen(15)
			print("Wainting for connection")
			(client, (ip, port)) = socketTCP.accept()
			newClient = threadTcpConnection(ip, port, client)
			newClient.start()






class threadTcpConnection(threading.Thread):

	def __init__(self, ip, port, client):
		threading.Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.client = client
		print("Tentative de connection entrante...")
		
	def run(self):
		print("Client %s %s join the game." % (self.ip, self.port))
		with lock:
			if nbPlayer < nbMaxPlayer:
				password = str(randint(1000, 9999))
				nom, ip = self.client.recvfrom(1024)
				#allIP.append(str(ip))
				idClient = str(len(player))
				self.client.send((password+idClient).encode('utf-8'))
				connection(nom.decode('utf-8'), password)
				self.client.close()




class liveDataReceive(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)	

	def run(self):
		while True:
			data = (socketUDP.recv(1024))

			with lock:
				needToDO.append(pickle.loads(data))

				#{9}{9999}{3.14}{4}{1}


####Controler que les données ne soient pas trop différentes des précédentes


class mainMover(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)



	def run(self):
		while(1):
			action = []
			with mainLock:
				try:
					action = needToDO[-1]
					del needToDO[-1]
				except:
					pass
				try:
					ID = int(action[0])

					if ID <= 9:
						if player[ID].password == str(action[1]):
							player[ID].changeAngle(math.radians(float(action[2])))
							player[ID].move(int(action[3]))

							if (player[ID].maxMissile > len(player[ID].shot)) and action[4] == 1:
								player[ID].shot.append(missile(player[ID].position_x,player[ID].position_y, player[ID].angle))
				except IndexError:
					continue

class mainWorker(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		self.data = ""

	def run(self):
		while(1):
			positions = []
			
			####missiles#####
			for k in range(2):
				try:
					positions.append([player[k].isAlive,player[k].tailleX, player[k].tailleY, round(player[k].position_x, 2), round(player[k].position_y,2) , round(player[k].angle,2) , player[k].chenille, k])
				except IndexError:
					positions.append([0,0,0,0,0,0,0,0])

				for x in range(3):
					try:
						with workLocker:
							player[k].shot[x].move()
						positions.append([player[k].shot[x].state, player[k].shot[x].tailleX, player[k].shot[x].tailleY, round(player[k].shot[x].x,2) , round(player[k].shot[x].y,2), round(player[k].shot[x].angle,2) , k, x])
					except IndexError:
						positions.append([0,0,0,0,0,0,0,0])


			####colisions######
			#for t in range(len(positions)):
			#	if positions[t][0]== 1 :
			#		if (self.collision_mur(positions[t][3], positions[t][4], positions[t][1], positions[t][2])) == 0:
			#			if t == 0 or t == 4:
			#				player[positions[t][7]].kill()
			#			else:
			#				player[positions[t][6]].shot[positions[t][7]].destroy()
			#				player[positions[t][6]].shot[positions[t][7]]
#
			#		for u in range(len(positions)):
			#			if t == u:
			#				continue
			#			elif self.collision(positions[t][3], positions[t][4], positions[t][1], positions[t][2], positions[u][3], positions[u][4], positions[u][1], positions[u][2]) == 0:
			#				if t == 0 or t == 4:
			#					player[positions[t][7]].kill()
			#				else:
			#					player[positions[t][6]].shot[positions[t][7]].destroy()
			#					del player[positions[t][6]].shot[positions[t][7]]

			####envoie####

			self.sender(positions)

			time.sleep(.035)
			#mettre seulement le Thread en pause <><><>




	def sender(self, serverData):

		data = pickle.dumps(serverData)
		for k in allIP:
			try:
				socketUDP.sendto(data, (str(k), 12000))
				socketUDP.sendto(data, (str(k), 13000))
			except socket.gaierror:
				print("Not found!")

	def collision_mur(pos_x, pos_y, b_size_x, b_size_y):
		pos = [[pos_x, pos_y], [pos_x+b_size_x, pos_y], [pos_x+b_size_x, pos_y+b_size_y], [pos_x, pos_y+b_size_y]]
		for n in range(0, 3):
			try:
				tableau.index(pos[n])
				print("Pos =", pos)
				print("collision mur")
				return 0
				break	
			except ValueError:
				pass
		return 1

	def collision(pos_x1,pos_y1,b_size_x, b_size_y, pos_x2, pos_y2, b_size_x2, b_size_y2):
		if pos_x1 <= pos_x2 and pos_x1 + b_size_x >= pos_x2:
			if pos_y1 <= pos_y2 and pos_y1 + b_size_y >= pos_y2:
				print("conti")
				return 0
		elif pos_x2 <= pos_x1 and pos_x2 + b_size_x2 >= pos_x1:
			if pos_y2 <= pos_y1 and pos_y2 + b_size_y2 >= pos_y1:
				print("conti2")
				return 0
		return 1




		



class user():

	def __init__(self, name, password):
		self.name = name
		self.password = password
		self.position_x = 0
		self.position_y = 0
		self.angle = 0             #Angle en radian
		self.isAlive = 1	   	   #Est-ce que je joueur est en vie
		self.stepRange = 8		   #On se déplace de x px en x px ---> vitesse  
		self.chenille = 0			#Si la valeur est 0, les chenilles sont verticales, sinon elles sont horizontales
		self.tailleX = 56
		self.tailleY=56			
		self.shot = []
		self.maxMissile = 3        #nombre maximal de missile de user sur la map

	def move(self, XY):            #XY vaut 1, 2 , 3 , 4 ->avancer d'une case, droite, reculer, aller a gauche
		
		if XY == 0:
			pass
		elif XY == 1:
			self.position_y += self.stepRange
			self.chenille = 0
		elif XY == 2:
			self.position_x += self.stepRange
			self.chenille = 1
		elif XY == 3:
			self.position_y -= self.stepRange
			self.chenille = 0
		elif XY == 4:
			self.position_x -= self.stepRange
			self.chenille = 1



	def changeAngle(self,an):

		self.angle = an

	def kill(self, end):
		self.isAlive = 0
		#compteurdepoints()

		if end == False:

			
			self.position_x = 0
			self.position_y = 0
			self.isAlive = 1

		else:
			pass

		def tir(self):

			if len(self.shot) < self.maxMissile:
				self.shot.append(missile(self.position_x+28, self.position_y+28, self.angle))
			else:
				pass





class missile():

	def __init__(self,a, b, angle):

		self.a = a
		self.b = b

		self.state = 1
		self.tailleX = -16
		self.tailleY = -6

		self.stepRange = 1
		self.t = 0
		self.angle = angle
		self.x = a
		self.y = b

	def move(self):
		#accélération:
		self.x = (1/2)*self.stepRange*math.cos(self.angle)*self.t*self.t+self.a
		self.y = (1/2)*self.stepRange*math.sin(self.angle)*self.t*self.t+self.b

		#sans accélération
		#self.x = (1/2)*self.stepRange*math.cos(self.angle)*self.t+self.a
		#self.y = (1/2)*self.stepRange*math.sin(self.angle)*self.t+self.b
	
		#déccelération
		#x=(500-2*t)*cos(2)*t+4000
		#y=(500-2*t)*sin(2)*t+6250

		self.t += 1
		if self.t > 50:
			self.destroy()

	def destroy(self):
		self.state = 0




def connection(name, password):
	player.append(user(name, password))



#try:
#	initMap()
#except:
#	pass



wait = waitForConnection()
Receive = liveDataReceive()
main1 = mainMover()
main2 = mainWorker()

main2.start()

main1.start()
wait.start()
Receive.start()

while(1):
	with lock:
		if len(needToDO) > 50:
			needToDO = []
	time.sleep(0.50)
