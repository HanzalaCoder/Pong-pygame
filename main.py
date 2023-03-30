import pygame
import random
from sys import exit


class Design:
    def __init__(self,screen,width,height):
        self.screen = screen
        self.screen_width = width
        self.screen_height = height
        self.image = pygame.image.load("images/buttonRed1.png")
        self.font = pygame.font.Font("font/IndianPoker.ttf",15)
        self.player1_wins = 0
        self.opponent_wins = 0

    def player1_score(self):
        self.screen.blit(self.image,(0,380))
        surf = self.font.render(f"Wins {self.player1_wins}",False,"green")
        self.screen.blit(surf,(5,380))

    def opponent_score(self):
        self.screen.blit(self.image,(0,350))
        surf = self.font.render(f"Wins {self.opponent_wins}",False,"red")
        self.screen.blit(surf,(5,350))

    def display_design(self):
        pygame.draw.line(self.screen,"white",(0,375),(900,375))


class Player:
    def __init__(self,screen,x_pos,y_pos,speed):
        self.surface = pygame.surface.Surface((150,15))
        self.react = self.surface.get_rect(midbottom=(x_pos,y_pos))
        self.surface.fill("green")
        self.screen = screen
        self.speed = speed

    def player_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.react.x -= self.speed
        if keys[pygame.K_d]:
            self.react.x += self.speed

    def player_constrain(self):
        if self.react.x >= 760:
            self.react.x = 760
        if self.react.x <= 0:
            self.react.x = 0

    def update(self):
        self.screen.blit(self.surface,self.react)
        self.player_movement()
        self.player_constrain()


class Opponent:
    def __init__(self,screen,x_pos,y_pos):
        self.surface = pygame.surface.Surface((125, 15))
        self.react = self.surface.get_rect(midbottom=(x_pos, y_pos))
        self.surface.fill("red")
        self.screen = screen
        self.speed = 7

    def opponent_movement(self,ball_rect):
        if self.react.right < ball_rect.x:
            self.react.x += self.speed

        if self.react.left > ball_rect.x:
            self.react.x -= self.speed

        if self.react.x >= 760:
            self.react.x = 760
        if self.react.left <= 0:
            self.react.left = 0

    def update(self,ball):
        self.screen.blit(self.surface,self.react)
        self.opponent_movement(ball)


class Ball:
    def __init__(self,screen,x_pos,y_pos):
        self.ball = pygame.Rect(y_pos/2 - 20, x_pos, 30, 30)
        self.screen = screen
        self.ball_speed_x = 0
        self.ball_speed_y = 0
        self.collision_tolerance = 10
        self.font = pygame.font.Font("font/Pixeltype.ttf",40)
        self.release_ball = True

    def ball_constrain(self):
        self.ball.x += self.ball_speed_x
        self.ball.y += self.ball_speed_y
        if self.ball.top <= 0:
            self.ball_speed_y = 0
            self.ball_speed_x = 0
            self.ball.center = (450, 375)
            game.design.player1_wins += 1
            self.release_ball = True
            game.start_time = pygame.time.get_ticks()

        if self.ball.bottom >= 750:
            self.ball_speed_y = 0
            self.ball_speed_x = 0
            self.ball.center = (450,375)
            game.design.opponent_wins += 1
            self.release_ball = True

            game.start_time = pygame.time.get_ticks()

        if self.ball.left <= 0:
            self.ball_speed_x *= -1

        if self.ball.right >= 880:
            self.ball_speed_x *= -1

    def start_ball(self,score_time):

        if self.release_ball:
            current_time = pygame.time.get_ticks()
            self.ball.center = (450, 375)
            if current_time - score_time < 700:
                number_three = self.font.render("3", False, "green")
                self.screen.blit(number_three, (450, 330))
            if 700 < current_time - score_time < 1000:
                number_two = self.font.render("2", False, "green")
                self.screen.blit(number_two, (450, 330))
            if 1400 < current_time - score_time < 2100:
                number_one = self.font.render("1", False, "green")
                self.screen.blit(number_one, (450, 330))
            if current_time - score_time < 2100:
                self.ball_speed_x, self.ball_speed_y = 0, 0
            else:
                self.ball_speed_x = random.choice((-7,))
                self.ball_speed_y = random.choice((-7,))
                self.release_ball = False

    def player_collision_ball(self,pad):
        if self.ball.colliderect(pad):
            if abs(pad.top - self.ball.bottom) < self.collision_tolerance and self.ball_speed_y > 0:
                self.ball_speed_y *= -1
            if abs(pad.bottom - self.ball.top) < self.collision_tolerance and self.ball_speed_y < 0:
                self.ball_speed_y *= -1
            if abs(pad.right - self.ball.left) < self.collision_tolerance and self.ball_speed_x < 0:
                self.ball_speed_x *= -1
            if abs(pad.left - self.ball.right) < self.collision_tolerance and self.ball_speed_x > 0:
                self.ball_speed_x *= -1

    def opponent_collision_ball(self,pad2):
        if self.ball.colliderect(pad2):
            if abs(pad2.top - self.ball.bottom) < self.collision_tolerance and self.ball_speed_y > 0:
                self.ball_speed_y *= -1
            if abs(pad2.bottom - self.ball.top) < self.collision_tolerance and self.ball_speed_y < 0:
                self.ball_speed_y *= -1
            if abs(pad2.right - self.ball.left) < self.collision_tolerance and self.ball_speed_x < 0:
                self.ball_speed_x *= -1
            if abs(pad2.left - self.ball.right) < self.collision_tolerance and self.ball_speed_x > 0:
                self.ball_speed_x *= -1

    def update(self):
        pygame.draw.ellipse(self.screen,"white",self.ball)
        self.ball_constrain()


class Game:
    def __init__(self):
        self.start_time = True
        self.width = 900
        self.height = 750
        self.screen = pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption("Pong by Hanzala")
        self.design = Design(self.screen,self.width,self.height)

        self.player = Player(self.screen,self.width/2,self.height,10)
        self.opponent = Opponent(self.screen,self.width/2,18)
        self.ball = Ball(self.screen,self.width,375)

    def update(self):
        bg_color = pygame.Color('grey12')
        self.screen.fill(bg_color)
        self.design.display_design()
        self.design.player1_score()
        self.design.opponent_score()

        self.ball.start_ball(self.start_time)

        self.ball.update()
        self.player.update()
        self.opponent.update(ball=self.ball.ball)

        self.ball.player_collision_ball(self.player.react)
        self.ball.opponent_collision_ball(self.opponent.react)


pygame.init()

game = Game()
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    game.update()

    pygame.display.update()
    clock.tick(60)
