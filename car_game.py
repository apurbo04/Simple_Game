import pygame
from pygame.locals import *
import random

pygame.init()

# Window the window size
width = 500
height = 650
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Car Game')

#color
gray = (100,100,100)
green = (76,208,56)
red = (200,0,0)
white = (255,255,255)
yellow = (255,232,0)

#game setting 
gameover =False
speed = 2
score = 0

#markers size
marker_width = 10
marker_height = 50

#road and edge markers
road = (100,0,300,height)
left_edge_marker = (95,0,marker_width,height)
right_edge_marker = (395,0,marker_width,height)

# x coordinates of Lane
left_lane = 150
center_lane = 250
right_lane = 350
lanes = [left_lane, center_lane, right_lane]

# for animating movement of the lane markers
lane_marker_move_y = 0

class Vehicle(pygame.sprite.Sprite):
   
   def __init__(self, image, x, y):
      pygame.sprite.Sprite.__init__(self)
      
      # scale the image to fit the screen
      image_scale = 45 / image.get_rect().width
      new_width = image.get_rect().width * image_scale
      new_height = image.get_rect().height * image_scale
      self.image = pygame.transform.scale(image, (new_width, new_height))
      
      self.rect = self.image.get_rect()
      self.rect.center = [x,y]
      
      
class PlayerVehicle(Vehicle):
   
   def __init__(self, image, x, y):
      image = pygame.image.load('images/Police.png')
      super().__init__(image, x, y)


# player's staring coordinates
player_x = 250
player_y = 400

# create the players car
player_group = pygame.sprite.Group()
player = PlayerVehicle(player_x, player_y)
player_group.add(player)


#game loop
clock = pygame.time.Clock()
fps = 120
running = True
while  running:
   clock.tick(fps)
   
   for event in pygame.event.get():
      if event.type == QUIT:
         running = False
      
   #draw the grass
   screen.fill(green)
   
   #draw the road
   pygame.draw.rect(screen,gray,road)
   
   # draw the edge markers
   pygame.draw.rect(screen,yellow,left_edge_marker)
   pygame.draw.rect(screen,yellow,right_edge_marker)
   
   # draw the lane markers
   lane_marker_move_y +=speed*2
   if lane_marker_move_y >= marker_height*2 :
      lane_marker_move_y = 0
      
   for y in range(marker_height* -2,height,marker_height*2):
      pygame.draw.rect(screen,white,(left_lane+45,y+ lane_marker_move_y ,marker_width,marker_height))
      pygame.draw.rect(screen,white,(center_lane+45,y+ lane_marker_move_y ,marker_width,marker_height))
   
   # draw the player,s car
   player_group.draw(screen)
   
   
   pygame.display.update()