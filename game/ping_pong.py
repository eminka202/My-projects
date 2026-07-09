import pygame

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пинг Понг")

WHITE = (255,255,255)
BLUE = (0,100,255)

player1 = pygame.Rect(50,150,20,100)
player2 = pygame.Rect(530,150,20,100)

PLAYER_SPEED = 5

# счет
score1 = 0
score2 = 0

# шрифт
font = pygame.font.SysFont(None,40)

# класс мяча
class Ball:
    def __init__(self,x,y,size):
        self.rect = pygame.Rect(x,y,size,size)
        self.speed_x = 4
        self.speed_y = 4

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def draw(self,screen):
        pygame.draw.ellipse(screen,WHITE,self.rect)

    def reset(self):
        self.rect.center = (WIDTH//2, HEIGHT//2)
        self.speed_x = 4
        self.speed_y = 4


# мяч
ball = Ball(290,190,20)

# цикл игры
clock = pygame.time.Clock()
run = True

while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    # управление игроками
    if keys[pygame.K_UP] and player1.top > 0:
        player1.y -= PLAYER_SPEED
    if keys[pygame.K_DOWN] and player1.bottom < HEIGHT:
        player1.y += PLAYER_SPEED

    if keys[pygame.K_w] and player2.top > 0:
        player2.y -= PLAYER_SPEED
    if keys[pygame.K_s] and player2.bottom < HEIGHT:
        player2.y += PLAYER_SPEED


    # движение мяча
    ball.move()

    # столкновение со стенами
    if ball.rect.top <= 0 or ball.rect.bottom >= HEIGHT:
        ball.speed_y *= -1


    # столкновение с игроками + ускорение
    if ball.rect.colliderect(player1) or ball.rect.colliderect(player2):
        ball.speed_x *= -1.2


    # гол
    if ball.rect.left <= 0:
        score2 += 1
        ball.reset()

    if ball.rect.right >= WIDTH:
        score1 += 1
        ball.reset()


    # рисуем
    screen.fill(BLUE)

    pygame.draw.rect(screen,WHITE,player1)
    pygame.draw.rect(screen,WHITE,player2)

    ball.draw(screen)

    # счет
    score_text = font.render(str(score1) + " : " + str(score2),True,WHITE)
    screen.blit(score_text,(270,20))

    pygame.display.update()
    clock.tick(60)

pygame.quit()