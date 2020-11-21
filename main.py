import pygame
import math
import random
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Space Wars')
icon = pygame.image.load('visuals/ufo.png')
pygame.display.set_icon(icon)
running = True

playerimg = pygame.image.load('visuals/spaceship.png')
bulletimg = pygame.image.load('visuals/bullet.png')
astimg = pygame.image.load('visuals/asteroid.png')
background = pygame.image.load('visuals/space.gif')

# sound
bullet_sound = mixer.Sound('audio/laser.wav')
dead_sound = mixer.Sound('audio/lose.wav')
mixer.music.load('audio/bgm.wav')
mixer.music.play(-1)

playerx = 370
playery = 480
playery_change = 0
playerx_change = 0

bulletx = playerx
bullety = playery
bullety_change = -1
bulletx_change = 10
bullet_state = 'ready'

astx = random.randint(0, 250)
asty = -500
asty_change = random.uniform(0.5, 0.8)

ast2x = random.randint(260, 350)
ast2y = -350
ast2y_change = random.uniform(0.5, 0.8)

ast3x = random.randint(360, 530)
ast3y = -150
ast3y_change = random.uniform(0.5, 0.8)

ast4x = random.randint(540, 700)
ast4y = -64
ast4y_change = random.uniform(0.5, 0.8)

# adding a score board
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
txtx = 10
txty = 10


def scoreboard(x, y):
    score = font.render('Score : ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletimg, (x+16, y+10))


def player(x, y):
    # drawing the image on the screen
    screen.blit(playerimg, (x, y))


def asteroid(a, b):
    screen.blit(astimg, (a, b))


def asteroid2(c, d):
    screen.blit(astimg, (c, d))


def asteroid3(e, f):
    screen.blit(astimg, (e, f))


def asteroid4(g, h):
    screen.blit(astimg, (g, h))


def collision(astx, asty, bulletx, bullety):
    distance = math.sqrt((math.pow(astx-bulletx, 2)) +
                         (math.pow(asty-bullety, 2)))
    if distance < 32:
        return True
    else:
        return False


def player_collision(astx, asty, playerx, playery):
    distance = math.sqrt((astx-playerx)**2 + (asty-playery)**2)

    if distance < 50:
        return True
    return False


def main():
    global playerx, playery, astx, asty, ast2x, ast2y, ast3x, ast3y, ast4x, ast4y, bulletx, bullety, bullet_state, score_value

    playery += playery_change
    if playery <= 0:
        playery = 0
    elif playery >= 536:
        playery = 536

    playerx += playerx_change
    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736

    asty += asty_change
    if asty >= 700:
        asty = -400
        astx = random.randint(20, 200)

    ast2y += ast2y_change
    if ast2y >= 700:
        ast2y = -600
        ast2x = random.randint(220, 400)

    ast3y += ast3y_change
    if ast3y >= 700:
        ast3y = -800
        ast3x = random.randint(420, 600)

    ast4y += ast4y_change
    if ast4y >= 700:
        ast4y = -200
        ast4x = random.randint(620, 736)
    # bullet movement
    if bullety <= 0:
        bullety = playery
        bullet_state = 'ready'

    if bullet_state == 'fire':
        fire_bullet(bulletx, bullety)
        bullety += bullety_change

    collide = collision(astx, asty, bulletx, bullety)
    if collide and bullet_state == 'fire':
        asty = -400
        astx = random.randint(0, 250)
        bullet_state = 'ready'
        bullety = playery
        score_value += 1

    collide2 = collision(ast2x, ast2y, bulletx, bullety)
    if collide2 and bullet_state == 'fire':
        ast2x = random.randint(260, 350)
        ast2y = -600
        bullet_state = 'ready'
        bullety = playery
        score_value += 1

    collide3 = collision(ast3x, ast3y, bulletx, bullety)
    if collide3 and bullet_state == 'fire':
        ast3x = random.randint(360, 530)
        ast3y = -800
        bullet_state = 'ready'
        bullety = playery
        score_value += 1

    collide4 = collision(ast4x, ast4y, bulletx, bullety)
    if collide4 and bullet_state == 'fire':
        ast4x = random.randint(540, 700)
        ast4y = -200
        bullet_state = 'ready'
        bullety = playery
        score_value += 1

    player_collide1 = player_collision(astx, asty, playerx, playery)
    player_collide2 = player_collision(ast2x, ast2y, playerx, playery)
    player_collide3 = player_collision(ast3x, ast3y, playerx, playery)
    player_collide4 = player_collision(ast4x, ast4y, playerx, playery)
    if player_collide1 or player_collide2 or player_collide3 or player_collide4:
        dead_sound.play()
        playerx = 370
        playery = 480
        astx = random.randint(0, 250)
        asty = -500
        ast2x = random.randint(260, 350)
        ast2y = -350
        ast3x = random.randint(360, 530)
        ast3y = -150
        ast4x = random.randint(540, 700)
        ast4y = -64
        bulletx = playerx
        bullety = playery
        bullet_state = 'ready'
        score_value = 0

    asteroid(astx, asty)
    asteroid2(ast2x, ast2y)
    asteroid3(ast3x, ast3y)
    asteroid4(ast4x, ast4y)
    player(playerx, playery)
    scoreboard(txty, txty)
    pygame.display.update()


# game loop
while running:

    # RGB red green blue , remember 'screen' is the value for the window
    screen.fill((0, 0, 0))
    # background
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # check keystroke if left or right
            if event.key == pygame.K_LEFT:
                playerx_change = -1
            if event.key == pygame.K_UP:
                playery_change = -1
            if event.key == pygame.K_DOWN:
                playery_change = 1
            if event.key == pygame.K_RIGHT:
                playerx_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bulletx = playerx
                    bullety = playery
                    fire_bullet(bulletx, bullety)
                    bullet_sound.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playery_change = 0

    main()
