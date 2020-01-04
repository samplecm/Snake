import pygame
import math
import random
from random import randint
import tkinter as tk
from tkinter import messagebox


class Cube(object):
	rows = 20
	w = 500
	def __init__(self,start,xDir=1,yDir=0,colour=(255,0,0)):
		self.pos = start
		self.xDir = 1
		self.yDir = 0
		self.colour = colour
		
		
	def move(self,xDir,yDir):
		self.xDir = xDir
		self.yDir = yDir
		self.pos = (self.pos[0]+self.xDir,self.pos[1]+self.yDir)
		   
		
		
	def draw(self,surface,eyes=False):
		#need distance between x and y values
		dis = self.w // self.rows
		i = self.pos[0]
		j = self.pos[1]
		
		pygame.draw.rect(surface,self.colour,(i*dis+1,j*dis+1,dis-2,dis-2))
		
		if eyes:
			centre = dis//2
			radius=4
			circleMiddle = (i*dis+centre-radius,j*dis+8)
			circleMiddle2 = (i*dis + dis-radius*2,j*dis+8)
			pygame.draw.circle(surface,(0,0,0),circleMiddle,radius)
			pygame.draw.circle(surface,(0,0,0),circleMiddle2,radius)
			
		
	

class Snake(object):
	body = []
	turns = {}
	def __init__(self,colour,pos):
		self.colour = colour
		self.head = Cube(pos)
		self.body.append(self.head)
		self.xDir = 0
		self.yDir = 1
		
	def move(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			keys = pygame.key.get_pressed()
			for key in keys:
				if keys[pygame.K_LEFT]:
					self.xDir = -1
					self.yDir = 0
					self.turns[self.head.pos[:]]=[self.xDir,self.yDir] #new turn at this positions
				elif keys[pygame.K_RIGHT]:
					self.xDir = 1
					self.yDir = 0
					self.turns[self.head.pos[:]]=[self.xDir,self.yDir]
				elif keys[pygame.K_UP]:
					self.xDir = 0
					self.yDir = -1
					self.turns[self.head.pos[:]]=[self.xDir,self.yDir]
				elif keys[pygame.K_DOWN]:
					self.xDir = 0
					self.yDir = 1
					self.turns[self.head.pos[:]]=[self.xDir,self.yDir]
		 			
		for i,c in enumerate(self.body):#look through list of positions (index and cube)
			p = c.pos[:] #copy so position doesn't get changed
			if p in self.turns:
				turn = self.turns[p]
				c.move(turn[0],turn[1])
				if i == len(self.body)-1: #if on last cube, remove turn
					self.turns.pop(p)
			else: #of at edges of screen, loop back to other side.
				if c.xDir == -1 and c.pos[0] <=0: c.pos = (c.rows-1,c.pos[1])
				elif c.xDir ==1 and c.pos[0] >= rows-1: c.pos = (0,c.pos[1])
				elif c.yDir == 1 and c.pos[1]>=rows-1: c.pos = (c.pos[0],0)
				elif c.yDir == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
				else: c.move(c.xDir,c.yDir)
				
				 
			
	def reset(self,pos):
		self.head = Cube(pos)
		self.body = []
		self.body.append(self.head)
		self.turns = {}
		self.xDir = 1
		self.yDir = 0
		
	def addCube(self):
		tail = self.body[-1]
		dx,dy = tail.xDir,tail.yDir
		#check direction of movement, to know where to add cube.
		if dx == 1 and dy == 0:
			self.body.append(Cube((tail.pos[0]-1,tail.pos[1])))
		elif dx ==-1 and dy == 0:
			self.body.append(Cube((tail.pos[0]+1,tail.pos[1])))
		elif dx == 0 and dy ==1:
			self.body.append(Cube((tail.pos[0],tail.pos[1]-1)))
		elif dx ==0 and dy == -1:
			self.body.append(Cube((tail.pos[0],tail.pos[1]+1)))
		
		self.body[-1].xDir = dx
		self.body[-1].yDir = dy
		
		
	def draw(self,surface):
		for i,c in enumerate(self.body):
			if i == 0:
				c.draw(surface,True)
			else:
				c.draw(surface)
		
		
		
	
	
	

def drawGrid(w, rows, surface):
	#need to know where to draw lines.
	sizeBtwn = w // rows
	
	x = 0
	y = 0
	for l in range(rows):
		x = x + sizeBtwn
		y = y + sizeBtwn
		
		pygame.draw.line(surface,(255,255,255),(x,0),(x,w))
		pygame.draw.line(surface,(255,255,255),(0,y),(w,y))
		
def redrawWindow(surface):
	global rows, width, snake
	surface.fill((0,0,0))
	snake.draw(surface)
	snack.draw(surface)
	
	drawGrid(width,rows,surface)
	pygame.display.update()
	
def randomSnack(rows,item):
	
	positions = item.body
	
	while True:
		x = random.randrange(rows)
		y = random.randrange(rows)
		if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
			#filtered list to see if any positions are same as position of snake
			continue
		else:
			break
	return (x,y)

def message_box(subject,content):
	root = tk.Tk()
	root.attributes("-topmost",True)
	root.withdraw()
	messagebox.showinfo(subject,content)
	try:
		root.destroy()
	except:
		pass
	
	
	

def main():
	
	global width,rows,snake,snack
	width = 500
	rows = 20
	pygame.init()
	window = pygame.display.set_mode((width,width))
	
	
	snake = Snake((250,255,0),(10,10))#initial position
	snack = Cube(randomSnack(rows,snake),colour = (0,0,255))
	flag = True
	
	clock = pygame.time.Clock()
	
	while flag:
		pygame.time.delay(25)
		clock.tick(15)#make sure no mare than 10fps	
		snake.move()
		if snake.body[0].pos == snack.pos:
			snake.addCube()
			colour1 = randint(0,100)
			colour2 = randint(0,255)
			colour3 = randint(0,255)
			
			snack = Cube(randomSnack(rows,snake),colour = (colour1,colour2,colour3))
		
		for x in range(len(snake.body)):
			if snake.body[x].pos in list(map(lambda z:z.pos,snake.body[x+1:])):
				print('Score: ' , len(snake.body))
				message_box('You Lost','Play Again')
				snake.reset((10,10))
				break
		redrawWindow(window)
		
		pass
if __name__ == '__main__':
	main()








































#pygame.init() #initialize pygame.
#
#window= pygame.display.set_mode((500,500)) #setting up the window
#
#pygame.display.set_caption("Snake")
#
##make a character.
#x = 50
#y = 50
#width = 40
#height = 60
#vel = 5
#
##always want a main loop.
#run = True
#while run:
#	pygame.time.delay(100) #ms, the load time of game
#	
#	for event in pygame.event.get():
#		if event.type == pygame.QUIT:
#			run = False
#			
#	keys = pygame.key.get_pressed()
#		
#	if keys[pygame.K_LEFT]	:
#		x -= vel
#
#	if keys[pygame.K_RIGHT]:
#		x+= vel	
#	if keys[pygame.K_UP]:
#		y-=vel
#	if keys[pygame.K_DOWN]:	
#		y+=vel	
#		
#	window.fill((0,0,0))	
#			
#			
#	pygame.draw.rect(window,(255,0,0),(x,y,width,height))
#	pygame.display.update()		
#pygame.quit()	
#
