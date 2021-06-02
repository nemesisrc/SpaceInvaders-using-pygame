import pygame
import random
import math
from pygame import mixer

# initialise pygame(compulsory)
pygame.init()

# create screen
screen = pygame.display.set_mode((800, 600))  # width,height

# title and icon
pygame.display.set_caption('SpaceInvaders')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# player
playerimg = pygame.image.load('space-invaders.png')
playerx = 370
playery = 500
playerx_change = 0

# enemy
enemyimg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load('monster.png'))
    enemyx.append(random.randint(0, 735))
    enemyy.append(random.randint(50, 150))
    enemyx_change.append(4)
    enemyy_change.append(10)

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bulletimg = pygame.image.load('bullet.png')
bulletx = 0
bullety = 500
bulletx_change = 0
bullety_change = 10
bullet_state = "ready"

# score
score = 0
font = pygame.font.Font('freesansbold.ttf', 30)
textx = 10
texty = 10

# game over text
over_font = pygame.font.Font('freesansbold.ttf', 80)


def show_score(x, y):
    score_value = font.render("Score : " + str(score), True, (255, 255, 255))  # boolean true means smooth edges
    screen.blit(score_value, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER!!", True, (255, 255, 255))
    screen.blit(over_text, (130, 250))


def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x, y))


def isCollision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt(math.pow(enemyx - bulletx, 2) + (math.pow(enemyy - bullety, 2)))
    if distance < 30:
        return True
    else:
        return False


# game loop
running = True
while running:

    # background colour (rgb); always use this before any img otherwise it gets over-ridden
    screen.fill((255, 255, 0))
    # background image
    background = pygame.image.load('background.png')
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -5
            if event.key == pygame.K_RIGHT:
                playerx_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    fire_bullet(playerx, bullety)
                    bulletx = playerx
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0
    # player movement
    playerx += playerx_change
    if playerx > 736:
        playerx = 736
    if playerx < 0:
        playerx = 0
    player(playerx, playery)

    # enemy movement
    for i in range(num_of_enemies):
        # Game Over
        if enemyy[i] > 460:
            for j in range(num_of_enemies):
                enemyy[j] = 2000
            game_over_text()
            break
        enemyx[i] += enemyx_change[i]
        if enemyx[i] > 736:
            enemyx_change[i] = -4
            enemyy[i] += enemyy_change[i]
        if enemyx[i] < 0:
            enemyx_change[i] = 4
            enemyy[i] += enemyy_change[i]
        enemy(enemyx[i], enemyy[i], i)

        # Collision
        collision = isCollision(enemyx[i], enemyy[i], bulletx, bullety)
        if collision:
            bullet_sound = mixer.Sound('explosion.wav')
            bullet_sound.play()
            bullety = 500
            bullet_state = "ready"
            score += 1
            enemyx[i] = random.randint(0, 735)
            enemyy[i] = random.randint(50, 150)

    # bullet movement
    if bullety <= 0:
        bullety = 500
        bullet_state = 'ready'
    if bullet_state is "fire":
        fire_bullet(bulletx, bullety)
        bullety -= bullety_change

    # score displayed persistently
    show_score(textx, texty)

    pygame.display.update()  # updating game window(compulsory)
