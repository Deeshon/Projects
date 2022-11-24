import pygame
from pygame.math import Vector2
import random
pygame.font.init()

WIN_WIDTH , WIN_HEIGHT = 640 , 480
CELL_WIDTH , CELL_HEIGHT = 20 , 20
CELL_X = 0
CELL_Y = 20
WIN = pygame.display.set_mode((WIN_WIDTH , WIN_HEIGHT))
LOSE_SCREEN = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))


class Snake():
    def __init__(self) -> None:
        self.body = [Vector2(100,100) , Vector2(80,100) , Vector2(60,100)]
        self.direction = Vector2(20,0)
    def draw_snake(self , WIN):
        for block in self.body:
            pygame.draw.rect(WIN , (255,0,0) , (block.x , block.y , 20 , 20))

    def move_snake(self):
        body_copy = self.body[:-1]
        body_copy.insert(0 , body_copy[0] + self.direction)
        self.body = body_copy[:]
    
    def grow_snake(self):
        body_copy = self.body[:]
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
        pygame.draw.rect(WIN , (251, 206, 177) , (self.pos.x , self.pos.y , 20 , 20))


 


class Main_game():
    def __init__(self) -> None:
        self.snake = Snake()
        self.apple = Food()
    def update(self):
        self.snake.move_snake()

    def draw_surfaces(self , CELL_X , CELL_Y , CELL_WIDTH , CELL_HEIGHT , SCORE):
        self.snake.draw_snake(WIN)
        self.apple.draw(WIN)

        #draw grid
        while CELL_Y < 480:
            while CELL_X < 640:
                pygame.draw.rect(WIN , (1, 50, 32) , (CELL_X , CELL_Y , CELL_WIDTH , CELL_HEIGHT) , 1)
                CELL_X+=20
            CELL_Y+=20
            CELL_X = 0  
        
        FONT = pygame.font.SysFont("TimesNewRoman" , 20)
        score_label = FONT.render(f"Score:{SCORE}" , 1 , (255,255,255))
        WIN.blit(score_label , (0,0))
        pygame.display.update()

    def apple_snake_collision(self):
        #select two random integers that are divisible by 20(so that they fit right in a cell in the grid) for x and y
        while True:
            x = random.randrange(0 , WIN_WIDTH-20)
            y = random.randrange(40 , WIN_HEIGHT-20)

            if x%20 == 0 and y%20 == 0:
                break
            else:
                pass
        offset_x = self.snake.body[0].x - self.apple.pos.x
        offset_y = self.snake.body[0].y - self.apple.pos.y
        if offset_x==0 and offset_y==0:
            self.apple.pos = Vector2(x,y)
            self.snake.grow_snake()
            return 0
    def snake_collision(self):
        for block in self.snake.body[1:]:
            if self.snake.body[0] == block:
                return 1
            else:
                pass
    def boundary_collision(self):
        if self.snake.body[0].x < 0 or self.snake.body[0].x == WIN_WIDTH or self.snake.body[0].y == 0 or self.snake.body[0].y == WIN_HEIGHT:
            return 1


def msg(FONT):
    label = FONT.render("Press R to restart or Press Q to exit" , 1 , (255,0,0))
    WIN.blit(label , (170,200))



def gameloop():
    SCORE = 0
    FONT = pygame.font.SysFont("TimesNewRoman" , 20)
    VEL=15
    game_over = False
    game_close = False

    run_game = Main_game()
    SCREEN_UPDATE = pygame.USEREVENT
    clock = pygame.time.Clock()

    
    while not game_over:
        
        while game_close == True:
            WIN.fill((255,255,255))
            msg(FONT)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        gameloop()
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_q]:
                game_over=True
                game_close=False       
        
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                game_over = True
                
            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_UP:
                    run_game.snake.direction = Vector2(0,-20)
                if events.key == pygame.K_DOWN:
                    run_game.snake.direction = Vector2(0,20)               
                if events.key == pygame.K_LEFT:
                    run_game.snake.direction = Vector2(-20,0)
                if events.key == pygame.K_RIGHT:
                    run_game.snake.direction = Vector2(20,0)       
    
        WIN.fill((0,0,0))
        run_game.draw_surfaces(CELL_X , CELL_Y , CELL_WIDTH , CELL_HEIGHT , SCORE)
        if run_game.apple_snake_collision() == 0:
            SCORE+=1
        if run_game.snake_collision() == 1:
            game_close = True
        if run_game.boundary_collision() == 1:
            game_close = True
        run_game.update()
        pygame.display.update()
        if SCORE >= 10 < 20:
            VEL=20
        elif SCORE >=20:
            VEL=25
        clock.tick(VEL)
            
            
gameloop()
