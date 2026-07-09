import pygame
import random

pygame.init()

# запуск звука
try:
    pygame.mixer.init()
    sound_on = True
except:
    sound_on = False

# экран
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Dino")

clock = pygame.time.Clock()

# цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (255, 0, 0)

font = pygame.font.Font(None, 40)

# звуки 
if sound_on:
    try:
        jump_sound = pygame.mixer.Sound("jump.mp3")
        hit_sound = pygame.mixer.Sound("hit.mp3")
        pygame.mixer.music.load("music.mp3")
        pygame.mixer.music.play(-1)
    except:
        sound_on = False

# игрок
player = pygame.Rect(100, 300, 40, 40)
velocity = 0
jump = False
gravity = 1

# препятствия
obstacles = []

# счёт
score = 0
game_speed = 5
game_over = False
jump_count = 0

# для контроля скорости
last_speed_up = 0

# препятствия
def spawn_obstacle():
    types = [
        {"size": 30, "speed": 7},
        {"size": 50, "speed": 5},
        {"size": 70, "speed": 3}
    ]
    t = random.choice(types)
    rect = pygame.Rect(WIDTH, 340 - t["size"], t["size"], t["size"])
    return {"rect": rect, "speed": t["speed"]}

# стартовое меню
def start_menu():
    waiting = True
    while waiting:
        screen.fill(WHITE)

        text = font.render("Press SPACE to start", True, BLACK)
        screen.blit(text, (250, 180))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

# экран проигрыша
def game_over_screen():
    global score, game_speed, obstacles, player, jump_count, last_speed_up

    waiting = True
    while waiting:
        screen.fill(WHITE)

        text = font.render("Game Over! Press SPACE", True, RED)
        screen.blit(text, (200, 180))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                score = 0
                game_speed = 5
                obstacles.clear()
                player.y = 300
                jump_count = 0
                last_speed_up = 0
                waiting = False

# запуск меню
start_menu()

running = True

while running:

    # очистка экрана
    screen.fill(WHITE)

    # смена фона
    if int(score) >= 100:
        screen.fill(GREEN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not jump and not game_over:
                jump = True
                velocity = -15
                jump_count += 1
                print("Прыжки:", jump_count)
                if sound_on:
                    jump_sound.play()

    if not game_over:

        # прыжок
        if jump:
            player.y += velocity
            velocity += gravity

            if player.y >= 300:
                player.y = 300
                jump = False

        # спавн
        if random.randint(1, 60) == 1:
            obstacles.append(spawn_obstacle())

        # движение
        for obs in obstacles:
            obs["rect"].x -= obs["speed"] + game_speed

            if player.colliderect(obs["rect"]):
                game_over = True
                if sound_on:
                    hit_sound.play()

        # удаление старых
        obstacles = [o for o in obstacles if o["rect"].x > -50]

        # счёт
        score += 0.1

        # увеличение сложности (фикс бага!)
        if int(score) >= last_speed_up + 200:
            game_speed += 1
            last_speed_up = int(score)

    else:
        game_over_screen()
        game_over = False

    # рисуем
    pygame.draw.rect(screen, BLACK, player)

    for obs in obstacles:
        pygame.draw.rect(screen, BLACK, obs["rect"])

    # текст
    score_text = font.render("Score: " + str(int(score)), True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
    