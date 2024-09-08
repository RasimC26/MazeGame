"""

#Author: Rasim Crnica
#Date: December 1st, 2023
#Course: CS 1400, University of Utah, Kahlert School of Computing
#Copyright: CS 1400 and [Rasim Crnica] - This work may not
#            be copied for use in Academic Coursework.
#
# I, [Rasim Crnica], certify that I wrote this code from scratch and
# did not copy it in part or whole from another source.
#
#    This file contains the code for a game in which you control a character named Donald, Donald has to
     Go through 3 levels, each with different mazes, random bananas with a random feature, different traps and different amount dodgeballs that go throught the maze.
     If Donald touches either the maze wall orthe dodgeball(s), the game ends. If Donald gets the key, he proceeds to the next
     level, if he gets all the keys, he wins.
"""


import sys, pygame
from pygame import Vector2


def pixel_collision(game_objects, item1, item2):
    pos1 = game_objects[item1]["pos"]
    pos2 = game_objects[item2]["pos"]
    mask1 = game_objects[item1]["mask"]
    mask2 = game_objects[item2]["mask"]

    pos1_temp = pos1 - Vector2(mask1.get_size()) / 2
    pos2_temp = pos2 - Vector2(mask2.get_size()) / 2
    offset = pos2_temp - pos1_temp

    overlap = mask1.overlap(mask2, offset)
    return overlap is not None


def draw_image_centered(screen, image, pos):
    containing_rectangle = image.get_rect()
    screen.blit(image, (pos.x - containing_rectangle.width / 2, pos.y - containing_rectangle.height / 2))


def add_game_object(game_objects, name, width, height, x, y):
    information = {}
    game_objects[name] = information

    image = pygame.image.load("images/" + name + ".png")
    information["name"] = name
    information["pos"] = Vector2(x, y)
    information["image"] = pygame.transform.smoothscale(image, (width, height))
    information["size"] = Vector2(width, height)
    information["mask"] = pygame.mask.from_surface(information["image"])
    information["visible"] = True

