import pygame
import math

class Node:
	def __init__(self,color,pos,N_type,value,Origin):
		self.color = color
		self.pos = pos
		self.N_type = N_type
		self.value = value
		self.is_visited = False
		self.Origin = Origin
		self.rect = pygame.Rect(self.pos,(32,32))
		self.distance_From_begin=0

	def Render(self,surf):
		pygame.draw.rect(surf,self.color,self.rect)

class Wall(Node):
	def __init__(self,pos):
		super().__init__((20, 21, 24),pos,"Wall",0,None)