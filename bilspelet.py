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
    def __init__(self, filename, start_at_map, gas_key, left_key, right_key):
        self.start_at_map = start_at_map
        self.gas_key = gas_key
        self.left_key = left_key
        self.right_key = right_key
        (self.pic, self.rct) = load_car_picture(filename)

        restart_car(self)

def restart_car(car):
    car.pedal_down = False
    car.direction = 0.0
    car.position_x = car.start_at_map[0] * 64.0 + 32.0
    car.position_y = car.start_at_map[1] * 64.0 + 32.0
    car.rotate_left = False
    car.rotate_right = False
    car.speed = 0.0
    car.rotate_speed = 200.0
    car.friction = 2.0
    car.acceleration = 1000.0
    car.lap = 0
    car.checkpoint_ok = True
    car.last_map_position = (0, 0)

def start_game():
    global game_mode, time_to_race, winner, game_time
    game_mode = 1
    time_to_race = 3.0
    game_time = 0.0
    winner = None
    for car in cars:
        restart_car(car)

def check_events(events):
    global game_mode
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_mode == 3:
                start_game()

def handle_car_events(car, events):
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == car.gas_key:
                car.pedal_down = True
            elif event.key == car.left_key:
                car.rotate_left = True
            elif event.key == car.right_key:
                car.rotate_right = True
        elif event.type == pygame.KEYUP:
            if event.key == car.gas_key:
                car.pedal_down = False
            elif event.key == car.left_key:
                car.rotate_left = False
            elif event.key == car.right_key:
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

def draw_text(car, offset):
    text = font.render("Lap {} / {}".format(car.lap, max_lap), True, (128, 128, 0))
    screen.blit(text,
                (512 - text.get_width() // 2,
                 384 + text.get_height() * offset + 10 * offset))

def handle_simulation(car):
    update_car_direction(car)
    update_car_map_position(car)
    update_car_friction(car)
    update_lap_position(car)
    update_car_speed(car)
    update_car_position(car)

def draw_main_game():
    global winner, game_mode, start_timer, game_time
    offset = 0
    game_time += delta_time
    for car in cars:
        handle_car_events(car, events)
        handle_simulation(car)
        draw_car(car)
        draw_text(car, offset)
        offset += 1

        if car.lap > max_lap:
            winner = car
            game_mode = 2
            start_timer = 5.0

    if winner:
        for car in cars:
            car.pedal_down = False
            car.rotate_left = False
            car.rotate_right = False

    text = font.render("{:.2f}s".format(game_time), True, (128, 128, 0))
    screen.blit(text,
                (512,
                 384 - text.get_height()))


def draw_countdown():
    global game_mode, time_to_race

    for car in cars:
        handle_simulation(car)
        draw_car(car)

    time_to_race -= delta_time

    text = font.render("Start in {}...".format(int(time_to_race) + 1), True, (128, 128, 0))
    screen.blit(text,
                (512 - text.get_width() // 2,
                 384 - text.get_height()))

    if time_to_race <= 0.0:
        game_mode = 0

def draw_winner():
    global game_mode, start_timer

    if start_timer < 0.0:
        game_mode = 3
    start_timer -= delta_time

    offset = 0
    for car in cars:
        offset += 1
        update_car_direction(car)
        update_car_map_position(car)
        update_car_friction(car)
        update_lap_position(car)
        update_car_speed(car)
        update_car_position(car)
        draw_car(car)

        if car == winner:
            text = font.render("Player {} won!".format(offset), True, (128, 128, 0))
            screen.blit(text,
                        (512 - text.get_width() // 2,
                         384 - text.get_height()))

def draw_start_screen():
    global game_mode, time_to_race

    for car in cars:
        handle_simulation(car)
        draw_car(car)

    text = font.render("Press SPACE", True, (128, 128, 0))
    screen.blit(text,
                (512 - text.get_width() // 2,
                 384 - text.get_height()))
    text = font.render("to START!", True, (128, 128, 0))
    screen.blit(text,
                (512 - text.get_width() // 2,
                 384))


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

cars = [
    Car("car.png", (6, 8), pygame.K_RCTRL, pygame.K_LEFT, pygame.K_RIGHT),
    Car("car_2.png", (6, 9), pygame.K_LCTRL, pygame.K_q, pygame.K_e),
    ]

game_mode = 3
time_to_race = 3.0
winner = None

while 1:
    this_time = pygame.time.get_ticks()
    delta_time = (this_time - last_time) / 1000.0
    last_time = this_time

    events = pygame.event.get()
    check_events(events)

    screen.fill(black)
    draw_map()

    if game_mode == 0:
        draw_main_game()
    elif game_mode == 1:
        draw_countdown()
    elif game_mode == 2:
        draw_winner()
    elif game_mode == 3:
        draw_start_screen()

    pygame.display.flip()
