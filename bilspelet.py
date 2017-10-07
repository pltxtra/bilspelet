import sys, pygame
import math
pygame.init()
font = pygame.font.Font(None, 72)

size = width, height = 1024, 768
black = 0, 0, 0

screen = pygame.display.set_mode(size)

small_map_pieces = [
    pygame.image.load("black.png"),
    pygame.image.load("green.png"),
    pygame.image.load("checkered.png"),
    ]

map_pieces = []
for small_m in small_map_pieces:
    m = pygame.transform.scale2x(small_m)
    map_pieces.append(m)

map_rect = map_pieces[0].get_rect()

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

class Car:
    def __init__(self):
        self.pedal_down = False
        self.direction = 0.0
        self.position_x = 6.0 * 64.0 + 32.0
        self.position_y = 8.0 * 64.0 + 32.0
        self.rotate_left = False
        self.rotate_right = False
        self.speed = 0.0
        self.rotate_speed = 200.0
        self.friction = 2.0
        self.acceleration = 1000.0
        self.lap = 0
        self.checkpoint_ok = True
        self.last_map_position = (0, 0)

pedal_down = False

direction = 0.0
position_x = 6.0 * 64.0 + 32.0
position_y = 8.0 * 64.0 + 32.0
rotate_left = False
rotate_right = False

car_speed = 0.0
rotate_speed = 200.0

friction = 2.0
acceleration = 1000.0

def check_events(car):
    global pedal_down, rotate_right, rotate_left

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

def update_car_direction(car):
    global direction, rotate_right, rotate_left
    global rotate_speed, delta_time

    if rotate_left:
        direction = direction + rotate_speed * delta_time
    elif rotate_right:
        direction = direction - rotate_speed * delta_time

    if direction >= 360.0:
        direction -= 360.0
    elif direction < 0.0:
        direction += 360

def update_car_map_position(car):
    global map_position_x, map_position_y, map_position, map_index
    map_position_x = int(position_x / 64.0)
    map_position_y = int(position_y / 64.0)
    map_index = (map_position_y * 16 + map_position_x) % (len(map))
    map_position = (map_position_x, map_position_y)

def update_car_friction(car):
    global friction
    map_type = map[map_index]
    if map_type == 0 or map_type == 2:
        friction = 2.0
    else:
        friction = 10.0

def update_lap_position(car):
    global lap, checkpoint_ok, last_map_position
    if checkpoint_ok and (map_position in start_position) and (last_map_position in goal_position):
        lap += 1
        checkpoint_ok = False
    elif map_position in checkpoint_position:
        checkpoint_ok = True
    last_map_position = map_position

def update_car_speed(car):
    global car_speed
    if pedal_down:
        car_speed += acceleration * delta_time
    car_speed -= car_speed * friction * delta_time

    if car_speed < 0.0:
        car_speed = 0.0

def update_car_position(car):
    global position_x, position_y, position
    radians = direction * math.pi / 180.0
    position_x = position_x + car_speed * delta_time * math.cos(radians)
    position_y = position_y - car_speed * delta_time * math.sin(radians)

    if position_x < 0:
        position_x = 0
    elif position_x > max_x:
        position_x = max_x
    if position_y < 0:
        position_y = 0
    elif position_y > max_y:
        position_y = max_y

    position = (int(position_x), int(position_y))

def draw_map():
    for y in range(0, 12):
        for x in range(0, 16):
            map_rect.topleft = (x * 64, y * 64)
            screen.blit(map_pieces[map[y * 16 + x]], map_rect)

def draw_car(car):
    picture_index = int(direction * MAX_PICS / 360.0)
    rect = car_rct[picture_index]
    rect.center = position
    screen.blit(car_pic[picture_index], rect)

def draw_text(car):
    text = font.render("Lap {} / {}".format(lap, max_lap), True, (128, 128, 0))
    screen.blit(text,
                (512 - text.get_width() // 2,
                 384 - text.get_height()))

map = [
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
    1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
    1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,

    1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1,
    1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1,
    1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1,
    1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1,

    1, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 1,
    1, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 1,
    1, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
]

max_x = 16.0 * 64.0
max_y = 12.0 * 64.0

lap = 0
max_lap = 3
checkpoint_ok = True

last_map_position = (0, 0)
goal_position = [(7, 8), (7, 9), (7, 10)]
start_position = [(8, 8), (8, 9), (8, 10)]
checkpoint_position = [(7, 1), (7, 2), (7, 3)]

car = Car()

while 1:
    this_time = pygame.time.get_ticks()
    delta_time = (this_time - last_time) / 1000.0
    last_time = this_time

    check_events(car)
    update_car_direction(car)
    update_car_map_position(car)
    update_car_friction(car)
    update_lap_position(car)
    update_car_speed(car)
    update_car_position(car)

    screen.fill(black)
    draw_map()
    draw_car(car)
    draw_text(car)

    pygame.display.flip()
