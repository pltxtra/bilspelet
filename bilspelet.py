import sys, pygame
import math
pygame.init()

size = width, height = 1024, 768
black = 0, 0, 0

screen = pygame.display.set_mode(size)

car = pygame.image.load("car.png")
car = pygame.transform.scale2x(car)

MAX_PICS = 48

car_pic = []
car_rct = []
for x in range(0, MAX_PICS):
    rotated = pygame.transform.rotate(car, 360 * (x / MAX_PICS))
    car_pic.append(rotated)
    car_rct.append(rotated.get_rect())

last_time = pygame.time.get_ticks()

pedal_down = False

direction = 0.0
position_x = width / 2.0
position_y = height / 2.0
rotate_left = False
rotate_right = False

car_speed = 0.0
rotate_speed = 200.0

friction = 2.0
acceleration = 1000.0

while 1:
    this_time = pygame.time.get_ticks()
    delta_time = (this_time - last_time) / 1000.0
    last_time = this_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pedal_down = True
            elif event.key == pygame.K_LEFT:
                rotate_left = True
            elif event.key == pygame.K_RIGHT:
                rotate_right = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                pedal_down = False
            elif event.key == pygame.K_LEFT:
                rotate_left = False
            elif event.key == pygame.K_RIGHT:
                rotate_right = False

    if rotate_left:
        direction = direction + rotate_speed * delta_time
    elif rotate_right:
        direction = direction - rotate_speed * delta_time

    if direction >= 360.0:
        direction -= 360.0
    elif direction < 0.0:
        direction += 360

    picture_index = int(direction * MAX_PICS / 360.0)
    angle = (picture_index / MAX_PICS) * 2.0 * math.pi
    if pedal_down:
        car_speed += acceleration * delta_time
    car_speed -= car_speed * friction * delta_time

    if car_speed < 0.0:
        car_speed = 0.0

    position_x = position_x + car_speed * delta_time * math.cos(angle)
    position_y = position_y - car_speed * delta_time * math.sin(angle)

    position = (int(position_x), int(position_y))
    rect = car_rct[picture_index]
    rect.center = position

    screen.fill(black)
    screen.blit(car_pic[picture_index], rect)
    pygame.display.flip()
