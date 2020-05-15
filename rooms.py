import arcade
import setup
import random

class Room:
    """
    This class holds all the information about the
    different rooms.
    """
    def __init__(self):
        # You may want many lists. Lists for coins, monsters, etc.
        self.wall_list = None

        # This holds the background images. If you don't want changing
        # background images, you can delete this part.
        self.background = None


def setup_room_1():
    """
    Create and return room 1.
    If your program gets large, you may want to separate this into different
    files.
    """
    room = Room()

    """ Set up the game and initialize the variables. """
    # Sprite lists
    room.wall_list = arcade.SpriteList()
    room.noCol_list = arcade.SpriteList()
    room.coin_list = arcade.SpriteList()

    # -- Set up the walls
    # Create bottom and top row of boxes
    # This y loops a list of two, the coordinate 0, and just under the top of window
    for y in (0, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE):
        # Loop for each box going across
        for x in range(0, setup.SCREEN_WIDTH, setup.SPRITE_SIZE):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", setup.SPRITE_SCALING)
            wall.left = x
            wall.bottom = y
            room.wall_list.append(wall)

    # Create left and right column of boxes
    for x in (0, setup.SCREEN_WIDTH - setup.SPRITE_SIZE):
        # Loop for each box going across
        for y in range(setup.SPRITE_SIZE, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE, setup.SPRITE_SIZE):
            # Skip making a block 4 and 5 blocks up on the right side
            if (y != setup.SPRITE_SIZE * 4 and y != setup.SPRITE_SIZE * 5) or x == 0:
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", setup.SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)


    # Load the background image for this level.
    room.background = arcade.load_texture(":resources:images/backgrounds/abstract_1.jpg")

    return room


def setup_room_2():
    """
    Create and return room 2.
    """
    room = Room()

    """ Set up the game and initialize the variables. """
    # Sprite lists
    room.wall_list = arcade.SpriteList()
    room.noCol_list = arcade.SpriteList()
    room.coin_list = arcade.SpriteList()

    # -- Set up the walls
    # Create bottom and top row of boxes
    # This y loops a list of two, the coordinate 0, and just under the top of window
    for y in (0, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE):
        # Loop for each box going across
        for x in range(0, setup.SCREEN_WIDTH, setup.SPRITE_SIZE):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", setup.SPRITE_SCALING)
            wall.left = x
            wall.bottom = y
            room.wall_list.append(wall)

    # Create left and right column of boxes
    for x in (0, setup.SCREEN_WIDTH - setup.SPRITE_SIZE):
        # Loop for each box going across
        for y in range(setup.SPRITE_SIZE, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE, setup.SPRITE_SIZE):
            # Skip making a block 4 and 5 blocks up
            if (y != setup.SPRITE_SIZE * 4 and y != setup.SPRITE_SIZE * 5):
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", setup.SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)


    wall = arcade.Sprite(":resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png", setup.SPRITE_SCALING)
    wall.left = 8 * setup.SPRITE_SIZE
    wall.bottom = 8 * setup.SPRITE_SIZE
    room.wall_list.append(wall)
    room.background = arcade.load_texture(":resources:images/backgrounds/abstract_2.jpg")

    return room


def setup_room_3():
    """
    Create and return room 3.
    """
    room = Room()

    """ Set up the game and initialize the variables. """
    # Sprite lists
    room.wall_list = arcade.SpriteList()
    room.noCol_list = arcade.SpriteList()
    room.coin_list = arcade.SpriteList()

    # -- Set up the walls
    # Create bottom and top row of boxes
    # This y loops a list of two, the coordinate 0, and just under the top of window
    for y in (0, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE):
        # Loop for each box going across
        for x in range(0, setup.SCREEN_WIDTH, setup.SPRITE_SIZE):
            if (x != setup.SPRITE_SIZE * 9 and x != setup.SPRITE_SIZE * 10 or y == 0):
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", setup.SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    # Create left and right column of boxes
    for x in (0, setup.SCREEN_WIDTH - setup.SPRITE_SIZE):
        # Loop for each box going across
        for y in range(setup.SPRITE_SIZE, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE, setup.SPRITE_SIZE):
            # Skip making a block 4 and 5 blocks up
            if (y != setup.SPRITE_SIZE * 4 and y != setup.SPRITE_SIZE * 5):
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", setup.SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", setup.SPRITE_SCALING)
    wall.left = 5 * setup.SPRITE_SIZE
    wall.bottom = 6 * setup.SPRITE_SIZE
    room.noCol_list.append(wall)
    room.background = arcade.load_texture(":resources:images/backgrounds/abstract_1.jpg")

    return room

def setup_room_4():
    """
    Create and return room 4.
    """
    room = Room()

    """ Set up the game and initialize the variables. """
    # Sprite lists
    room.wall_list = arcade.SpriteList()
    room.noCol_list = arcade.SpriteList()
    room.coin_list = arcade.SpriteList()

    # -- Set up the walls
    # Create bottom and top row of boxes
    # This y loops a list of two, the coordinate 0, and just under the top of window
    for y in (0, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE):
        # Loop for each box going across
        for x in range(0, setup.SCREEN_WIDTH, setup.SPRITE_SIZE):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", setup.SPRITE_SCALING)
            wall.left = x
            wall.bottom = y
            room.wall_list.append(wall)

    # Create left and right column of boxes
    for x in (0, setup.SCREEN_WIDTH - setup.SPRITE_SIZE):
        # Loop for each box going across
        for y in range(setup.SPRITE_SIZE, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE, setup.SPRITE_SIZE):
            # Skip making a block 4 and 5 blocks up
            if (y != setup.SPRITE_SIZE * 4 and y != setup.SPRITE_SIZE * 5):
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", setup.SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    room.background = arcade.load_texture(":resources:images/backgrounds/abstract_2.jpg")

    return room