def level_1():
    """
        First level of the game.

        This function initializes and runs the first level of the game, where the player controls "Donald" to
        navigate through a maze without touching the walls and must avoid the dodgeball that goes through the map and collect a key
        to proceed to the next level, there is a trap that kills you. If Donald touches the maze walls or the dodgeball the game ends.
        A banana helps to slow down the ball.

        Args:
            None

        Returns:
            None
        """

    level_functions = [level_1, level_2, level_3]  # Add more level functions if needed
    max_level = len(level_functions) - 1
    current_level = 0

    game_objects = {}

    add_game_object(game_objects, "Donald", 40, 40, 20, 335)
    add_game_object(game_objects, "key", 30, 30, 780, 270)
    add_game_object(game_objects, "dodgeball", 150, 150, 400, 300)
    add_game_object(game_objects, "trap", 125, 125, 550, 470)
    add_game_object(game_objects, "Banana", 60, 60, 640, 250)
    add_game_object(game_objects, "map1", width=800, height=600, x=400, y=300)


    width = 800
    height = 600




    screen = pygame.display.set_mode(game_objects["map1"]["image"].get_size())




    # Different font sizes
    myfont = pygame.font.Font("ka1.ttf", 50)
    myfont1 = pygame.font.Font("ka1.ttf", 25)
    myfont2 = pygame.font.Font("ka1.ttf", 10)

    is_playing = True

    key_found = False

    game_started = False

    speed_of_dodgeball = 5  # Initialize the speed outside the game loop

    while is_playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_playing = False


        screen.fill((255,255,255))


        # Controls how Donald gets moved
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            game_objects["Donald"]["pos"] += Vector2(-5, 0)
        if keys[pygame.K_RIGHT]:
            game_objects["Donald"]["pos"] += Vector2(5, 0)
        if keys[pygame.K_UP]:
            game_objects["Donald"]["pos"] += Vector2(0, -5)
        if keys[pygame.K_DOWN]:
            game_objects["Donald"]["pos"] += Vector2(0, 5)




        #Displays messages before the game starts
        if not game_started:
            label = myfont1.render("Move to Start!", True, (0, 0, 0))
            screen.blit(label, (500, 20))
            label = myfont1.render("Level 1", True, (0, 0, 0))
            screen.blit(label, (40, 20))


            label = myfont2.render("Get The Key To Proceed!", True, (0, 0, 0))
            screen.blit(label, (40, 480))


        #If you move the game starts
        if not game_started and (
                keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
            game_started = True


        #Makes it so Donald cant go past the screen
        donald_pos = game_objects["Donald"]["pos"]
        donald_pos.x = max(0, min(donald_pos.x, width))
        donald_pos.y = max(0, min(donald_pos.y, height))

        #Makes it so the dodgeball cant go past the screen
        dodgeball_pos = game_objects["dodgeball"]["pos"]
        dodgeball_pos.x = max(0, min(dodgeball_pos.x, width))
        dodgeball_pos.y = max(0, min(dodgeball_pos.y, height))

        # Move the "dodgeball" object
        if game_started:
            dodgeball_pos += Vector2(speed_of_dodgeball, 0)

        # Bounce off the right and left walls
        if game_started and dodgeball_pos.x + game_objects["dodgeball"]["size"].x / 2 >= width or dodgeball_pos.x - \
                game_objects["dodgeball"]["size"].x / 2 <= 0:
            speed_of_dodgeball *= -1  # Reverse the direction

        # Draw the "dodgeball" object
        draw_image_centered(screen, game_objects["dodgeball"]["image"], dodgeball_pos)

        for object in game_objects.values():
            if object["visible"]:
                draw_image_centered(screen, object["image"], object["pos"])

        if not key_found and pixel_collision(game_objects, "Donald", "key"):
            game_objects["key"]["visible"] = False
            key_found = True
            pygame.time.delay(1000)
            current_level += 1
            if current_level > max_level:  # Check if all levels are completed
                is_playing = False
            else:
                # Load the next level
                level_functions[current_level]()


        if pixel_collision(game_objects, "Donald", "dodgeball"):
            is_alive = False
            pygame.time.delay(3000)
            is_playing = False


        if pixel_collision(game_objects, "Donald", "trap"):
            is_alive = False
            pygame.time.delay(3000)
            is_playing = False



        if pixel_collision(game_objects, "Donald", "Banana"):
            speed_of_dodgeball *= .9
            game_objects["Banana"]["visible"] = False




        if pixel_collision(game_objects, "Donald", "map1"):
            is_alive = False
            is_playing = False



        pygame.display.flip()
        pygame.time.Clock().tick(30)

    pygame.quit()
    sys.exit()

def level_2():
    """
            Second level of the game.

            This function initializes and runs the second level of the game, where the player controls "Donald" to
            navigate through a different maze without touching the walls and must avoid more dodgeballs that goes through the map and collect a key
            to proceed to the next level. If Donald touches the maze walls or the dodgeball or the trap the game ends. The banana
            teleports you to the end

            Args:
                None

            Returns:
                None
            """


    level_functions = [level_1, level_2, level_3]  # Add more level functions if needed
    max_level = len(level_functions) - 1
    current_level = 1

    game_objects = {}

    add_game_object(game_objects, "Donald", 25, 25, 345, 15)
    add_game_object(game_objects, "key", 25, 25, 555, 585)
    add_game_object(game_objects, "dodgeball", 125, 125, 150, 300)
    add_game_object(game_objects, "dodgeball2", 125, 125, 400, 300)
    add_game_object(game_objects, "dodgeball3", 125, 125, 650, 300)
    add_game_object(game_objects, "trap", 70, 70, 550, 200)
    add_game_object(game_objects, "Banana", 30, 30, 760, 35)
    add_game_object(game_objects, "map2", width=800, height=600, x=400, y=300)

    width = 800
    height = 600

    screen = pygame.display.set_mode(game_objects["map2"]["image"].get_size())

    # Different font sizes
    myfont = pygame.font.Font("ka1.ttf", 50)
    myfont2 = pygame.font.Font("ka1.ttf", 50)
    myfont1 = pygame.font.Font("ka1.ttf", 25)

    is_playing = True

    key_found = False

    game_started = False

    speed_of_dodgeball = 7  # Initialize the speed outside the game loop

    while is_playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_playing = False

        screen.fill((255,255,255))

        #Keys to control Donalds movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            game_objects["Donald"]["pos"] += Vector2(-5, 0)
        if keys[pygame.K_RIGHT]:
            game_objects["Donald"]["pos"] += Vector2(5, 0)
        if keys[pygame.K_UP]:
            game_objects["Donald"]["pos"] += Vector2(0, -5)
        if keys[pygame.K_DOWN]:
            game_objects["Donald"]["pos"] += Vector2(0, 5)

        #Messages displayed before the game starts
        if not game_started:
            label = myfont1.render("Move to Start!", True, (0, 0, 0))
            screen.blit(label, (450, 20))
            label = myfont1.render("Level 2", True, (0, 0, 0))
            screen.blit(label, (10, 20))



        #Move to start game
        if not game_started and (
                keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
            game_started = True


        #Makes it so Donald cant leave the map border
        donald_pos = game_objects["Donald"]["pos"]
        donald_pos.x = max(0, min(donald_pos.x, width))
        donald_pos.y = max(0, min(donald_pos.y, height))

        # Makes it so the dodgeballs cant leave the map border
        dodgeball_pos = game_objects["dodgeball"]["pos"]
        dodgeball_pos.x = max(0, min(dodgeball_pos.x, width))
        dodgeball_pos.y = max(0, min(dodgeball_pos.y, height))

        # Makes it so the dodgeballs cant leave the map border
        dodgeball2_pos = game_objects["dodgeball2"]["pos"]
        dodgeball2_pos.x = max(0, min(dodgeball2_pos.x, width))
        dodgeball2_pos.y = max(0, min(dodgeball2_pos.y, height))

        # Makes it so the dodgeballs cant leave the map border
        dodgeball3_pos = game_objects["dodgeball3"]["pos"]
        dodgeball3_pos.x = max(0, min(dodgeball3_pos.x, width))
        dodgeball3_pos.y = max(0, min(dodgeball3_pos.y, height))

        # Move the "dodgeball" object
        if game_started:
            dodgeball_pos -= Vector2(0, speed_of_dodgeball)
            dodgeball2_pos += Vector2(0, speed_of_dodgeball)
            dodgeball3_pos -= Vector2(0, speed_of_dodgeball)

        # Bounce off the top and bottom walls
        if dodgeball_pos.y + game_objects["dodgeball"]["size"].y / 2 >= height or dodgeball_pos.y - \
                game_objects["dodgeball"]["size"].y / 2 <= 0:
            speed_of_dodgeball *= -1  # Reverse the direction

        # Draw the "dodgeball" object
        draw_image_centered(screen, game_objects["dodgeball"]["image"], dodgeball_pos)

        for object in game_objects.values():
            if object["visible"]:
                draw_image_centered(screen, object["image"], object["pos"])

        if not key_found and pixel_collision(game_objects, "Donald", "key"):
            game_objects["key"]["visible"] = False
            key_found = True
            pygame.time.delay(1000)
            current_level += 1
            if current_level > max_level:  # Check if all levels are completed
                is_playing = False
            else:
                # Load the next level
                level_functions[current_level]()

        if pixel_collision(game_objects, "Donald", "trap"):
            is_alive = False
            pygame.time.delay(3000)
            is_playing = False

        if pixel_collision(game_objects, "Donald", "Banana"):
            donald_pos.x = (500)
            donald_pos.y = (568)
            game_objects["Banana"]["visible"] = False

        if pixel_collision(game_objects, "Donald", "dodgeball"):
            is_alive = False
            pygame.time.delay(3000)
            is_playing = False

        if pixel_collision(game_objects, "Donald", "dodgeball2"):
            is_alive = False
            pygame.time.delay(3000)
            is_playing = False

        if pixel_collision(game_objects, "Donald", "dodgeball3"):
            is_alive = False
            pygame.time.delay(3000)
            is_playing = False

        if pixel_collision(game_objects, "Donald", "map2"):
            is_alive = False
            pygame.time.delay(3000)
            is_playing = False

        pygame.display.flip()
        pygame.time.Clock().tick(30)

    pygame.quit()
    sys.exit()

def level_3():
    """
                Third level of the game.

                This function initializes and runs the third level of the game, where the player controls "Donald" to
                navigate through a different maze without touching the walls and  avoid even more dodgeballs that goes through the map and collect a key
                to proceed to the next level. If Donald touches the maze walls or the dodgeball the game ends.

                Args:
                    None

                Returns:
                    None
                """


    level_functions = [level_1, level_2, level_3]  # Add more level functions if needed
    max_level = len(level_functions) - 1
    current_level = 2

    game_objects = {}

    add_game_object(game_objects, "Donald", 25, 25, 20, 20)
    add_game_object(game_objects, "key", 20, 20, 565, 500)
    add_game_object(game_objects, "dodgeball", 100, 100, 100, 300)
    add_game_object(game_objects, "dodgeball2", 100, 100, 225, 300)
    add_game_object(game_objects, "dodgeball3", 100, 100, 340, 300)
    add_game_object(game_objects, "dodgeball4", 100, 100, 460, 300)
    add_game_object(game_objects, "dodgeball5", 100, 100, 575, 300)
    add_game_object(game_objects, "dodgeball6", 100, 100, 700, 300)
    add_game_object(game_objects, "trap", 70, 70, 700, 15)
    add_game_object(game_objects, "map3", width=800, height=600, x=400, y=300)

    width = 800
    height = 600

    screen = pygame.display.set_mode(game_objects["map3"]["image"].get_size())

    #Different font sizes
    myfont = pygame.font.Font("ka1.ttf", 50)
    myfont2 = pygame.font.Font("ka1.ttf", 50)
    myfont1 = pygame.font.Font("ka1.ttf", 25)

    is_playing = True

    key_found = False

    game_started = False

    speed_of_dodgeball = 7  # Initialize the speed outside the game loop

    while is_playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_playing = False

        screen.fill((255, 255, 255))

        #Controls to move Donald
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            game_objects["Donald"]["pos"] += Vector2(-5, 0)
        if keys[pygame.K_RIGHT]:
            game_objects["Donald"]["pos"] += Vector2(5, 0)
        if keys[pygame.K_UP]:
            game_objects["Donald"]["pos"] += Vector2(0, -5)
        if keys[pygame.K_DOWN]:
            game_objects["Donald"]["pos"] += Vector2(0, 5)

        #Text displayed before the game starts
        if not game_started:
            label = myfont1.render("Move to Start!", True, (0, 0, 0))
            screen.blit(label, (50, 5))
            label = myfont1.render("Level 3", True, (0, 0, 0))
            screen.blit(label, (350, 40))



        #Move to start the game
        if not game_started and (
                keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
            game_started = True


        #Makes it so Donald cant leave the screen border
        donald_pos = game_objects["Donald"]["pos"]
        donald_pos.x = max(0, min(donald_pos.x, width))
        donald_pos.y = max(0, min(donald_pos.y, height))

        # Makes it so the dodgeball cant leave the screen border
        dodgeball_pos = game_objects["dodgeball"]["pos"]
        dodgeball_pos.x = max(0, min(dodgeball_pos.x, width))
        dodgeball_pos.y = max(0, min(dodgeball_pos.y, height))

        # Makes it so the dodgeball cant leave the screen border
        dodgeball2_pos = game_objects["dodgeball2"]["pos"]
        dodgeball2_pos.x = max(0, min(dodgeball2_pos.x, width))
        dodgeball2_pos.y = max(0, min(dodgeball2_pos.y, height))

        # Makes it so the dodgeball cant leave the screen border
        dodgeball3_pos = game_objects["dodgeball3"]["pos"]
        dodgeball3_pos.x = max(0, min(dodgeball3_pos.x, width))
        dodgeball3_pos.y = max(0, min(dodgeball3_pos.y, height))

        # Makes it so the dodgeball cant leave the screen border
        dodgeball4_pos = game_objects["dodgeball4"]["pos"]
        dodgeball4_pos.x = max(0, min(dodgeball4_pos.x, width))
        dodgeball4_pos.y = max(0, min(dodgeball4_pos.y, height))

        # Makes it so the dodgeball cant leave the screen border
        dodgeball5_pos = game_objects["dodgeball5"]["pos"]
        dodgeball5_pos.x = max(0, min(dodgeball5_pos.x, width))
        dodgeball5_pos.y = max(0, min(dodgeball5_pos.y, height))

        # Makes it so the dodgeball cant leave the screen border
        dodgeball6_pos = game_objects["dodgeball6"]["pos"]
        dodgeball6_pos.x = max(0, min(dodgeball6_pos.x, width))
        dodgeball6_pos.y = max(0, min(dodgeball6_pos.y, height))

        # Move the "dodgeball" object
        if game_started:
            dodgeball_pos -= Vector2(0, speed_of_dodgeball)
            dodgeball2_pos += Vector2(0, speed_of_dodgeball)
            dodgeball3_pos -= Vector2(0, speed_of_dodgeball)
            dodgeball4_pos += Vector2(0, speed_of_dodgeball)
            dodgeball5_pos -= Vector2(0, speed_of_dodgeball)
            dodgeball6_pos += Vector2(0, speed_of_dodgeball)

        # Bounce off the top and bottom walls
        if dodgeball_pos.y + game_objects["dodgeball"]["size"].y / 2 >= height or dodgeball_pos.y - \
                game_objects["dodgeball"]["size"].y / 2 <= 0:
            speed_of_dodgeball *= -1  # Reverse the direction

        # Draw the "dodgeball" object
        draw_image_centered(screen, game_objects["dodgeball"]["image"], dodgeball_pos)

        for object in game_objects.values():
            if object["visible"]:
                draw_image_centered(screen, object["image"], object["pos"])


        #Touch the key to proceed to the next level
        if not key_found and pixel_collision(game_objects, "Donald", "key"):
            game_objects["key"]["visible"] = False
            label = myfont.render("You Won The Game Yo!", True, (0, 0, 0))
            screen.blit(label, (50, 20))
            key_found = True
            pygame.display.flip()  # Display the message immediately
            pygame.time.delay(3000)
            current_level += 1
            if current_level > max_level:  # Check if all levels are completed
                is_playing = False
            else:
                 # Load the next level
                level_functions[current_level]()

        if pixel_collision(game_objects, "Donald", "trap"):
            is_alive = False
            pygame.time.delay(3000)
            is_playing = False


        #If you touch the dodgeball, the game ends
        if pixel_collision(game_objects, "Donald", "dodgeball"):
            is_alive = False
            pygame.time.delay(3000)
            is_playing = False

        # If you touch the dodgeball, the game ends
        if pixel_collision(game_objects, "Donald", "dodgeball2"):
            is_alive = False
            pygame.time.delay(3000)
            is_playing = False

        # If you touch the dodgeball, the game ends
        if pixel_collision(game_objects, "Donald", "dodgeball3"):
            is_alive = False
            pygame.time.delay(3000)
            is_playing = False

        # If you touch the dodgeball, the game ends
        if pixel_collision(game_objects, "Donald", "dodgeball4"):
            is_alive = False
            pygame.time.delay(3000)
            is_playing = False

        # If you touch the dodgeball, the game ends
        if pixel_collision(game_objects, "Donald", "dodgeball5"):
            is_alive = False
            pygame.time.delay(3000)
            is_playing = False

        # If you touch the dodgeball, the game ends
        if pixel_collision(game_objects, "Donald", "dodgeball6"):
            is_alive = False
            pygame.time.delay(3000)
            is_playing = False

        # If you touch the maze walls, the game ends
        if pixel_collision(game_objects, "Donald", "map3"):
            is_alive = False
            pygame.time.delay(3000)
            is_playing = False

        pygame.display.flip()
        pygame.time.Clock().tick(30)

    pygame.quit()
    sys.exit()





def main():
    pygame.init()


    level_1()






if __name__ == "__main__":
    main()