import pygame
from pygame.locals import *
import random

pygame.init()

# create the window
width = 500
height = 700
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Car Game")

# colors
gray = (100, 100, 100)
green = (76, 208, 56)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)

# road and marker sizes
road_width = 300
marker_width = 5
marker_height = 40

# lane coordinates
left_lane = 150
center_lane = 250
right_lane = 350
lanes = [left_lane, center_lane, right_lane]

# road and edge markers
road = (100, 0, road_width, height)
left_edge_marker = (95, 0, marker_width, height)
right_edge_marker = (395, 0, marker_width, height)

# for animating movement of the lane markers
lane_marker_move_y = 0

# player's staring coordinates
player_x = 250
player_y = height - 100  # Adjust this value to place the vehicle near the floor

# frame settings
clock = pygame.time.Clock()
fps = 120

# game settings
gameover = False
speed = 2
score = 0

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image, x, y, scale_factor=2):  # Add scale_factor as a parameter
        pygame.sprite.Sprite.__init__(self)

        # Scale the image to fit the screen
        image_scale = (
            45 * scale_factor
        ) / image.get_rect().width  # Adjust the base size by scale_factor
        new_width = int(image.get_rect().width * image_scale)
        new_height = int(image.get_rect().height * image_scale)
        self.image = pygame.transform.scale(image, (new_width, new_height))

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]


class PlayerVehicle(Vehicle):

    def __init__(self, x, y):
        image = pygame.image.load("images/Police.png")
        super().__init__(image, x, y)


# sprite groups
player_group = pygame.sprite.Group()
vehicle_group = pygame.sprite.Group()

# create the player's car
player = PlayerVehicle(player_x, player_y)
player_group.add(player)

# load the vehicle images
image_filenames = [
    "truck.png",
    "Car.png",
    "Ambulance2.png",
    "Police2.png",
    "Black_viper.png",
    "taxi.png",
    "Ambulance.png",
    "Mini_van.png",
    "Audi.png",
    "Mini_truck.png",
]
vehicle_images = []
for image_filename in image_filenames:
    image = pygame.image.load("images/" + image_filename)
    vehicle_images.append(image)

# load the crash image
crash = pygame.image.load("images/crash.png")
crash_rect = crash.get_rect()

# game loop
running = True
while running:

    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        # move the player's car using the left/right arrow keys
        if event.type == KEYDOWN:

            if event.key == K_LEFT and player.rect.center[0] > left_lane:
                player.rect.x -= 100
            elif event.key == K_RIGHT and player.rect.center[0] < right_lane:
                player.rect.x += 100

            # check if there's a side swipe collision after changing lanes
            for vehicle in vehicle_group:
                if pygame.sprite.collide_rect(player, vehicle):

                    gameover = True

                    # place the player's car next to other vehicle
                    # and determine where to position the crash image
                    if event.key == K_LEFT:
                        player.rect.left = vehicle.rect.right
                        crash_rect.center = [
                            player.rect.left,
                            (player.rect.center[1] + vehicle.rect.center[1]) / 2,
                        ]
                    elif event.key == K_RIGHT:
                        player.rect.right = vehicle.rect.left
                        crash_rect.center = [
                            player.rect.right,
                            (player.rect.center[1] + vehicle.rect.center[1]) / 2,
                        ]

    # draw the grass
    screen.fill(green)

    # draw the road
    pygame.draw.rect(screen, gray, road)

    # draw the edge markers
    pygame.draw.rect(screen, yellow, left_edge_marker)
    pygame.draw.rect(screen, yellow, right_edge_marker)

    # draw the lane markers
    lane_marker_move_y += speed * 2
    if lane_marker_move_y >= marker_height * 2:
        lane_marker_move_y = 0
    for y in range(marker_height * -2, height, marker_height * 2):
        pygame.draw.rect(
            screen,
            white,
            (left_lane + 45, y + lane_marker_move_y, marker_width, marker_height),
        )
        pygame.draw.rect(
            screen,
            white,
            (center_lane + 45, y + lane_marker_move_y, marker_width, marker_height),
        )

    # draw the player's car
    player_group.draw(screen)

    # add a vehicle
    if len(vehicle_group) < 2:

        # ensure there's enough gap between vehicles
        add_vehicle = True
        for vehicle in vehicle_group:
            if vehicle.rect.top < vehicle.rect.height * 3:
                add_vehicle = False

        if add_vehicle:

            # select a random lane
            lane = random.choice(lanes)

            # select a random vehicle image
            image = random.choice(vehicle_images)
            vehicle = Vehicle(image, lane, height / -2)
            vehicle_group.add(vehicle)

    # make the vehicles move
    for vehicle in vehicle_group:
        vehicle.rect.y += speed

        # remove vehicle once it goes off screen
        if vehicle.rect.top >= height:
            vehicle.kill()

            # add to score
            score += 1

            # speed up the game after passing 4 vehicles
            if score > 0 and score % 5 == 0:
                speed += 0.5

    # draw the vehicles
    vehicle_group.draw(screen)

    # display the score
    font = pygame.font.Font(pygame.font.get_default_font(), 18)
    game_over_text = font.render("Score: " + str(score), True, white)
    text_rect = game_over_text.get_rect()
    text_rect.center = (40, 100)
    screen.blit(game_over_text, text_rect)

    # check if there's a head on collision
    if pygame.sprite.spritecollide(player, vehicle_group, True):
        gameover = True
        crash_rect.center = [player.rect.center[0], player.rect.top]

    # display game over
    if gameover:
        screen.blit(crash, crash_rect)

        pygame.draw.rect(screen, red, (0, height // 2 - 50, width, 100))

        font = pygame.font.Font(pygame.font.get_default_font(), 20)

        game_over_text = font.render(
            "Game over.Play again? (Enter Y or N).", True, white
        )
        text_rect = game_over_text.get_rect()

        text_rect.center = (width / 2, height // 2 - 20)
        screen.blit(game_over_text, text_rect)

        # Render the current score
        score_text = font.render(
            f"Score: {score}", True, white
        )  # Display the current score
        score_rect = score_text.get_rect()
        score_rect.center = (
            width / 2,
            height // 2 + 20,
        )  # Position it slightly below the game over game_over_text
        screen.blit(score_text, score_rect)

    pygame.display.update()

    # wait for user's input to play again or exit
    while gameover:

        clock.tick(fps)

        for event in pygame.event.get():

            if event.type == QUIT:
                gameover = False
                running = False

            # get the user's input (y or n)
            if event.type == KEYDOWN:
                if event.key == K_y:
                    # reset the game
                    gameover = False
                    speed = 2
                    score = 0
                    vehicle_group.empty()
                    player.rect.center = [player_x, player_y]
                elif event.key == K_n:
                    # exit the loops
                    gameover = False
                    running = False

pygame.quit()