def setup_room_5():
    """
    Create and return room 5.
    """
    room = Room()

    """ Set up the game and initialize the variables. """
    # Sprite lists
    room.wall_list = arcade.SpriteList()
    room.noCol_list = arcade.SpriteList()
    room.coin_list = arcade.SpriteList()

    # -- Set up the walls
    # Create bottom and top row of boxes
    # This y loops a list of two, the coordinate 0, and just under the top of window
    for y in (0, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE):
        # Loop for each box going across
        for x in range(0, setup.SCREEN_WIDTH, setup.SPRITE_SIZE):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", setup.SPRITE_SCALING)
            wall.left = x
            wall.bottom = y
            room.wall_list.append(wall)

    # Create left and right column of boxes
    for x in (0, setup.SCREEN_WIDTH - setup.SPRITE_SIZE):
        # Loop for each box going across
        for y in range(setup.SPRITE_SIZE, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE, setup.SPRITE_SIZE):
            # Skip making a block 4 and 5 blocks up
            if (y != setup.SPRITE_SIZE * 4 and y != setup.SPRITE_SIZE * 5):
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", setup.SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    room.background = arcade.load_texture(":resources:images/backgrounds/abstract_1.jpg")

    return room


def setup_room_6():
    """
    Create and return room 6.
    """
    room = Room()

    """ Set up the game and initialize the variables. """
    # Sprite lists
    room.wall_list = arcade.SpriteList()
    room.noCol_list = arcade.SpriteList()
    room.coin_list = arcade.SpriteList()

    # -- Set up the walls
    # Create bottom and top row of boxes
    # This y loops a list of two, the coordinate 0, and just under the top of window
    for y in (0, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE):
        # Loop for each box going across
        for x in range(0, setup.SCREEN_WIDTH, setup.SPRITE_SIZE):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", setup.SPRITE_SCALING)
            wall.left = x
            wall.bottom = y
            room.wall_list.append(wall)

    # Create left and right column of boxes
    for x in (0, setup.SCREEN_WIDTH - setup.SPRITE_SIZE):
        # Loop for each box going across
        for y in range(setup.SPRITE_SIZE, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE, setup.SPRITE_SIZE):
            # Skip making a block 4 and 5 blocks up
            if (y != setup.SPRITE_SIZE * 4 and y != setup.SPRITE_SIZE * 5):
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", setup.SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    room.background = arcade.load_texture(":resources:images/backgrounds/abstract_2.jpg")

    return room

def setup_room_7():
    """
    Create and return room 7.
    """
    room = Room()

    """ Set up the game and initialize the variables. """
    # Sprite lists
    room.wall_list = arcade.SpriteList()
    room.noCol_list = arcade.SpriteList()
    room.coin_list = arcade.SpriteList()

    # -- Set up the walls
    # Create bottom and top row of boxes
    # This y loops a list of two, the coordinate 0, and just under the top of window
    for y in (0, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE):
        # Loop for each box going across
        for x in range(0, setup.SCREEN_WIDTH, setup.SPRITE_SIZE):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", setup.SPRITE_SCALING)
            wall.left = x
            wall.bottom = y
            room.wall_list.append(wall)

    # Create left and right column of boxes
    for x in (0, setup.SCREEN_WIDTH - setup.SPRITE_SIZE):
        # Loop for each box going across
        for y in range(setup.SPRITE_SIZE, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE, setup.SPRITE_SIZE):
            # Skip making a block 4 and 5 blocks up
            if (y != setup.SPRITE_SIZE * 4 and y != setup.SPRITE_SIZE * 5) or x != 0:
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", setup.SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    room.background = arcade.load_texture(":resources:images/backgrounds/abstract_1.jpg")

    return room


def setup_room_8():
    """
    Create and return room 8. The coin room.
    """
    room = Room()

    """ Set up the game and initialize the variables. """
    # Sprite lists
    room.wall_list = arcade.SpriteList()
    room.noCol_list = arcade.SpriteList()
    room.coin_list = arcade.SpriteList()

    # -- Set up the walls
    # Create bottom and top row of boxes
    # This y loops a list of two, the coordinate 0, and just under the top of window
    for y in (0, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE):
        # Loop for each box going across
        for x in range(0, setup.SCREEN_WIDTH, setup.SPRITE_SIZE):
            if (x != setup.SPRITE_SIZE * 9 and x != setup.SPRITE_SIZE * 10) or y != 0:
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", setup.SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    # Create left and right column of boxes
    for x in (0, setup.SCREEN_WIDTH - setup.SPRITE_SIZE):
        # Loop for each box going across
        for y in range(setup.SPRITE_SIZE, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE, setup.SPRITE_SIZE):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", setup.SPRITE_SCALING)
            wall.left = x
            wall.bottom = y
            room.wall_list.append(wall)

    for i in range(setup.COIN_COUNT):
        # Create the coin instance
        # Coin image from kenney.nl
        coin = arcade.Sprite(":resources:images/items/coinGold.png",
                             setup.SPRITE_SCALING_COIN)

        # Position the coin
        coin.center_x = random.randrange(setup.USABLE_ROOM, setup.SCREEN_WIDTH - (setup.USABLE_ROOM))
        coin.center_y = random.randrange(setup.USABLE_ROOM, setup.SCREEN_HEIGHT - (setup.USABLE_ROOM))

        # Add the coin to the lists
        room.coin_list.append(coin)

    room.background = arcade.load_texture(":resources:images/backgrounds/abstract_1.jpg")

    return room