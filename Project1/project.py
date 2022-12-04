import pygame
from pygame.math import Vector2
import random
pygame.font.init()
pygame.mixer.init()

WIN_WIDTH , WIN_HEIGHT = 640 , 480
CELL_WIDTH , CELL_HEIGHT = 20 , 20
CELL_X = 0
CELL_Y = 20
WIN = pygame.display.set_mode((WIN_WIDTH , WIN_HEIGHT))
pygame.display.set_caption("Snake Rush")
#background image configuration
BG_IMG = pygame.image.load("data/bgimg.png")
BG_IMG = pygame.transform.scale(BG_IMG , (WIN_WIDTH , WIN_HEIGHT))
#lost screen configuration
IMG = pygame.image.load("data/img.png")
IMG = pygame.transform.scale(IMG , (WIN_WIDTH , WIN_HEIGHT))

APPLE_IMG = pygame.image.load("data/apple1.png")
APPLE_IMG = pygame.transform.scale(APPLE_IMG , (35,30))

SNAKE_HEAD_IMG = pygame.image.load("data/body.png")
SNAKE_HEAD_IMG = pygame.transform.scale(SNAKE_HEAD_IMG , (35,30))

SNAKE_BODY_IMG = pygame.image.load("data/body.png")
SNAKE_BODY_IMG = pygame.transform.scale(SNAKE_BODY_IMG , (35,30))

BTN_IMG = pygame.image.load("data/oval-23967_960_720.png")
BTN_IMG = pygame.transform.scale(BTN_IMG , (200,100))

GOBBLE_SOUND = pygame.mixer.Sound("data/Sound_crunch.wav")
CRASH_SOUND = pygame.mixer.Sound("data/mixkit-funny-fail-low-tone-2876.wav")
GAME_SOUND = pygame.mixer.Sound("data/Snake Game - Theme Song.mp3")


class Snake():
    def __init__(self) -> None:
        self.body = [Vector2(100,100) , Vector2(80,100) , Vector2(60,100)]
        self.direction = Vector2(20,0)
    def draw_snake(self , WIN):
        for block in self.body:
            if block == self.body[0]:
               WIN.blit(SNAKE_HEAD_IMG , (block.x , block.y))
            else:
                WIN.blit(SNAKE_BODY_IMG , (block.x , block.y))

    def move_snake(self):
        body_copy = self.body[:-1]
        body_copy.insert(0 , body_copy[0] + self.direction)
        self.body = body_copy[:]
    
    def grow_snake(self):
        body_copy = self.body[:]
        body_copy.insert(1 , body_copy[1] + self.direction)
        body_copy.insert(0 , body_copy[0] + self.direction)
        
        self.body = body_copy[:]        

class Food:
    def __init__(self) -> None:
        #select two random integers that are divisible by 20(so that they fit right in a cell in the grid) for x and y
        while True:
            x = random.randrange(0 , WIN_WIDTH-20)
            y = random.randrange(0 , WIN_HEIGHT-20)

            if x%20 == 0 and y%20 == 0:
                break
            else:
                pass
        self.pos = Vector2(x,y)
    
    def draw(self , WIN):

        WIN.blit(APPLE_IMG , (self.pos.x , self.pos.y))

def update(snake):
    snake.move_snake()

def draw_surfaces(snake , apple , SCORE):
    snake.draw_snake(WIN)
    apple.draw(WIN)


    FONT = pygame.font.SysFont("TimesNewRoman" , 20)
    score_label = FONT.render(f"Score:{SCORE}" , 1 , (255,255,255))
    WIN.blit(score_label , (0,0))
    pygame.display.update()

def apple_snake_collision(snake , apple):
    #select two random integers that are divisible by 20(so that they fit right in a cell in the grid) for x and y
    while True:
        x = random.randrange(0 , WIN_WIDTH-20)
        y = random.randrange(40 , WIN_HEIGHT-20)

        if x%20 == 0 and y%20 == 0:
            break
        else:
            pass
    offset_x = snake.body[0].x - apple.pos.x
    offset_y = snake.body[0].y - apple.pos.y
    if offset_x==0 and offset_y==0:
        GOBBLE_SOUND.play()
        apple.pos = Vector2(x,y)
        snake.grow_snake()
        return 0
