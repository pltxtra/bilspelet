import sys, pygame
pygame.init()

size = width, height = 1024, 768
black = 0, 0, 0

screen = pygame.display.set_mode(size)

car = pygame.image.load("car.png")
car = pygame.transform.scale2x(car)
rect = car.get_rect()

pedal_down = False

position_x = width / 2.0
position_y = height / 2.0

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pedal_down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                pedal_down = False

    if pedal_down:
        position_y = position_y - 1

    position = (int(position_x), int(position_y))
    rect.center = position

    screen.fill(black)
    screen.blit(car, rect)
    pygame.display.flip()
