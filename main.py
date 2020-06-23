#pygame template 

import pygame
import math
import random


pygame.init()



#Constants 

FS = False
SIZE_X = 700
SIZE_Y = 700
FPS = 60
clock = pygame.time.Clock()


#Colors 

WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0) 
BLACK = pygame.Color(0,0,0)
BLUE = pygame.Color(86,145,204)
DRED = pygame.Color(91,57,57)

#fonts

font_size = 12
font = pygame.font.SysFont('arial', font_size)

if FS:
    pygame.display.init()
    info = pygame.display.Info()
    SIZE_X = info.current_w
    SIZE_Y = info.current_h
    screen = pygame.display.set_mode((0, 0),pygame.FULLSCREEN)
else:
    #This producers a smaller window, which is for trying new code. 

    
    screen = pygame.display.set_mode((SIZE_X, SIZE_Y))
    
grid_list = []
gridw,gridh = 100,100
isle_list = []

class _Isle(object):
    def __init__(self,x,y,id):
        self.x = x 
        self.y = y
        self.id = id 
        self.page = self.id // 16
        self.true_x = x + (self.id//page) + self.id
        self.true_y = y + (self.id//page) + self.id
        self.clicked = "TESTING"
        self.rect = None
         
        

class _Grid(object):
    def __init__(self,id,row,col):
        self.id = id
        self.row = row
        self.col = col
        self.w = gridw
        self.h = gridh
        
        for x in range(5,gridw,25):
            for y in range(5,gridh,25):
                dice = random.randint(0,100)
                if dice > 90:
                    isle_list.append(_Isle(x,y,self.id))
        
                   
        
class Move_Btn(object):
    def __init__(self,x,y,w,h,dir):
        self.x = x
        self.y = y
        self.w = w
        self.h = h 
        self.dir = dir
        self.rect = pygame.Rect(self.x,self.y,self.w,self.h)
        self.color = BLUE
        
    def draw(self):
        pygame.draw.rect(screen,self.color,(self.rect))
        # self.surface = font.render(str(),
                                # False, 
                                # BLACK)
                                
        # screen.blit(self.surface,(self.x,self.y))
        
        
class Camera(object):
    def __init__(self,page=24, max=16):
        self.page = 0
        self.max = max
        self.dimX,self.dimY = get_grid_dims()
        self.btnW = 25
        self.btnH = 25
        self.color = WHITE
        
        
    def move(x):
        if self.page+x < 1:
            return False
        if self.page+x > self.max:
            return False
        self.page += x
        return True
        
    def display_page(self):
        count = 0
        tmp = []
        for isle in isle_list:
            
            isle.rect = None
        for i in range(0,self.max):
            tmp.append(grid_list[self.page* self.max+i])
            
        
        for i in range(0,4):
            for n in range(0,4):
                x = (self.dimX //2 )+ (gridw*n)
                y = (self.dimY //2 )+ (gridh*i)
                
                pygame.draw.rect(screen,
                                self.color,
                                (x,y,100-1,100-1))
                for isle in isle_list:
                    if isle.id == tmp[count].id:
                        
                        isle.rect = pygame.draw.rect(screen,BLACK,(x+isle.x,y+isle.y,5,5))
                        
                    
                
                self.surface = font.render(str(tmp[count].id),
                                False, 
                                BLACK)
                                
                screen.blit(self.surface,(x,y))    
                #print(x,y)
                #print(count)
                count +=1
        self.surface = font.render(str(self.page),
                                False, 
                                WHITE)
                                
        screen.blit(self.surface,(0,0))
        
        self.draw_buttons()
    
    def draw_buttons(self):
        #global My_Btns
        buttons = self.find_limits()
        for dir in buttons:
            #right side
            if dir == 1:
                x = SIZE_X - self.dimX//3
                y = SIZE_Y //2 - (self.btnH//2)
                My_Btns.append(Move_Btn(x,y,self.btnW,self.btnH,1))
                
            #down
            if dir == 2:
                x = SIZE_X // 2 - (self.btnW //2)
                y = SIZE_Y - self.dimX//3
                My_Btns.append(Move_Btn(x,y,self.btnW,self.btnH,4))
            #up 
            if dir == 3:
                x = SIZE_X // 2 - (self.btnW //2)
                y = (0 + self.dimY//3) - self.btnH
                My_Btns.append(Move_Btn(x,y,self.btnW,self.btnH,-4))    
            #left 
            if dir == 4:
                x = (0 + self.dimX//3) - self.btnW
                y = SIZE_Y //2 - (self.btnH//2)
                My_Btns.append(Move_Btn(x,y,self.btnW,self.btnH,-1))
                                
                               
    def find_limits(self):
        boarder = []
        
        if self.page + 1 < page:
            boarder.append(1)
        if self.page + 4 < page:
            boarder.append(2)
        if self.page - 4 >= 0:
            boarder.append(3)
        if self.page - 1 >= 0:
            boarder.append(4)
        return boarder
    
        
        
    
def get_grid_dims():
    box = gridw * 4
    paddingX = SIZE_X - (box)
    paddingY = SIZE_Y - (box)
    return paddingX,paddingY
    
        
            
def draw_window():
    global My_Btns
    pos = pygame.mouse.get_pos()
    My_Btns = []
    screen.fill(BLACK)
    cam.display_page()
    for btn in My_Btns:
        btn.draw()
    
    
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            #check if btn was clicked. 
            for btn in My_Btns:
                if btn.rect.collidepoint(pos):
                    cam.page += btn.dir
            for isle in isle_list:
                try:
                
                    if isle.rect.collidepoint(pos):
                        
                        isle.clicked = "I've Clicked you"
                        
                except:
                    pass
                
        if event.type == pygame.QUIT:
            quit()
    
    
def gen_world(squares):
    count = 0
    for row in range(1,squares+1):
        for col in range(1,squares+1):
            count += 1
            grid_list.append(_Grid(count,row,col))
            
    print(count)
        
        
page = 16
gen_world(page)
cam = Camera()
    
    

    


    

    

    
    
     
    


while True:
    draw_window()
    
    #Cycle through the different events we expect. 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    keys = pygame.key.get_pressed()  #checking pressed keys
    
    pygame.display.update()        
    clock.tick(FPS)