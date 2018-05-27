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
allIP =["localhost"]
b_size_missile_x = -16
b_size_missile_y = -6
E = []


socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketTCP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socketTCP.bind(("", 7089))

socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socketUDP.bind(("localhost", 33108))


def initMap():
#Création de la map
	filin = open('MAP2_2.txt','r')
	for i in range(675):
		sl=[]
		c = filin.readline()
		#print(c)
		for j in range(len(c)):
			if (c[j] != ' ') and (c[j]!='\n'):
				sl.append(int(c[j]))
		E.append(sl)
	filin.close()

class waitForConnection(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		while True:
			socketTCP.listen(15)
			print("Waiting for connection")
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
			#time.sleep(.001)
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
					positions.append([player[k].isAlive,player[k].tailleX, player[k].tailleY, int(player[k].position_x), int(player[k].position_y) , round(player[k].angle,2) , player[k].chenille, k])
				except IndexError:
					positions.append([0,0,0,0,0,0,0,0])

				for x in range(3):
					try:
						with workLocker:
							player[k].shot[x].move()
						positions.append([player[k].shot[x].state, player[k].shot[x].tailleX, player[k].shot[x].tailleY, int(player[k].shot[x].x) , int(player[k].shot[x].y), round(player[k].shot[x].angle,2) , k, x])
					except IndexError:
						positions.append([0,0,0,0,0,0,0,0])


			####colisions######
			for t in range(len(positions)):
				if positions[t][0]== 1 :
					if t == 4 or t==0:
						if ((self.collision_mur(positions[t][3], positions[t][4], 56, 56)) == 1):
							player[positions[t][7]].kill(False)
					
					else:
						player[positions[t][6]].shot[positions[t][7]].tailleX, player[positions[t][6]].shot[positions[t][7]].tailleY = self.hitbox_missile(positions[t][5])
						if self.collision_mur(positions[t][3], positions[t][4], positions[t][1], positions[t][2]) == 1:
							player[positions[t][6]].shot[positions[t][7]].destroy()

			for u in range(len(positions)):
				for v in range(len(positions)):
					if positions[u][0]== 1 and positions[v][0]== 1 and u != v:
						if self.collision(positions[u][3], positions[u][4], positions[u][1], positions[u][2], positions[v][3], positions[v][4], positions[v][1], positions[v][2]) == 0:
							if u == 0 or u == 4:
								player[positions[u][7]].kill(False)
							else:
								player[positions[u][6]].shot[positions[u][7]].destroy()

							if v == 0 or v == 4:
								player[positions[v][7]].kill(False)
							else:
								player[positions[v][6]].shot[positions[v][7]].destroy()



			####envoie####

			self.sender(positions)

			time.sleep(.040)
			#mettre seulement le Thread en pause <><><>




	def sender(self, serverData):

		data = pickle.dumps(serverData)
		for k in allIP:
			try:
				socketUDP.sendto(data, (str(k), 12000))
				socketUDP.sendto(data, (str(k), 13000))
			except socket.gaierror:
				print("Not found!")

	def collision_mur(self, x1, y1, s1, s2):
	
		boom = 0
		try:
			for i in range (s1):
				if E[y1][i+x1]==1:
					boom=1
				else:
					if E[y1+s1][i+x1]==1:
						boom=1

			if boom != 0:
				for i in range (s2):
					if E[i+y1][x1]==1:
						boom=1
					else:
						if E[i+y1][x1+s2]==1:
							boom=1
		#if boom==1:
		#	print(boom,"x1= ",x1," et y1= ",y1)
		except IndexError:
			boom = 1

		return boom

	def hitbox_missile(self, angle):
		self.b_size_missile_x = 16
		self.b_size_missile_y = 6
		self.b_size_x = math.ceil(self.b_size_missile_x * math.cos(angle))
		self.b_size_y = math.ceil(self.b_size_missile_y * math.sin(angle))
		return self.b_size_x, self.b_size_y

	def collision(self,     pos_x1, pos_y1,  b_size_x, b_size_y,       pos_x2, pos_y2,  b_size_x2, b_size_y2):

		if pos_x1 <= pos_x2 and pos_x1 + b_size_x >= pos_x2:
			if pos_y1 <= pos_y2 and pos_y1 + b_size_y >= pos_y2:
				return 0
		elif pos_x2 <= pos_x1 and pos_x2 + b_size_x2 >= pos_x1:
			if pos_y2 <= pos_y1 and pos_y2 + b_size_y2 >= pos_y1:
				return 0
		return 1




class user():

	def __init__(self, name, password):
		self.name = name
		self.password = password
		self.position_x = 0
		self.position_y = 0
		try:
			if player[0].isAlive == 1:
				self.position_x = 1120
				self.position_y = 550
		except IndexError:
			self.position_x = 25
			self.position_y = 25


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
			self.chenille = 1
		elif XY == 2:
			self.position_x += self.stepRange
			self.chenille = 0
		elif XY == 3:
			self.position_y -= self.stepRange
			self.chenille = 1
		elif XY == 4:
			self.position_x -= self.stepRange
			self.chenille = 0

		try:
			if len(self.shot) == 3 and self.shot[2].t > 50 :
				self.shot = []
		except:
			pass



	def changeAngle(self,an):

		self.angle = an

	def kill(self, end):
		self.isAlive = 0
		#compteurdepoints()

		if end == False:

			
			self.position_x = 40
			self.position_y = 40
			self.isAlive = 1

		else:
			pass

	def tir(self):

		if len(self.shot) < self.maxMissile:
			self.shot.append(missile((self.position_x+28), (self.position_y+28), self.angle))
		else:
			pass





class missile():

	def __init__(self,a, b, angle):

		self.a = a
		self.b = b

		self.state = 0
		self.tailleX = -16
		self.tailleY = -6

		self.stepRange = 15
		self.t = 0
		self.angle = angle
		self.x = a
		self.y = b

	def move(self):
		#accélération:
		#self.x = int((1/2)*self.stepRange*math.cos(self.angle)*self.t*self.t+self.a)
		#self.y = int((1/2)*self.stepRange*math.sin(self.angle)*self.t*self.t+self.b)

		#sans accélération
		self.x = 0.35*self.stepRange*math.cos(self.angle)*self.t+self.a
		self.y = 0.35*self.stepRange*math.sin(self.angle)*self.t+self.b
	
		#déccelération
		#x=(500-2*t)*cos(2)*t+4000
		#y=(500-2*t)*sin(2)*t+6250

		self.t += 1
		if self.t > 20:
			self.state = 1
		if self.t > 500:
			self.destroy()

	def destroy(self):
		self.state = 0




def connection(name, password):
	player.append(user(name, password))



try:
	initMap()
except:
	pass



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
