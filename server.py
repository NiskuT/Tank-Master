#!/usr/bin/env python
# coding: utf-8
import math
import socket
from threading import Thread, RLock
import threading
from random import randrange, randint
import time

nbPlayer = 0
nbMaxPlayer = 4
lock = RLock()
mainLock = RLock()
workLocker = RLock()
dataToSend = ""
player = []
needToDO =[]
allIP =[]




socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketTCP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socketTCP.bind(("", 1234))

socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socketUDP.bind(('', 12000))



#def collision(XA,YA, a, ID, xb, yb, ab, idb):

#def check():
#	collision joueur joueur
#	collision joueur map
#	collision joueur missile
#	collision missile map
#	collision missile missile




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
				password = randint(0, 9999)
				nom, ip = self.client.recvfrom(2048)
				allIP.append(ip)
				self.client.send((password+len(player).encode('utf-8')))
				connection(nom.decode('utf-8'), password)
				self.client.close()




class liveDataReceive(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)	

	def run(self):
		while True:
			data = (socketUDP.recv(1024)).decode('utf-8')
			if len(data) != 11:
				continue
			with lock:
				needToDO.append(data)
				#{9}{9999}{3.14}{4}{1}

class liveDataSender(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)


	def run(self):
		while True:
			with lock:
				self.data = dataToSend.encode('utf-8')
			for k in allIP:
				socketUDP.sendto(seld.data, k)


class mainMover(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)


	def run(self):
		while(1):
			action = "90000000000"
			with mainLock:
				try:
					action = needToDO[-1]
					del needToDO[-1]
				except:
					pass
				id = int(action[0])
				if id != 9:
					if player[id].password == (action[1]+action[2]+action[3]+action[4]):
						player[id].changeAngle(float(action[5]+action[6]+action[7]+action[8]))
						player[id].move(int(action[9]))
						if (player[id].maxMissile > len(player[id].shot)) and action[10] == "1":
							player[id].shot.append(missile(player[id].position_x,player[id].position_y, player[id].angle))


class mainWorker(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)

	def run:
		while(1):
			positions = []
			
			####missiles#####
			for k in player:
				for x in k.shot:
					with workLocker:
						x.move()

			####colisions######






		



class user():

	def __init__(self, name, password):
		self.name = name
		self.password = password
		self.position_x = 0
		self.position_y = 0
		self.angle = 0             #Angle en radian
		self.isAlive = True		   #Est-ce que je joueur est en vie
		self.stepRange = 8		   #On se déplace de x px en x px ---> vitesse  

		self.shot = []
		self.maxMissile = 3        #nombre maximal de missile de user sur la map

	def move(self, XY):            #XY vaut 1, 2 , 3 , 4 ->avancer d'une case, droite, reculer, aller a gauche
		
		vecteurX0_x = (math.cos(self.angle-math.pi/2)) * self.stepRange
		vecteurX0_y = (math.sin(self.angle-math.pi/2)) * self.stepRange
		vecteurY0_x = (math.cos(self.angle)) * self.stepRange
		vecteurY0_y = (math.sin(self.angle)) * self.stepRange

		X = 0
		Y = 0
		if XY == 0:
			pass
		elif XY == 1:
			X=0
			Y=1
		elif XY == 2:
			X=1
			Y=0
		elif XY == 3:
			X=0
			Y=-1
		elif XY == 4:
			X=-1
			Y=0

		if X*Y != 0:
			raise moveError("Les coordonnées de déplacement sont incorrect.")
			#on ne peut pas se déplacer sur deux axes en même temps, donc le produit des deux doit valoir 0
		else:
			
			vecteurX0_x = vecteurX0_x * X
			vecteurX0_y = vecteurX0_y * X
			vecteurY0_x = vecteurY0_x * Y
			vecteurY0_y = vecteurY0_y * Y

			self.position_x = round(self.position_x + vecteurX0_x + vecteurY0_x)
			self.position_y = round(self.position_y + vecteurX0_y + vecteurY0_y)

	def changeAngle(self,an):

		self.angle = an

	def kill(self, end):
		self.isAlive = False
		#compteurdepoints()

		if end == False:

			Nspawn = randrange(0,len(spawn))
			self.position_x = spawn[Nspawn][0]
			self.position_y = spawn[Nspawn][1]
			self.isAlive = True

		else:
			pass

		def tir(self):

			if len(self.shot) < self.maxMissile:
				self.shot.append(missile(self.position_x, self.position_y, self.angle))
			else:
				pass





class missile():

	def __init__(self,a, b, angle):

		self.a = a
		self.b = b

		self.stepRange = 15
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
		if t > 50:
			self.destroy()

	def destroy(self):
		pass




def connection(password, name):
	player.append(user(name, password))




		
joueur1 = user("quentin", 4597)



wait = waitForConnection()
Sender = liveDataSender()
Receive = liveDataReceive()
main1 = mainMover()

main1.start()
wait.start()
Sender.start()
Receive.start()

#joueur1.kill(False)
while 1:
	a = int(input("nb:"))
	joueur1.angle = float(input("angle:"))
	joueur1.move(a)
	print(joueur1.position_x, joueur1.position_y)


