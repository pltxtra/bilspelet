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

MAX_PICS = 48

def load_car_picture(filename):
    picture = pygame.image.load(filename)
    picture = pygame.transform.scale2x(picture)
    pic = []
    rct = []
    for x in range(0, MAX_PICS):
        rotated = pygame.transform.rotate(picture, 360 * (x / MAX_PICS))
        pic.append(rotated)
        rct.append(rotated.get_rect())
    return (pic, rct)

last_time = pygame.time.get_ticks()

class Car:
    def __init__(self, filename, start_at_map):
        self.pedal_down = False
        self.direction = 0.0
        self.position_x = start_at_map[0] * 64.0 + 32.0
        self.position_y = start_at_map[1] * 64.0 + 32.0
        self.rotate_left = False
        self.rotate_right = False
        self.speed = 0.0
        self.rotate_speed = 200.0
        self.friction = 2.0
        self.acceleration = 1000.0
        self.lap = 0
        self.checkpoint_ok = True
        self.last_map_position = (0, 0)
        (self.pic, self.rct) = load_car_picture(filename)

def check_events(car):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        else:
            handle_car_event(car, event)

def handle_car_event(car, event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            car.pedal_down = True
        elif event.key == pygame.K_LEFT:
            car.rotate_left = True
        elif event.key == pygame.K_RIGHT:
            car.rotate_right = True
    elif event.type == pygame.KEYUP:
        if event.key == pygame.K_SPACE:
            car.pedal_down = False
        elif event.key == pygame.K_LEFT:
            car.rotate_left = False
        elif event.key == pygame.K_RIGHT:
            car.rotate_right = False

def update_car_direction(car):
    if car.rotate_left:
        car.direction = car.direction + car.rotate_speed * delta_time
    elif car.rotate_right:
        car.direction = car.direction - car.rotate_speed * delta_time

    if car.direction >= 360.0:
        car.direction -= 360.0
    elif car.direction < 0.0:
        car.direction += 360

def update_car_map_position(car):
    car.map_position_x = int(car.position_x / 64.0)
    car.map_position_y = int(car.position_y / 64.0)
    car.map_index = (car.map_position_y * 16 + car.map_position_x) % (len(map))
    car.map_position = (car.map_position_x, car.map_position_y)

def update_car_friction(car):
    map_type = map[car.map_index]
    if map_type == 0 or map_type == 2:
        car.friction = 2.0
    else:
        car.friction = 10.0

def update_lap_position(car):
    if car.checkpoint_ok and (car.map_position in start_position) and (car.last_map_position in goal_position):
        car.lap += 1
        car.checkpoint_ok = False
    elif car.map_position in checkpoint_position:
        car.checkpoint_ok = True
    car.last_map_position = car.map_position

def update_car_speed(car):
    if car.pedal_down:
        car.speed += car.acceleration * delta_time
    car.speed -= car.speed * car.friction * delta_time

    if car.speed < 0.0:
        car.speed = 0.0

def update_car_position(car):
    radians = car.direction * math.pi / 180.0
    car.position_x = car.position_x + car.speed * delta_time * math.cos(radians)
    car.position_y = car.position_y - car.speed * delta_time * math.sin(radians)

    if car.position_x < 0:
        car.position_x = 0
    elif car.position_x > max_x:
        car.position_x = max_x
    if car.position_y < 0:
        car.position_y = 0
    elif car.position_y > max_y:
        car.position_y = max_y

    car.position = (int(car.position_x), int(car.position_y))

def draw_map():
    for y in range(0, 12):
        for x in range(0, 16):
            map_rect.topleft = (x * 64, y * 64)
            screen.blit(map_pieces[map[y * 16 + x]], map_rect)

def draw_car(car):
    picture_index = int(car.direction * MAX_PICS / 360.0)
    rect = car.rct[picture_index]
    rect.center = car.position
    screen.blit(car.pic[picture_index], rect)

def draw_text(car):
    text = font.render("Lap {} / {}".format(car.lap, max_lap), True, (128, 128, 0))
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

max_lap = 3

goal_position = [(7, 8), (7, 9), (7, 10)]
start_position = [(8, 8), (8, 9), (8, 10)]
checkpoint_position = [(7, 1), (7, 2), (7, 3)]

car = Car("car.png", (6, 8))

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
