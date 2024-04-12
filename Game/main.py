import pygame
from sys import exit

pygame.init()
height = 700
width = 735
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invader")
clock = pygame.time.Clock()
icon = pygame.image.load("res/Icon.png").convert_alpha()
pygame.display.set_icon(icon)
x = True
# Enemy side-way movement clock and variables

clock_side = pygame.time.Clock()
side_timer = 0
count = 75
rate = 2
touch_border = False

# Enemy vertical movement clock and variables

clock_vertical = pygame.time.Clock()
vertical_timer = 0

direction = "Left"

# Background

space_surface = pygame.image.load("res/Black.png").convert()

# Player

shuttle_surf = pygame.image.load("res/Shuttle2.png").convert_alpha()
shuttle_rect = shuttle_surf.get_rect(midbottom = (width/2, 650))

# Enemy

ufo_surf = pygame.image.load("res/Ufo.png").convert_alpha()

# Beam

beam_surf = pygame.image.load("res/Beam.png").convert_alpha()

# Final line

final_line_surf = pygame.image.load("res/Final_line.png").convert()

def create_enemy_list():
    n_line = 5
    n_column = 15
    list_enemy = [[] for _ in range(n_line)]
    for i in range(n_line):
        for l in range(n_column):
            ufo_rect = ufo_surf.get_rect(midleft = (15 * (1*l + 1) + (33*l), (1+i) * 50))
            list_enemy[i].append(ufo_rect)
    return list_enemy
                
list_enemy = create_enemy_list()  
beam = 0      
        
def create_beam():      
    beam = beam_surf.get_rect(center = (shuttle_rect.centerx - 2 , 550))
    return beam

while True:
    for event in pygame.event.get():
        
        # Closing the game window
        
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        # Keyboard input for shooting
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not beam:
                    beam = create_beam()
                    
                
                
        side_movement_elapsed = 0
                    
    
    # Cleaning an empty line
    
    while [] in list_enemy:
        list_enemy.remove([])
            
    # GameOver
    
    if list_enemy == []:
        pygame.quit()
        exit()             
    
    
    
    # Movement of beam
    
    if beam:
        beam.y -= 15
        if beam.top <= 0:
           beam = 0
        
    # Keyboard input for shuttle
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
            shuttle_rect.x -= 2
    if keys[pygame.K_RIGHT]:
            shuttle_rect.x += 2
    if shuttle_rect.left <= -25:
        shuttle_rect.left = -25
    if shuttle_rect.right >= width + 25:
        shuttle_rect.right = width + 25   
        
    # Collision check
    
    if beam:
        for line in list_enemy:
            for column in line:
                collide = beam.colliderect(column)
                if collide:
                    line.remove(column)
                    count -= 1
                    beam = 0
                    break
            if beam == 0:
                break
    
    # Timer and movement of enemy (side-way)
    
    if count == 60:
        rate = 3
    if count == 45:
        rate = 4
    if count == 30:
        rate = 5
    if count == 15:
        rate = 6
        
    side_time_elapsed = clock_side.tick()
    side_timer += side_time_elapsed
    
    
    if side_timer >= 50:
        for i in range(len(list_enemy)-1, -1, -1):
            for l in range(len(list_enemy[i])):
                if direction == "Left":
                    list_enemy[i][l].x -= rate
                if direction == "Right":
                    list_enemy[i][l].x += rate
                screen.blit(ufo_surf, list_enemy[i][l])
            if list_enemy[i]:
                if list_enemy[i][0].x <= 0:
                    touch_border = True  
                elif list_enemy[i][len(list_enemy[i])-1].x >= width -33:
                    touch_border = True
        if touch_border:
            if direction == "Left":
                direction = "Right"
            elif direction == "Right":
                direction = "Left"
            touch_border = False
        side_timer = 0            
    
    # Timer and movement of enemy (vertical)
    
    vertical_time_elapsed = clock_vertical.tick()
    vertical_timer += vertical_time_elapsed
    
    if vertical_timer >= 12000:
        
        for i in range(len(list_enemy)-1, -1, -1):
            for l in range(len(list_enemy[i])):
                list_enemy[i][l].y += 50
                if list_enemy[i][l].y >= 530:
                    pygame.quit()
                    exit()
                
        
        vertical_timer = 0
    
    
    # Blits    
        
    screen.blit(space_surface, (0,0))     
    screen.blit(shuttle_surf, shuttle_rect)
    screen.blit(final_line_surf, (0, 530))
    
    
    
    for line in list_enemy:
        for column_of_line in line:
            if column_of_line:
                screen.blit(ufo_surf, column_of_line)
                
                
    if beam:
        screen.blit(beam_surf, beam)
    
    pygame.display.update()
    clock.tick(60)