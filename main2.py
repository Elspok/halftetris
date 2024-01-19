import pygame
import math
import random

pygame.init()
WIDTH = 600
HEIGHT = 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
#making of the basic shapes and where they should start 
T_COOR = [[12,0], [14,0], [16,0], [14,2]]
O_COOR = [[12,0], [14,0], [12,2], [14,2]]
I_COOR = [[10,0], [12,0], [14,0], [16,0]]
L_COOR = [[14,0], [14,2], [14,4], [16,4]]
S_COOR =  [[12,0], [14,0], [10,2], [12,2]]

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

class Grid():
    def __init__(self, space_between, thickness,color):
        self.space_between = space_between
        self.thickness = thickness
        self.color = color 
        self.horizontal_positions = [[0,y] for y in range(0,HEIGHT, self.space_between)]
        self.vertical_positions = [[x,0] for x in range(0, WIDTH, self.space_between)]       
        self.horizontal_lines = [pygame.Rect(y[0], y[1], WIDTH,thickness) for y in self.horizontal_positions]
        self.vertical_lines = [pygame.Rect(x[0],x[1],thickness, HEIGHT) for x in self.vertical_positions]
    def display(self):
        lines = self.horizontal_lines
        lines.extend(self.vertical_lines)
        for line in lines:
            pygame.draw.rect(screen,self.color,line)
      
#0 in terms of a simpler coordinate system is going to be the fist inter
#section between the second top horizontal line and the second left vertical line

class Shape():
    def __init__(self, horizontal_positions, vertical_positions,color, positions):
        #position shoud be an array of points (or squares)
        #that describe the hole shape
        self.horizontal_positions = horizontal_positions
        self.vertical_positions = vertical_positions
        self.color = color
        self.positions = positions
        self.size = 2*(self.horizontal_positions[1][1] - self.horizontal_positions[0][1])        
        # from here we do the calculations
        self.center_positions = []
        self.real_positions = []
        self.squares = [] 
    #the translation      
    def make_shape(self):                                             
        squares = []
        for i,position in enumerate(self.positions):            
            self.center_positions.extend([[self.vertical_positions[position[0] + 2][0], self.horizontal_positions[position[1] + 2][1]]])
            self.real_positions.extend([[self.center_positions[i][0] - int(self.size/2), self.center_positions[i][1] - int(self.size/2)]])
            squares.extend([pygame.Rect(self.real_positions[i][0], self.real_positions[i][1], self.size, self.size)])              
        return squares  
    def display(self):
        self.squares = self.make_shape()
        self.positions
        for square in self.squares:
            pygame.draw.rect(screen, self.color, square)          
    def rotate(self, angle):                   
        rotation = math.radians(angle)
        center = self.positions[2]    
        vectors_from_center = [[position[0] - center[0], position[1] - center[1]] for position in self.positions]       
        vectors_from_center.pop(2)
        vectors_modules = [math.sqrt(vector[0]**2 + vector[1]**2) for vector in vectors_from_center]
        angles = [math.acos(vectors_from_center[i][0]/vectors_modules[i]) for i in range(len(vectors_modules))]
        new_vectors = [[round(vectors_modules[i]*math.cos(angles[i] + rotation)),round(vectors_modules[i]*math.sin(angles[i] + rotation))] for i in range(len(angles))]        
        new_points = [[new_vectors[i][0] + center[0],new_vectors[i][1] + center[1]] for i in range(len(new_vectors))]
        return [new_points[0], new_points[1],center , new_points[2]]
    def move(self, dir, sp):
        direction = dir # the direction vector is an array that indicates where the shape is moving [1,0] or [0,1] or [-1,0] or [0,-1] 
        speed = sp
        if direction[0] != 0:
            self.positions= [[position[0] + speed*direction[0], position[1]] for position in self.positions]  
            return self.positions
        elif direction[1] != 0:
            self.positions =  [[position[0], position[1] + speed*direction[1]] for position in self.positions]
            return self.positions     
    def on_vertical_limit(self):
        vertical_limit = self.horizontal_positions[len(self.horizontal_positions)-1][1] - self.size
        for position in self.real_positions:
            if position[1] >= vertical_limit:
                return True
        return False  
    def on_top(self):
        top = self.horizontal_positions[0][1] + self.size
        for position in self.real_positions:
            if position[1] <= top:
                return True
        return False 
    def get_rects(self):
        return self.squares
    def get_colitions(self, old_shapes):
        if len(old_shapes) < 0:
            return False        
        for shape in old_shapes:
            for old_rect in shape.get_rects():
                for square in self.squares:
                    if pygame.Rect.colliderect(square, old_rect):
                        return True 
        return False
    
    
