import pygame
import random
from random import randint
import time


#################################################################################
class Cube(object):
	rows = 32
	w = 800
	def __init__(self,start,xDir=1,yDir=0,colour=(255,255,0)):
		self.pos = start
		self.xDir = xDir
		self.yDir = yDir
		self.colour = colour
		
		
	def move(self,xDir,yDir):
		self.xDir = xDir
		self.yDir = yDir
		self.pos = (self.pos[0]+self.xDir,self.pos[1]+self.yDir)
		   
		
		
	def draw(self,surface,head=False):
		#need distance between x and y values
		dis = self.w // self.rows
		i = self.pos[0]
		j = self.pos[1]
		
		pygame.draw.rect(surface,self.colour,(i*dis+1,j*dis+1,dis-2,dis-2))
		
		if head:
			mJFace = pygame.image.load(r'C:\Users\sampl\Documents\Python\Snake\Photos/MJ_Face.jpg')
			mJFace = pygame.transform.scale(mJFace, (int(800/32),int(800/32)))
			window.blit(mJFace,(i*dis+1,j*dis+1,dis-2,dis-2))
#			centre = dis//2
#			radius=4
#			circleMiddle = (i*dis+centre-radius,j*dis+8)
#			circleMiddle2 = (i*dis + dis-radius*2,j*dis+8)
#			pygame.draw.circle(surface,(0,0,0),circleMiddle,radius)
#			pygame.draw.circle(surface,(0,0,0),circleMiddle2,radius)
###########################################################################			
		
	

class Snake(object):
	body = []
	turns = {}
	def __init__(self,colour,pos):
		self.colour = colour
		self.head = Cube(pos,1,0,(255,0,0))
		self.body.append(self.head)
		self.xDir = 0
		self.yDir = randint(0,1)
		
	def move(self):
		global gameOver
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			keys = pygame.key.get_pressed()
			for key in keys:
				if keys[pygame.K_LEFT]:
					if not self.xDir == 1 and not self.yDir == 0:
						self.xDir = -1
						self.yDir = 0
						self.turns[self.head.pos[:]]=[self.xDir,self.yDir] #new turn at this positions
				elif keys[pygame.K_RIGHT]:
					if not self.xDir == -1 and not self.yDir == 0:
						self.xDir = 1
						self.yDir = 0
						self.turns[self.head.pos[:]]=[self.xDir,self.yDir]
				elif keys[pygame.K_UP]:
					if not self.xDir == 0 and not self.yDir == 1:
						self.xDir = 0
						self.yDir = -1
					self.turns[self.head.pos[:]]=[self.xDir,self.yDir]
				elif keys[pygame.K_DOWN]:
					if not self.xDir == 0 and not self.yDir == -1:
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
				if c.pos[0] < 0: #c.pos = (c.rows-1,c.pos[1])
					gameOver = True
					pygame.mixer.music.load('Sounds/BadIntro.WAV')
					pygame.mixer.music.play(1)
					time.sleep(1.63)
					break
				elif c.pos[0] >= rows: #c.pos = (0,c.pos[1])
					gameOver = True
					pygame.mixer.music.load('Sounds/BadIntro.WAV')
					pygame.mixer.music.play(1)
					time.sleep(1.63)
					break
				elif c.pos[1]>=rows: #c.pos = (c.pos[0],0)
					gameOver = True
					pygame.mixer.music.load('Sounds/BadIntro.WAV')
					pygame.mixer.music.play(1)
					time.sleep(1.63)
					break
				elif c.pos[1] < 0: 
					gameOver = True #c.pos = (c.pos[0],c.rows-1)
					pygame.mixer.music.load('Sounds/BadIntro.WAV')
					pygame.mixer.music.play(1)
					time.sleep(1.63)
					break
				else: c.move(c.xDir,c.yDir)
				
				 
			
	def reset(self,pos):
		self.head = Cube(pos,1,0,(255,0,0))
		self.body = []
		self.body.append(self.head)
		self.turns = {}
		self.xDir = 1
		self.yDir = 0
		
	def addCube(self,colour):
		
		tail = self.body[-1]
		dx,dy = tail.xDir,tail.yDir
		#check direction of movement, to know where to add cube.
		if dx == 1 and dy == 0:
			self.body.append(Cube((tail.pos[0]-1,tail.pos[1]),dx,dy,colour))
		elif dx ==-1 and dy == 0:
			self.body.append(Cube((tail.pos[0]+1,tail.pos[1]),dx,dy,colour))
		elif dx == 0 and dy ==1:
			self.body.append(Cube((tail.pos[0],tail.pos[1]-1),dx,dy,colour))
		elif dx ==0 and dy == -1:
			self.body.append(Cube((tail.pos[0],tail.pos[1]+1),dx,dy,colour))
		
		self.body[-1].xDir = dx
		self.body[-1].yDir = dy
		
		
	def draw(self,surface):
		for i,c in enumerate(self.body):
			if i == 0:
				c.draw(surface,True)
			else:
				c.draw(surface)
		
###############################################################################		
		
	
	
	

