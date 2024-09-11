import random

import pygame

pygame.init()

screen = pygame.display.set_mode((900, 700))

clock = pygame.time.Clock()

running = True

car = pygame.rect.Rect(418, 600, 64, 64)

car_change_left = 0

road_centers = [[-1, -1], [450, 625]]

road_width = 300

road_height = 150

road_limits = [400, 500]

player_car = pygame.image.load("assets/blue.png")

road_pic = pygame.image.load("assets/road.png")

red_car = pygame.image.load("assets/red_car.png")

background = pygame.image.load("assets/background2.png")

player_x = 418

player_y = 600

car_rows = []

score_value = 0

score_font = pygame.font.Font("assets/UbuntuMono-Regular.ttf", 32)

spawn_car_pattern = [
    [0, 0, 0],
    [0, 0, 0],
    [1, 1, 0],
    [1, 0, 1],
    [0, 1, 1],
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
]

score_value_final = 0


def place_score():
    score = score_font.render(f"Score:{score_value}", True, (255, 255, 255))
    screen.blit(score, (0, 0))


def Game_over():
    game_over_font = pygame.font.Font("assets/UbuntuMono-Regular.ttf", 150)
    score_font = pygame.font.Font("assets/UbuntuMono-Regular.ttf", 75)
    game_over = game_over_font.render(f"GAME OVER", True, (255, 255, 255))
    score = score_font.render(f"Final Score:{score_value_final}", True, (255, 255, 255))

    screen.fill((0, 0, 0))
    screen.blit(game_over, (150, 0))
    screen.blit(score, (250, 200))


def draw_player(x, y):
    screen.blit(player_car, (x, y))


def spawn_cars_first():
    pattern = random.choice(spawn_car_pattern[4::])

    new_car_center = []

    if pattern[0] == 1:
        new_car_center.append([
            road_centers[-1][0] - 150, -150
        ])

    if pattern[1] == 1:
        new_car_center.append([
            road_centers[-1][0], -150
        ])

    if pattern[2] == 1:
        new_car_center.append([
            road_centers[-1][0] + 150, -150
        ])

    car_rows.append(new_car_center)


def spawn_new_car_row():
    pattern = random.choice(spawn_car_pattern)

    new_car_center = []

    if pattern == [0, 0, 0]:
        pass
    else:
        if pattern[0] == 1:
            new_car_center.append([
                road_centers[-1][0] - 150, -150
            ])

        if pattern[1] == 1:
            new_car_center.append([
                road_centers[-1][0], -150
            ])

        if pattern[2] == 1:
            new_car_center.append([
                road_centers[-1][0] + 150, -150
            ])

        car_rows.append(new_car_center)

    for rows in car_rows[:-1]:
        for center in rows:
            center[1] += road_height

    if car_rows[0][0][1] > 750:
        del car_rows[0]


def create_car(car_centers):
    car_rects = []
    for row in car_rows:
        new_rects = []
        for center in row:
            new_rects.append(
                pygame.rect.Rect(
                    center[0] - 32,
                    center[1] - 32,
                    64,
                    64
                ))
        car_rects.append(new_rects)

    return car_rects


def draw_cars(car_rows, ticks):
    coll = False
    for row in car_rows:
        for car_new in row:

            car_new.bottom += ticks
            pygame.draw.rect(screen, (255, 0, 255), car_new)
            screen.blit(red_car, (car_new.left, car_new.top))

            if (pygame.Rect.colliderect(car, car_new)):
                coll = True

    return coll


def spawn_road(n=1):
    for i in range(n):
        offset = random.randint(0, 12)
        offset = (offset - 6)
        new_center = [
            road_centers[-1][0] + offset,
            road_centers[-1][1] - road_height,
        ]

        if not new_center[0] in range(road_limits[0], road_limits[1] + 1):
            new_center[0] -= 2 * (offset)

        road_centers.append(new_center)

    for center in road_centers:
        center[1] += road_height

    return road_centers[1::]


def create_road(road_centers):
    road_rects = []
    for center in road_centers:
        road_rects.append(pygame.rect.Rect(
            center[0] - road_width // 2,
            center[1] - road_height // 2,
            road_width,
            road_height
        ))
    return road_rects


def draw_road(road, ticks):
    on_road = False
    for road_segment in road:
        road_segment.bottom += ticks
        pygame.draw.rect(screen, (0, 0, 0), road_segment)
        screen.blit(road_pic, (road_segment.left - 64, road_segment.top))
        if (pygame.Rect.colliderect(car, road_segment)):
            on_road = True

    return on_road


def draw_car(pos):
    pygame.draw.rect(screen, (255, 0, 0), car)


road_centers = spawn_road(700 // road_height + 2)

spawn_cars_first()

ticks = 0
ticks_max = 9
coll = False

while running:

    clock.tick(144)

    if (coll):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        Game_over()
    else:

        ticks += min(ticks_max, (score_value / 50) + 2)

        screen.blit(background, (0, 0))

        if ticks >= 150:
            road_centers = spawn_road()
            spawn_new_car_row()
            ticks = 0
            score_value += 1

        coll = (not draw_road(create_road(road_centers), ticks)) or draw_cars(create_car(car_rows), ticks)

        if coll:
            score_value_final = score_value

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    car_change_left = -3

                if event.key == pygame.K_d:
                    car_change_left = 3

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    car_change_left = 0

        car.left += car_change_left

        draw_car([450, 450])

        draw_player(car.left, car.top)

        place_score()

    pygame.display.update()