grid = Grid(20,1, (60, 179, 113))

def creator():
    #Here all of the shapes that had already falled to the floor will be saved
    coordinates = [T_COOR,O_COOR,I_COOR,L_COOR,S_COOR]
    colors = [RED,GREEN,BLUE,YELLOW,CYAN]
    rotations = [0,90,180,270]
    random_coor_col = random.randint(0,len(coordinates)-1)
    random_coor = coordinates[random_coor_col]
    random_color = colors[random_coor_col] 
    rotation = rotations[random.randint(0,len(rotations)-1)]
    random_shape = Shape(grid.horizontal_positions,grid.vertical_positions, random_color, random_coor)    
    if rotation != 0: 
        random_shape = Shape(grid.horizontal_positions,grid.vertical_positions, random_shape.color, random_shape.rotate(rotation))                                 
    #This display is nescesary for the while to work       
    #There is a bug that happens only on cicle zero a rotated piece, sometimes
    #gets stuck because it is in the vertical limit
      
    #to correct it we should move it a bit downwards        
    random_shape.display()
    while random_shape.on_vertical_limit():
        new_positions = random_shape.move([0,1], 1)
        random_shape = Shape(grid.horizontal_positions,grid.vertical_positions, random_shape.color, new_positions)
        random_shape.display()
    return random_shape

random_old = [] 
cycles = 0 
while running == True:
    if cycles == 0:    
        random_shape = creator()   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if random_shape.on_vertical_limit() == False:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN: 
                    new_positions = random_shape.move([0,1],3) 
                    random_shape = Shape(grid.horizontal_positions,grid.vertical_positions, random_shape.color, new_positions)    
                    print("in")
                if event.key == pygame.K_RIGHT:
                    new_positions = random_shape.move([1,0],1) 
                    random_shape = Shape(grid.horizontal_positions,grid.vertical_positions, random_shape.color, new_positions)
                if event.key == pygame.K_LEFT:
                    new_positions = random_shape.move([-1,0],1) 
                    random_shape = Shape(grid.horizontal_positions,grid.vertical_positions, random_shape.color, new_positions)
                if event.key == pygame.K_SPACE:
                    random_shape = Shape(grid.horizontal_positions,grid.vertical_positions, random_shape.color, random_shape.rotate(90))                        
    screen.fill("white")
    grid.display()    
    if random_shape.on_vertical_limit() == False and random_shape.get_colitions(random_old) == False:
        new_positions = random_shape.move([0,1],1) 
        random_shape = Shape(grid.horizontal_positions,grid.vertical_positions, random_shape.color, new_positions)
    else:
        print('in')
        if random_shape.get_colitions(random_old) ==  True:           
            new_positions = random_shape.move([0,1], -1)
            random_shape = Shape(grid.horizontal_positions,grid.vertical_positions, random_shape.color, new_positions)            
        random_old.extend([random_shape])
        cycles = -1
    if len(random_old) > 0:    
        for shape in random_old:                   
            shape.display()     
            if shape.on_top():
                running = False   
    random_shape.display()    
    cycles += 1        
    pygame.display.flip()

    pygame.time.delay(100)