#def drawGrid(w, rows, surface):
#	#need to know where to draw lines.
#	sizeBtwn = w // rows
#	
#	x = 0
#	y = 0
#	for l in range(rows):
#		x = x + sizeBtwn
#		y = y + sizeBtwn
#		
#		pygame.draw.line(surface,(255,255,255),(x,0),(x,w))
#		pygame.draw.line(surface,(255,255,255),(0,y),(w,y))
#		
def redrawWindow(surface):
	global rows, width, snake
	surface.fill((0,0,0))
	snake.draw(surface)
	snack.draw(surface)
	score = len(snake.body)-1
	scoreStatement = 'Score: ' + str(score)
	drawText(window,scoreStatement, 25,width/(rows-15),width/(rows-10),(255,255,255))
	
	#drawGrid(width,rows,surface)
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

def highScoreFetch():
	highScore = 0 #default
	
	try:
		highScoreFile = open('highScore.txt','r')
		highScore  = int(highScoreFile.read())
		highScoreFile.close()
	except:
		print('IO error')	
	if score > highScore:
		highScore = score
		highScoreFile = open('highScore.txt','w')
		highScoreFile.write(str(highScore))
		highScoreFile.close()
		
	
	return highScore
	
		

def GO_Screen():#Game Over Screen/ Start up Screen
	
	WHITE = (255,255,255)
	
	
	highScore = highScoreFetch()
	scoreStatement = 'Score: ' + str(score)
	highScoreStatement = 'High Score: ' + str(highScore)
	
	window.fill((50,180,255))
	mJFace = pygame.image.load(r'C:\Users\sampl\Documents\Python\Snake\Photos/MJ_Outline.jpg')
	mJFace = pygame.transform.scale(mJFace, (int(800*0.55),int(800*0.55)))
	window.blit(mJFace,(800*0.23,800*0.4))	
	drawText(window,"MJ SNAKE",120 ,width / 2, width / 6.5,(175,20,20))
	drawText(window,"Use the arrow keys to move",35,width/2,width/3,WHITE)
	drawText(window,scoreStatement, 25,width/9.5,width/30,WHITE)
	drawText(window,"Press any key to begin a new game",40,width/2,width/3.5,(250,250,250))
	drawText(window,highScoreStatement, 25,width/13,width/125,WHITE)

	
	
	pygame.display.flip()
	
	waiting = True
	snake.reset((10,10))
	pygame.init()
	pygame.mixer.music.load('Sounds/BadMain.WAV')
	pygame.mixer.music.play(-1)
	
	while waiting:
		
		
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				waiting = False
				pygame.mixer.quit()
				pygame.init()
				pygame.mixer.music.load('Sounds/BadIntro.WAV')#load it back up for next time.
				
				break
def mJNoise():
	
	sound = 'Sounds/' + str(randint(1,48)) + '.WAV'
	print(sound)
	pygame.mixer.music.load(sound)
	pygame.mixer.music.load(sound)
	pygame.mixer.music.play(1)
			

def drawText(surface,text,size,x,y,colour):
	
	font  = pygame.font.Font(myFont,size)
	text_surface = font.render(text,True,colour) #anti-alias or not
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x,y)	
	window.blit(text_surface,text_rect)		
 				
	

def main():
	
	global width,rows,snake,snack,clock,myFont,window,score,gameOver, highScore
	width = 800
	rows = 32
	
	pygame.init()
	colList1 = [255,255,0,0,255,0,255,154,255,250,173,102,0]
	colList2 = [255,0,255,0,255,255,0,205,140,128,255,205,191]
	colList3 = [255,0,0,255,0,255,255,50,0,114,147,170,255]
	
	
	
	window = pygame.display.set_mode((width,width))
	pygame.mixer.music.load('Sounds/BadIntro.WAV')
				
	
	snake = Snake((200,255,0),(10,10))#initial position
	snack = Cube(randomSnack(rows,snake),colour = (0,0,255))
	on = True
	gameOver= True
	myFont = pygame.font.match_font('8-Bit-Madness')
	clock = pygame.time.Clock()
	
	while on:
		
		

		
		pygame.time.delay(10)
		clock.tick(15)#make sure no mare than 10fps	
		snake.move()
		if gameOver:
			score = len(snake.body)-1
			gameOver = False
			snake.reset((10,10))
			
			GO_Screen()
			
		
		if snake.body[0].pos == snack.pos:
			if len(snake.body)==1:
				colour1 = 0
				colour2 = 0
				colour3 = 255
			
			mJNoise()
			snake.addCube((colour1,colour2,colour3))
			
			colour1 = colList1[randint(0,12)]
			colour2 = colList2[randint(0,12)]
			colour3 = colList3[randint(0,12)]
			
			
				
			
					
			snack = Cube(randomSnack(rows,snake),colour = (colour1,colour2,colour3))
		
		for x in range(len(snake.body)):
			if snake.body[x].pos in list(map(lambda z:z.pos,snake.body[x+1:])):
				score = len(snake.body)-1
				print('Score: ' , score)
				gameOver = True
				pygame.mixer.music.load('Sounds/BadIntro.WAV')
				pygame.mixer.music.play(1)
				time.sleep(1.63)
				
				
				
				break
		
		redrawWindow(window)
		
		pass
if __name__ == '__main__':
	main()
