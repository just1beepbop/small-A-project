#rgb#rgb(41, 173, 255):Blue
#rgb(0, 228, 54) : Green
#rgb(20, 21, 24): Black
#rgb(229, 34, 16): Red
import pygame
import sys
from Node import *

Red = (229, 34, 16)
Blue = (41, 173, 255)
Green = (0, 228, 54)
Black = (20, 21, 24)

class Game():
	def __init__(self):
		pygame.mixer.init()
		pygame.init()
		self.screen = pygame.display.set_mode((832, 672))
		self.clock = pygame.time.Clock()
		self.running = True
		self.Block = {}
		self.Begin = Node(Green,(32,32),"Begin",0,None)
		self.End = Node(Red,(736,576),"End",0,None)
		self.Block[str(self.Begin.pos)] = self.Begin
		self.Block[str(self.End.pos)] = self.End
		self.shifting = False
		self.Visited = [self.Begin]
		self.Nodes = [self.Begin]
		self.neighbors = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
		self.going = False
		self.time = 0
		self.end = False

	def Run(self):
		while self.running:
			self.screen.fill((255,255,255))
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
				if event.type == pygame.MOUSEBUTTONDOWN:
					pos = pygame.mouse.get_pos()
					pos = (pos[0]//32*32,pos[1]//32*32)
					if self.shifting:
						try:
							self.Block.pop(str(pos))
						except:
							pass
					elif str(pos) not in self.Block.keys():
						self.Block[str(pos)] = Wall(pos)
					

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
						self.shifting = True	
					if event.key == pygame.K_b:
						self.going = True

				if event.type == pygame.KEYUP:
					if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
						self.shifting = False
			if self.end:
				self.ending(self.End)

			elif self.going:
				self.time += 1
				self.Algorithm(min(self.Nodes, key=lambda x: x.value))

			for i in self.Block.values():
				i.Render(self.screen)

			pygame.display.flip()
			self.clock.tick(60)

		pygame.mixer.quit()
		pygame.quit()
		sys.exit()

	#A* algorithm	
	def Algorithm(self,node):
		node.color = Red
		Nodes = []
		for x,y in self.neighbors:
			pos = (int(node.pos[0] + x*32), int(node.pos[1] +y*32))
			po = pygame.math.Vector2(pos)
			H = po.distance_to(node.pos)
			G = po.distance_to(self.End.pos)
			value = H+ G+ node.distance_From_begin 

			if str(pos) in self.Block.keys():
				if self.Block[str(pos)].N_type == "Wall" or self.Block[str(pos)] in self.Visited:
					continue
				elif self.Block[str(pos)].value > value:
					self.Block[str(pos)].value = value
					self.Block[str(pos)].Origin = node
					self.Block[str(pos)].distance_From_begin = node.distance_From_begin + H
				elif self.Block[str(pos)].N_type == "End":
					self.end = True
					self.End.Origin = node
			else:
				new_node = Node(Green,pos,"Node",value,node)
				new_node.distance_From_begin = node.distance_From_begin + H
				self.Block[str(pos)] = new_node
				Nodes.append(new_node)

		self.Visited.append(node)
		self.Nodes.remove(node)
		self.Nodes += Nodes

	def ending(self,node):
		if node.N_type == "Begin":
			node.color = Blue
		else:
			node.color = Blue
			self.ending(node.Origin)

if __name__ == '__main__':
	game = Game()
	game.Run()