def snake_collision(snake):
    for block in snake.body[1:]:
        if snake.body[0] == block:
            CRASH_SOUND.play()
            return 1
        else:
            pass
def boundary_collision(snake):
    if snake.body[0].x < 0 or snake.body[0].x == WIN_WIDTH or snake.body[0].y < 0 or snake.body[0].y == WIN_HEIGHT:
        CRASH_SOUND.play()
        return 1


def msg(FONT):
    label = FONT.render("Press R to restart or Press Q to exit" , 1 , (255,0,0))
    WIN.blit(label , (170,200))


def main(status1 , status2):
    snake = Snake()
    apple = Food()
    state = False
    SCORE = 0
    FONT = pygame.font.SysFont("TimesNewRoman" , 20)
    VEL=15
    game_over = False
    game_close = False
    main_game = status2
    main_menu = status1
    instruction_menu = False
    clock = pygame.time.Clock()

    
    while not game_over:  
        
        while game_close == True: 
            WIN.blit(IMG , (0,0))
            msg(FONT)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        main_menu = False                       
                        main(False , True)
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_q]:
                game_over=True
                game_close=False       
               
        while main_game == True:
            
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    game_over = True
                    
                if events.type == pygame.KEYDOWN:
                    if events.key == pygame.K_UP:
                        snake.direction = Vector2(0,-20)
                    if events.key == pygame.K_DOWN:
                        snake.direction = Vector2(0,20)               
                    if events.key == pygame.K_LEFT:
                        snake.direction = Vector2(-20,0)
                    if events.key == pygame.K_RIGHT:
                        snake.direction = Vector2(20,0)       

            WIN.blit(BG_IMG , (0,0))
            draw_surfaces(snake , apple , SCORE)
            if apple_snake_collision(snake , apple) == 0:
                SCORE+=1
            if snake_collision(snake) == 1:
                game_close = True
                main_game = False
            if boundary_collision(snake) == 1:
                game_close = True
                main_game = False
            update(snake)
            pygame.display.update()
            if SCORE >= 10 < 20:
                VEL=20
            if SCORE >=20:
                VEL=23
            clock.tick(VEL)
            
        
        while instruction_menu == True:
            WIN.blit(IMG , (0,0))
            FONT2 = pygame.font.SysFont("TimesNewRoman" , 20)
            instructions = FONT2.render("Use arrow keys to move the snake" , 1 , (0,0,0))
            back = FONT2.render("Press B to return to Main menu" , 1 , (0,0,0))
            WIN.blit(instructions , (150,200))
            WIN.blit(back , (125 , 250))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        instruction_menu = False
                        main_menu = True
                
                if event.type == pygame.QUIT:
                    game_over = True
                    instruction_menu = False    
        
        while main_menu == True:
            
            WIN.blit(IMG , (0,0))
            WIN.blit(BTN_IMG , (150,150))
            FONT1 = pygame.font.SysFont("TimesNewRoman" , 40)
            start_label = FONT1.render("START" , 1 , (0,0,0))
            WIN.blit(start_label , (190,180))
            pos = pygame.mouse.get_pos()

            instruction_label = FONT1.render("Instructions" , 1 , (0,0,0))
            WIN.blit(instruction_label , (160 , 280))            
            
            for eventz in pygame.event.get():
                if eventz.type == pygame.QUIT:
                    game_over=True
                    
                    main_menu = False
                    
                if eventz.type == pygame.KEYDOWN:
                    if eventz.key == pygame.K_t:
                        main_game = True
                        main_menu = False
                if eventz.type == pygame.MOUSEBUTTONDOWN and ((pos[0] >=150 and pos[0] <= 350) and (pos[1] >= 150 and pos[1]<=250)):
                    main_game = True
                    main_menu = False
                if eventz.type == pygame.MOUSEBUTTONDOWN and ((pos[0] >=160 and pos[0] <= 345) and (pos[1] >= 290 and pos[1]<=310)):
                    instruction_menu = True
                    main_menu = False
  
            pygame.display.update()   
        pygame.quit

if __name__=="__main__":
    main(True , False)
