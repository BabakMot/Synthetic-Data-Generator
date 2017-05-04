import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from sklearn.preprocessing import scale
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from scipy import stats
from sklearn.datasets.samples_generator import make_blobs
import pygame, random



import pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *

def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return event.key
    else:
      pass

def display_box(screen, message, pos, color):
  #"Print a message in a box in the contorl panel"
  fontobject = pygame.font.Font(None, 18)	
  pygame.draw.rect(screen, (0,0,0),
                   (pos[0]+650,
                    pos[1]+10,
                    100,20), 0)
  pygame.draw.rect(screen, color,
                   (pos[0]+648,
                    pos[1]+8,
                    100,24), 1)
  if len(message) != 0:
    screen.blit(fontobject.render(message, 1, color),
                (pos[0]+650,pos[1]+10))
  pygame.display.update()


def ask(screen, question, pos):
  #"ask(screen, question) -> answer"
  pygame.font.init()
  current_string = []
  display_box(screen, question + ": " , pos, WHITE)
  while 1:
    inkey = get_key()
    if inkey == K_BACKSPACE:
      current_string = current_string[0:-1]
    elif inkey == K_RETURN:
      break
    elif inkey == K_MINUS:
      current_string.append("_")
    elif inkey <= 127:
      if(len(current_string) < 1):
          feature = inkey
          current_string = current_string[0:-1]
          current_string.append(chr(inkey))
    display_box(screen, question + ": " + str(current_string), pos, WHITE)
  return int(feature-48)







pygame.init()
screen = pygame.display.set_mode((800,600))

# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

feature_colors = [(253,184,99),(145,191,219),(145,207,96),(241,18,130),(255,0,0),(255,255,0)]
space = pygame.Rect((0, 0), (590, 590))
control = pygame.Rect((595, 0), (200, 600))
select_feature = pygame.Rect((650,40),(97,22))
space_box = pygame.Rect((0,0),(600,600))
control_box = pygame.Rect((605,0),(195,600))
save_file = pygame.Rect((648,407),(99,22))
#--------------------
# Feature Legend:
f1 = pygame.Rect((750,180),(20,20))
f2 = pygame.Rect((750,210),(20,20))
f3 = pygame.Rect((750,240),(20,20))
f4 = pygame.Rect((750,270),(20,20))
f5 = pygame.Rect((750,300),(20,20))
f6 = pygame.Rect((750,330),(20,20))

draw_on = False
last_pos = (0, 0)
color = (255, 128, 0)
radius = 10
output = pd.DataFrame(columns=['x1','x2','y'])
current_feature = 1

def roundline(srf, color, start, end, radius=1):
    dx = end[0]-start[0]
    dy = end[1]-start[1]
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int( start[0]+float(i)/distance*dx)
        y = int( start[1]+float(i)/distance*dy)
        pygame.display.update(pygame.draw.circle(srf, color, (x, y), radius))

try:
    #screen.fill(WHITE)    #for while background
    pygame.display.update(pygame.draw.rect(screen, GREEN, space_box, 4))
    pygame.display.update(pygame.draw.rect(screen, GREEN, control_box, 4))
    pygame.display.update(pygame.draw.rect(screen, RED, select_feature, 2))
    pygame.display.update(pygame.draw.rect(screen, GREEN, save_file, 2))
  
    pygame.display.update(pygame.draw.line(screen, GREEN, [595, 0], [595,595], 10))
    pygame.display.update(pygame.draw.line(screen, WHITE, [300, 0], [300,600], 2))
    pygame.display.update(pygame.draw.line(screen, WHITE, [0, 300], [600,300], 2))
    display_box(screen, "  Control Panel", (0,0), BLUE)
    display_box(screen, "  Change Label", (0,30), RED)
    display_box(screen, "  Save and exit", (0,400), GREEN)

    #draw feature legend
    pygame.display.update(pygame.draw.rect(screen, feature_colors[0], f1, 0))
    pygame.display.update(pygame.draw.rect(screen, feature_colors[1], f2, 0))
    pygame.display.update(pygame.draw.rect(screen, feature_colors[2], f3, 0))
    pygame.display.update(pygame.draw.rect(screen, feature_colors[3], f4, 0))
    pygame.display.update(pygame.draw.rect(screen, feature_colors[4], f5, 0))
    pygame.display.update(pygame.draw.rect(screen, feature_colors[5], f6, 0))
    #pygame.Surface.fill(feature_colors[0])


    while True:

        e = pygame.event.wait()
        if e.type == pygame.QUIT:
            raise StopIteration
        if e.type == pygame.MOUSEBUTTONDOWN:
            if space.collidepoint(e.pos[0], e.pos[1]):	#if click on feature space

                color = (random.randrange(256), random.randrange(256), random.randrange(256))
                np.random.seed(int(e.pos[1]))
                X, y = make_blobs(n_samples=10, centers=1, n_features=2, cluster_std=1, center_box=[0,0], random_state=int(e.pos[1]))
                data = pd.DataFrame(columns=['x1','x2','y'])
                print (e.pos[0])
                data['x1']=((10*X[:,0]+e.pos[0])-300)/300
                data['x2']=(300-(10*X[:,1]+e.pos[1]))/300
                data['y']=current_feature
                output = output.append(data,ignore_index = True)
                print (output)

                #print (ask(screen, "feature",(0,30)))
                for i in X:
                    pygame.draw.circle(screen, feature_colors[current_feature-1], (int(e.pos[0]+10*i[0]),int(e.pos[1]+10*i[1])), 1)
            elif f1.collidepoint(e.pos[0], e.pos[1]):	#if click on feature 
                 current_feature = 1
            elif f2.collidepoint(e.pos[0], e.pos[1]):	#if click on feature 
                 current_feature = 2
            elif f3.collidepoint(e.pos[0], e.pos[1]):	#if click on feature 
                 current_feature = 3
            elif f4.collidepoint(e.pos[0], e.pos[1]):	#if click on feature 
                 current_feature = 4
            elif f5.collidepoint(e.pos[0], e.pos[1]):	#if click on feature 
                 current_feature = 5
            elif f6.collidepoint(e.pos[0], e.pos[1]):	#if click on feature 
                 current_feature = 6
            elif save_file.collidepoint(e.pos[0], e.pos[1]):	#if click on save file
                 output = output[(output['x1'] < 1) & (output['x1'] > -1) ]
                 output = output[(output['x2'] < 1) & (output['x2'] > -1) ]
                 output.to_csv("synthetic_data.csv", sep = '\t', index=False)
                 break
            elif select_feature.collidepoint(e.pos[0], e.pos[1]):	#if click on feature selection box
                current_feature = ask(screen, "Feature",(0,100))
                print (current_feature)
            #draw_on = True
        if e.type == pygame.MOUSEBUTTONUP:
            if space.collidepoint(e.pos[0], e.pos[1]):	#if click on feature space
                for i in X:
                    pygame.display.update(pygame.draw.circle(screen, feature_colors[current_feature-1], (int(e.pos[0]+10*i[0]),int(e.pos[1]+10*i[1])), 1))
           # pygame.display.update(pygame.draw.circle(screen, color, e.pos, radius))
           # draw_on = False
        if e.type == pygame.MOUSEMOTION:
            if draw_on:
                pygame.display.update(pygame.draw.circle(screen, color, e.pos, radius))
                roundline(screen, color, e.pos, last_pos,  radius)
            last_pos = e.pos

except StopIteration:
    pass

pygame.quit()

