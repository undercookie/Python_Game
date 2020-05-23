import arcade
import setup
import random

class Room:
    """
    This class holds all the information about the
    different rooms.
    """
    def __init__(self, background_image):
        # You may want many lists. Lists for coins, monsters, etc.
        self.wall_list = arcade.SpriteList()
        self.noCol_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        # This holds the background images. If you don't want changing
        # background images, you can delete this part.
        self.background = arcade.load_texture(background_image)

    def create_wall_sides_trophy_room(self, image):

        for x in (0, setup.SCREEN_WIDTH - setup.SPRITE_SIZE):
            # Loop for each box going across
            for y in range(setup.SPRITE_SIZE, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE, setup.SPRITE_SIZE):
                # Skip making a block 4 and 5 blocks up on the right side
                if y != setup.SPRITE_SIZE * 5 or x == 0:
                    wall = arcade.Sprite(image, setup.SPRITE_SCALING)
                    wall.left = x
                    wall.bottom = y
                    self.wall_list.append(wall)

    def create_wall_top_bottom(self, image):

        for y in (0, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE):
            # Loop for each box going across
            for x in range(0, setup.SCREEN_WIDTH, setup.SPRITE_SIZE):
                wall = arcade.Sprite(image, setup.SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                self.wall_list.append(wall)


    def create_wall_left_right(self, image):

        for x in (0, setup.SCREEN_WIDTH - setup.SPRITE_SIZE):
            # Loop for each box going across
            for y in range(setup.SPRITE_SIZE, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE, setup.SPRITE_SIZE):
                # Skip making a block 5:
                if y != setup.SPRITE_SIZE * 5:
                    wall = arcade.Sprite(image, setup.SPRITE_SCALING)
                    wall.left = x
                    wall.bottom = y
                    self.wall_list.append(wall)

    def create_wall_top_minigame(self, image):

        for y in (0, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE):
            # Loop for each box going across
            for x in range(0, setup.SCREEN_WIDTH, setup.SPRITE_SIZE):
                #skip making two boxes
                if (x != setup.SPRITE_SIZE * 9 and x != setup.SPRITE_SIZE * 10 or y == 0):
                    wall = arcade.Sprite(image, setup.SPRITE_SCALING)
                    wall.left = x
                    wall.bottom = y
                    self.wall_list.append(wall)

    def create_wall_sides_minigame(self, image):
        for x in (0, setup.SCREEN_WIDTH - setup.SPRITE_SIZE):
            # Loop for each box going across
            for y in range(setup.SPRITE_SIZE, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE, setup.SPRITE_SIZE):
                # Skip making a block 4 and 5 blocks up
                if y != setup.SPRITE_SIZE * 5 or x != 0:
                    wall = arcade.Sprite(image, setup.SPRITE_SCALING)
                    wall.left = x
                    wall.bottom = y
                    self.wall_list.append(wall)

    def create_wall_bottom_inside(self, image):

        for y in (0, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE):
            # Loop for each box going across
            for x in range(0, setup.SCREEN_WIDTH, setup.SPRITE_SIZE):
                if (x != setup.SPRITE_SIZE * 9 and x != setup.SPRITE_SIZE * 10) or y != 0:
                    wall = arcade.Sprite(image, setup.SPRITE_SCALING)
                    wall.left = x
                    wall.bottom = y
                    self.wall_list.append(wall)

    def create_wall_sides_inside(self, image):

        for x in (0, setup.SCREEN_WIDTH - setup.SPRITE_SIZE):
            # Loop for each box going across
            for y in range(setup.SPRITE_SIZE, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE, setup.SPRITE_SIZE):
                wall = arcade.Sprite(image, setup.SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                self.wall_list.append(wall)


def setup_room_1():
    room = Room("images/jonas_1.webp")

    #create the walls for the rooms
    room.create_wall_top_bottom("images/jonas_character.PNG")
    room.create_wall_sides_trophy_room("images/jonas_character.PNG")

    return room


def setup_room_2():
    room = Room("images/bg1.png")

    room.create_wall_top_bottom(":resources:images/space_shooter/meteorGrey_big1.png")
    for x in (0, setup.SCREEN_WIDTH - setup.SPRITE_SIZE):
        # Loop for each box going across
        for y in range(setup.SPRITE_SIZE, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE, setup.SPRITE_SIZE):
            # Skip making a block 5:
            if y != setup.SPRITE_SIZE * 5 or x == 0:
                wall = arcade.Sprite(":resources:images/space_shooter/meteorGrey_big1.png", setup.SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)


    wall = arcade.Sprite(":resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png", setup.SPRITE_SCALING)
    wall.left = 8 * setup.SPRITE_SIZE
    wall.bottom = 8 * setup.SPRITE_SIZE
    room.noCol_list.append(wall)

    return room


def setup_room_3():
    room = Room("images/bg2.png")

    room.create_wall_top_minigame(":resources:images/space_shooter/meteorGrey_big1.png")
    room.create_wall_sides_minigame(":resources:images/space_shooter/meteorGrey_big1.png")

    wall = arcade.Sprite(":resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png", setup.SPRITE_SCALING)
    wall.left = 8 * setup.SPRITE_SIZE
    wall.bottom = 8 * setup.SPRITE_SIZE
    room.noCol_list.append(wall)

    return room

def setup_room_4():

    room = Room("images/bg3.png")

    room.create_wall_top_minigame(":resources:images/space_shooter/meteorGrey_big1.png")
    room.create_wall_sides_minigame(":resources:images/space_shooter/meteorGrey_big1.png")

    wall = arcade.Sprite(":resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png", setup.SPRITE_SCALING)
    wall.left = 8 * setup.SPRITE_SIZE
    wall.bottom = 8 * setup.SPRITE_SIZE
    room.noCol_list.append(wall)

    return room


def setup_room_5():

    room = Room("images/bg4.png")

    room.create_wall_top_minigame(":resources:images/space_shooter/meteorGrey_big1.png")
    room.create_wall_sides_minigame(":resources:images/space_shooter/meteorGrey_big1.png")

    wall = arcade.Sprite(":resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png", setup.SPRITE_SCALING)
    wall.left = 8 * setup.SPRITE_SIZE
    wall.bottom = 8 * setup.SPRITE_SIZE
    room.noCol_list.append(wall)

    return room


def setup_room_6():

    room = Room("images/bg5.png")

    room.create_wall_top_minigame(":resources:images/space_shooter/meteorGrey_big1.png")
    room.create_wall_left_right(":resources:images/space_shooter/meteorGrey_big1.png")

    return room

def setup_room_7():

    room = Room("images/bg7.jpg")

    room.create_wall_top_bottom(":resources:images/space_shooter/meteorGrey_big1.png")
    for x in (0, setup.SCREEN_WIDTH - setup.SPRITE_SIZE):
        # Loop for each box going across
        for y in range(setup.SPRITE_SIZE, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE, setup.SPRITE_SIZE):
            # Skip making a block 5:
            if y != setup.SPRITE_SIZE * 5 or y == 0:
                wall = arcade.Sprite(":resources:images/space_shooter/meteorGrey_big1.png", setup.SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)



    return room


def setup_room_8():
    """
    Create and return room 8. The coin room.
    """
    room = Room("images/bg2.png")

    room.create_wall_bottom_inside(":resources:images/space_shooter/meteorGrey_big1.png")
    room.create_wall_sides_inside(":resources:images/space_shooter/meteorGrey_big1.png")


    for i in range(setup.COIN_COUNT):
        # Create the coin instance
        # Coin image from kenney.nl
        coin = arcade.Sprite("images/python-icon-2.png",
                             setup.SPRITE_SCALING_COIN)

        # Position the coin
        coin.center_x = random.randrange(setup.USABLE_ROOM, setup.SCREEN_WIDTH - (setup.USABLE_ROOM))
        coin.center_y = random.randrange(setup.USABLE_ROOM, setup.SCREEN_HEIGHT - (setup.USABLE_ROOM))

        # Add the coin to the lists
        room.coin_list.append(coin)

    return room

def setup_room_9():
    """
    Create and return room 8. The maze.
    """
    room = Room("images/bg3.png")

    for y in (0, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE):
        # Loop for each box going across
        for x in range(0, setup.SCREEN_WIDTH, setup.SPRITE_SIZE):
            if (x != setup.SPRITE_SIZE * 9 and x != setup.SPRITE_SIZE * 10):
                wall = arcade.Sprite(":resources:images/space_shooter/meteorGrey_big1.png", setup.SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)
    room.create_wall_sides_inside(":resources:images/space_shooter/meteorGrey_big1.png")

    y1 = [2, 4, 11, 12, 13, 14, 15]
    y2 = [6, 7, 8, 9, 11, 17]
    y3 = [1, 2, 4, 5, 9, 13, 15, 16, 17]
    y4 = [4, 7, 9, 10, 11, 12, 15, 16]
    y5 = [2, 3, 4, 6, 7, 14, 15, 18]
    y6 = [1, 6, 8, 9, 10, 12, 13, 14, 16, 18]
    y7 = [1, 3, 4, 5, 6, 8, 9, 12, 13, 14]
    y8 = [3, 11, 15, 16, 17]
    y9 = [2, 3, 5, 6, 7, 8, 9, 10, 13, 15, 16, 17, 18]
    y10 = [2, 5, 9, 10, 11, 12]
    y11 = [3, 5, 7, 14, 15, 16, 17]
    y12 = [1, 3, 4, 5, 7, 8, 9, 10, 11, 12, 14, 17]
    y13 = [1, 7, 8, 14, 15]

    y = [y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13]
    status = 1
    for i in range(0, 13, 1):
        for x in y[i]:
            wall = arcade.Sprite(":resources:images/space_shooter/meteorGrey_big2.png", setup.SPRITE_SCALING)
            wall.left = x * setup.SPRITE_SIZE
            wall.bottom = status * setup.SPRITE_SIZE
            room.wall_list.append(wall)
        status += 1

    return room


def setup_room_10():
    """
    Create and return room 10. The coin room.
    """
    room = Room("images/bg4.png")

    room.create_wall_bottom_inside(":resources:images/space_shooter/meteorGrey_big1.png")
    room.create_wall_sides_inside(":resources:images/space_shooter/meteorGrey_big1.png")

    return room


def setup_room_11():
    """
    Create and return room 8. The coin room.
    """
    room = Room("images/bg5.png")

    room.create_wall_bottom_inside(":resources:images/space_shooter/meteorGrey_big1.png")
    room.create_wall_sides_inside(":resources:images/space_shooter/meteorGrey_big1.png")

    return room