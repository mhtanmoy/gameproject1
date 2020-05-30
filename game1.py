import pygame as pg
import sys
import random


wid = 800
hght = 600

#init pygame
pg.init()
#display section
dis =  pg.display.set_mode(( wid, hght ))

#color tuple
obj_color = (13, 4, 71)
enemy_color = (237, 36, 170)
back_color = (255, 215, 54)

#variable
obj_pos = [370,500]
obj_size = [50,50]
enemy_size = [50,50]
enemy_pos = [random.randint(0, wid-enemy_size[1]),0]
enemy_list = [enemy_pos]
speed = 10
score = 0

game_over = False

#fps section
clock = pg.time.Clock()
font = pg.font.SysFont("monospace.png", 22)


def set_level(score, speed):
    # if score < 10:
    #     speed = 8
    # elif score < 20:
    #     speed = 10
    # elif score < 40:
    #     speed = 13
    # elif score < 60:
    #     speed = 15
    # elif score < 80:
    #     speed = 18
    # else:
    #     speed = 23
    speed = score/9 + 8
    return speed

def drop_enemy(enemy_list):
    delay = random.random()
    if len(enemy_list) < 30 and delay < 0.1 :
        x_pos = random.randint(0,wid+enemy_size[0])
        y_pos = 0
        enemy_list.append([x_pos,y_pos])

def draw_enemies(enemy_list):
    for enemy in enemy_list:
        img1 = pg.image.load("logo1.png")
        rect1 = pg.Rect( enemy[0], enemy[1], enemy_size[0], enemy_size[1])
        scale_img = pg.transform.scale(img1, rect1.size)
        scale_img = scale_img.convert()
        dis.blit(scale_img, rect1)

def update_enemy_pos(enemy_list, score):
    #update section of enemy obj
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < hght:
            enemy_pos[1] += speed
        else:
            enemy_list.pop(idx)
            score += 1
    return score

def collision_check(enemy_list, obj_pos):
    for enemy_pos in enemy_list:
        if detect_collision(enemy_pos, obj_pos):
            return True
    return False

def detect_collision(obj_pos, enemy_pos):
    obj_x = obj_pos[0]
    obj_y = obj_pos[1]
    en_x = enemy_pos[0]
    en_y = enemy_pos [1]
    if (en_x >= obj_x and en_x < (obj_x+obj_size[0])) or (obj_x >= en_x and obj_x < (en_x+enemy_size[0])):
        if (en_y >= obj_y and en_y < (obj_y+obj_size[0])) or (obj_y >= en_y and obj_y < (en_y+enemy_size[0])):
            return True
    return False


while not game_over:
    for event in pg.event.get():
        #input section
        if event.type == pg.QUIT:
            sys.exit()
        if event.type == pg.KEYDOWN:
            x = obj_pos[0]
            y = obj_pos[1]
            if event.key == pg.K_LEFT and x > 0:
                x -= 40
            elif event.key == pg.K_RIGHT and x <= (wid - obj_size[0]):
                x += 40
            
            obj_pos = [x,y]
    
    dis.fill(back_color)
        
    
    #draw section
    drop_enemy(enemy_list)
    score = update_enemy_pos(enemy_list, score)
    speed = set_level(score, speed)
    point = "point: " + str(score)
    label1 = font.render(point, 1 , obj_color)
    dis.blit(label1, (wid-150, hght-40))

    if collision_check(enemy_list, obj_pos):
        game_over = True
        break
    draw_enemies(enemy_list)

    img1 = pg.image.load("logo2.png")
    rect = pg.Rect( obj_pos[0], obj_pos[1], obj_size[0], obj_size[1] )
    scale_img = pg.transform.scale(img1, rect.size)
    scale_img = scale_img.convert()
    dis.blit(scale_img, rect)
    
    clock.tick(30)
    pg.display.update()
