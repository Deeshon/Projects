import pygame
import random
pygame.font.init()


#window configuration
WIDTH , HEIGHT = 500 , 800
WIN = pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption("First game")

SHIP_WIDTH , SHIP_HEIGHT = 55 , 40
OBSTACLE_WIDTH , OBSTACLE_HEIGHT = 60 , 60



RED = (255,0,0)
FPS = 60
VEL = 5
ENEMY_VEL = 7
OBSTACLE_VEL = 9
BULLET_VEL = 7


WHITE = (255,255,255)
#background image configuration
BG_IMG = pygame.image.load("Assets/space1.png")
BG_IMG = pygame.transform.scale(BG_IMG , (WIDTH , HEIGHT))
#spaceship configuration
MY_SPACESHIP = pygame.image.load("Assets/spaceship_yellow.png")
MY_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(MY_SPACESHIP , (SHIP_WIDTH , SHIP_HEIGHT)) , 180)

#enemy spaceship configuration
ENEMY_SPACESHIP = pygame.image.load("Assets/spaceship_red.png")
ENEMY_SPACESHIP = pygame.transform.scale(ENEMY_SPACESHIP , (SHIP_WIDTH , SHIP_HEIGHT))

#obstacle configuration
OBSTACLE = pygame.image.load("Assets/meteor-26464.png")
OBSTACLE = pygame.transform.scale(OBSTACLE , (OBSTACLE_WIDTH , OBSTACLE_HEIGHT))

class Obstacle():
    def __init__(self , x , y):
        self.x = x
        self.y = y
        
    def draw(self , WIN):
        ob = pygame.Rect(self.x , self.y , OBSTACLE_WIDTH , OBSTACLE_HEIGHT )
        WIN.blit(OBSTACLE , (ob.x , ob.y))

    def collide(self , obj):
        obj.x = 1000
        obj.y = 1000


    
def win_drawings(my_spaceship , enemy_spaceship , BULLETS , BULLET_CAP , OBSTACLES , FONT , HEALTH , SCORE):
    #place BG_IMG on WIN
    WIN.blit(BG_IMG,(0,0))
    #draw text
    health_label = FONT.render(f"Health:{HEALTH}" , 1 , (255,255,255))
    score_label = FONT.render(f"Score:{SCORE}" , 1 , (255,255,255))

    WIN.blit(health_label , (10 , 10))
    WIN.blit(score_label , (390 , 10))
    
    #place MY_SPACESHIP on WIN
    WIN.blit(MY_SPACESHIP , (my_spaceship.x , my_spaceship.y))
    #place ENEMY_SPACESHIP on WIN
    WIN.blit(ENEMY_SPACESHIP , (enemy_spaceship.x , enemy_spaceship.y))
    #draw bullets
    for bullet in BULLETS:
        pygame.draw.rect(WIN , RED , bullet)
    #draw obstacles
    for obstacle in OBSTACLES:
        obstacle.draw(WIN)


    pygame.display.update()


def my_spaceship_movements(keys_pressed , my_spaceship):
    if keys_pressed[pygame.K_a] and my_spaceship.x - VEL > 0:#LEFT
        my_spaceship.x -= VEL
    if keys_pressed[pygame.K_d] and my_spaceship.x + VEL < WIDTH-50:#RIGHT
        my_spaceship.x += VEL
    if keys_pressed[pygame.K_w] and my_spaceship.y - VEL > 0:#FORWARD
        my_spaceship.y -= VEL
    if keys_pressed[pygame.K_s] and my_spaceship.y < HEIGHT-50:#BACKWARD
        my_spaceship.y += VEL


def enemy_spaceship_movements(enemy_spaceship):
    enemy_spaceship.y += ENEMY_VEL
    if enemy_spaceship.y > HEIGHT:
        enemy_spaceship.x = random.randrange(0 , WIDTH-50)
        enemy_spaceship.y = 50

def obstacle_movement(OBSTACLES):
    for obstacle in OBSTACLES:
        obstacle.y += OBSTACLE_VEL
    if obstacle.y > HEIGHT:
        obstacle.x = random.randrange(0 , WIDTH-50)
        obstacle.y = 50
   



def handle_bullets(BULLETS , enemy_spaceship , SCORE):
    
    for bullet in BULLETS:
        bullet.y -= BULLET_VEL
        if enemy_spaceship.colliderect(bullet):
            BULLETS.remove(bullet)
            enemy_spaceship.x = random.randrange(0 , WIDTH-50)
            enemy_spaceship.y = 50
            return 1

def handle_spaceship_collision(my_spaceship , enemy_spaceship , HEALTH):
    if enemy_spaceship.colliderect(my_spaceship) and HEALTH > 1:
        print(HEALTH)
        enemy_spaceship.x = random.randrange(0 , WIDTH-50)
        enemy_spaceship.y = 50
        return 0
    if enemy_spaceship.colliderect(my_spaceship) and HEALTH == 1:
        return 1

def ob_collide(ob , my_spaceship , HEALTH):
    offset_x = my_spaceship.x - ob.x
    offset_y = my_spaceship.y - ob.y
    if offset_x < -20:
        pass
    else:
        if offset_x <20 and offset_y < 20:
            ob.collide(ob)
            if HEALTH > 1:
                return 0
            elif HEALTH == 1:
                return 1



            


def main():
    
    my_spaceship = pygame.Rect(WIDTH/2 , HEIGHT-150 , SHIP_WIDTH , SHIP_HEIGHT )
    enemy_spaceship = pygame.Rect(WIDTH/2 , HEIGHT-750 , SHIP_WIDTH , SHIP_HEIGHT )


        
    OBSTACLE_COUNT = 3
    OBSTACLES = []
    BULLETS = []
    BULLET_CAP = 3 
    HEALTH = 3
    SCORE = 0
    FONT = pygame.font.SysFont("TimesNewRoman" , 30)

    clock = pygame.time.Clock()
    run=True
    while run:
        
        clock.tick(FPS)
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                run=False  

            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_SPACE:
                    bullet = pygame.Rect(my_spaceship.x , my_spaceship.y, 10 , 20)
                    BULLETS.append(bullet)

        while OBSTACLE_COUNT > 0:
            ob = Obstacle(random.randrange(0 , WIDTH-50),random.randrange(-200 , 0))
            OBSTACLES.append(ob)
            OBSTACLE_COUNT-=1
            print(OBSTACLES)

        keys_pressed = pygame.key.get_pressed()
        enemy_spaceship_movements(enemy_spaceship)
        my_spaceship_movements(keys_pressed , my_spaceship)
        obstacle_movement(OBSTACLES)
        status1 = ob_collide(ob , my_spaceship , HEALTH)
        status0 = handle_bullets(BULLETS , enemy_spaceship , SCORE)
        if status0 == 1:
            SCORE += 1
        status = handle_spaceship_collision(my_spaceship , enemy_spaceship , HEALTH)
        if status == 1 or status1 == 1:
            run=False
        if status == 0 or status1 == 0:
            HEALTH -= 1 
               
    
        win_drawings(my_spaceship , enemy_spaceship , BULLETS , BULLET_CAP , OBSTACLES , FONT , HEALTH , SCORE)


    pygame.quit

main()