import arcade
import setup
import random


# Our room class. That's what we call for each room in our main game class.
class Room:
    def __init__(self, background_image):
        # All sprite lists and background image.
        self.wall_list = arcade.SpriteList()
        self.noCol_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.background = arcade.load_texture(background_image)

        """ There will now be a list of functions.
        Each of them will be making a slightly altered version of walls, 
        depending on our need for each room.
        Each function either makes the bottom and top row of walls,
        or the right and left. """

    def create_wall_sides_trophy_room(self, image):
        for x in (0, setup.SCREEN_WIDTH - setup.SPRITE_SIZE):
            for y in range(setup.SPRITE_SIZE, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE, setup.SPRITE_SIZE):
                # Skip making a block 5:
                if y != setup.SPRITE_SIZE * 5 or x == 0:
                    wall = arcade.Sprite(image, setup.SPRITE_SCALING)
                    wall.left = x
                    wall.bottom = y
                    self.wall_list.append(wall)

    def create_wall_top_bottom(self, image):
        for y in (0, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE):
            for x in range(0, setup.SCREEN_WIDTH, setup.SPRITE_SIZE):
                wall = arcade.Sprite(image, setup.SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                self.wall_list.append(wall)

    def create_wall_left_right(self, image):
        for x in (0, setup.SCREEN_WIDTH - setup.SPRITE_SIZE):
            for y in range(setup.SPRITE_SIZE, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE, setup.SPRITE_SIZE):
                if y != setup.SPRITE_SIZE * 5:
                    wall = arcade.Sprite(image, setup.SPRITE_SCALING)
                    wall.left = x
                    wall.bottom = y
                    self.wall_list.append(wall)

    def create_wall_top_minigame(self, image):
        for y in (0, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE):
            for x in range(0, setup.SCREEN_WIDTH, setup.SPRITE_SIZE):
                # Skips making two boxes at top to enter mini game
                if (x != setup.SPRITE_SIZE * 9 and x != setup.SPRITE_SIZE * 10 or y == 0):
                    wall = arcade.Sprite(image, setup.SPRITE_SCALING)
                    wall.left = x
                    wall.bottom = y
                    self.wall_list.append(wall)

    def create_wall_sides_minigame(self, image):
        for x in (0, setup.SCREEN_WIDTH - setup.SPRITE_SIZE):
            for y in range(setup.SPRITE_SIZE, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE, setup.SPRITE_SIZE):
                if y != setup.SPRITE_SIZE * 5 or x != 0:
                    wall = arcade.Sprite(image, setup.SPRITE_SCALING)
                    wall.left = x
                    wall.bottom = y
                    self.wall_list.append(wall)

    def create_wall_bottom_inside(self, image):
        for y in (0, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE):
            for x in range(0, setup.SCREEN_WIDTH, setup.SPRITE_SIZE):
                if (x != setup.SPRITE_SIZE * 9 and x != setup.SPRITE_SIZE * 10) or y != 0:
                    wall = arcade.Sprite(image, setup.SPRITE_SCALING)
                    wall.left = x
                    wall.bottom = y
                    self.wall_list.append(wall)

    def create_wall_sides_inside(self, image):
        for x in (0, setup.SCREEN_WIDTH - setup.SPRITE_SIZE):
            for y in range(setup.SPRITE_SIZE, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE, setup.SPRITE_SIZE):
                wall = arcade.Sprite(image, setup.SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                self.wall_list.append(wall)


# Creates the walls for the rooms
def setup_room_1():
    room = Room("images/jonas_1.webp") # Calling room class with background picture as parameter.
    room.create_wall_top_bottom("images/jonas_character.PNG") # Adds top / bottom row of walls with sprite as parameter.
    room.create_wall_sides_trophy_room("images/jonas_character.PNG") # Same for the right and left walls.
    return room


def setup_room_2():
    room = Room("images/bg1.png")
    room.create_wall_top_bottom(":resources:images/space_shooter/meteorGrey_big1.png")
    # In some rooms we will need to make our own walls, as we don't have functions for them.
    # These are usually one of a kind
    for x in (0, setup.SCREEN_WIDTH - setup.SPRITE_SIZE):
        for y in range(setup.SPRITE_SIZE, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE, setup.SPRITE_SIZE):
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
    wall = arcade.Sprite(":resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png", setup.SPRITE_SCALING)
    wall.left = 8 * setup.SPRITE_SIZE
    wall.bottom = 8 * setup.SPRITE_SIZE
    room.noCol_list.append(wall)
    return room


def setup_room_7():
    room = Room("images/bg7.jpg")
    room.create_wall_top_bottom(":resources:images/space_shooter/meteorGrey_big1.png")
    # Another instance of custom walls
    for x in (0, setup.SCREEN_WIDTH - setup.SPRITE_SIZE):
        for y in range(setup.SPRITE_SIZE, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE, setup.SPRITE_SIZE):
            if y != setup.SPRITE_SIZE * 5 or y == 0:
                wall = arcade.Sprite(":resources:images/space_shooter/meteorGrey_big1.png", setup.SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)
    return room

# This room is special, as it's our coin collection room.
def setup_room_8():
    room = Room("images/bg2.png")
    room.create_wall_bottom_inside(":resources:images/space_shooter/meteorGrey_big1.png")
    room.create_wall_sides_inside(":resources:images/space_shooter/meteorGrey_big1.png")

    # Makes 50 coins at random locations.
    for i in range(setup.COIN_COUNT):
        coin = arcade.Sprite("images/python-icon-2.png",
                             setup.SPRITE_SCALING_COIN)
        coin.center_x = random.randrange(setup.USABLE_ROOM, setup.SCREEN_WIDTH - (setup.USABLE_ROOM))
        coin.center_y = random.randrange(setup.USABLE_ROOM, setup.SCREEN_HEIGHT - (setup.USABLE_ROOM))
        room.coin_list.append(coin)

    return room

# Our second mini game. The maze.
def setup_room_9():
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
    # This plots our maze.
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
    # And prints it.
    for i in range(0, 13, 1):
        for x in y[i]:
            wall = arcade.Sprite(":resources:images/space_shooter/meteorGrey_big2.png", setup.SPRITE_SCALING)
            wall.left = x * setup.SPRITE_SIZE
            wall.bottom = status * setup.SPRITE_SIZE
            room.wall_list.append(wall)
        status += 1
    return room


# Our 3rd minigame. Falling coins. All logic done in on_update in main code.
def setup_room_10():
    room = Room("images/bg4.png")
    room.create_wall_bottom_inside(":resources:images/space_shooter/meteorGrey_big1.png")
    room.create_wall_sides_inside(":resources:images/space_shooter/meteorGrey_big1.png")
    return room

# Our last mini game. Hangman.
def setup_room_11():
    room = Room("images/bg5.png")
    room.create_wall_bottom_inside(":resources:images/space_shooter/meteorGrey_big1.png")
    room.create_wall_sides_inside(":resources:images/space_shooter/meteorGrey_big1.png")

    # The hanging man:
    wall = arcade.Sprite(":resources:images/animated_characters/male_person/malePerson_idle.png", setup.SPRITE_SCALING)
    wall.left = (13 * setup.SPRITE_SIZE) + 35
    wall.bottom = (3 * setup.SPRITE_SIZE) + 3
    room.wall_list.append(wall)

    # Create the Gallows:
    gallows_1 = arcade.Sprite("images/Gallows_1.png", setup.SPRITE_SCALING)
    gallows_2 = arcade.Sprite("images/Gallows_2.png", setup.SPRITE_SCALING)
    gallows_3 = arcade.Sprite("images/Gallows_3.png", setup.SPRITE_SCALING)
    gallows_4 = arcade.Sprite("images/Gallows_4.png", setup.SPRITE_SCALING)
    gallows_5 = arcade.Sprite("images/Gallows_5.png", setup.SPRITE_SCALING)
    gallows_6 = arcade.Sprite("images/Gallows_5.png", setup.SPRITE_SCALING)
    room.gallows_list = [gallows_1, gallows_2, gallows_3, gallows_4, gallows_5, gallows_6]
    room.gallows_list[0].left = 13 * setup.SPRITE_SIZE
    room.gallows_list[0].bottom = 2 * setup.SPRITE_SIZE
    room.wall_list.append(room.gallows_list[0])

    # Enemy robot that the player has to "fight" in hangman. Without the scaling, so the robot seems more threatening:
    enemy_robot = arcade.Sprite(":resources:images/animated_characters/robot/robot_idle.png")
    enemy_robot.left = 7 * setup.SPRITE_SIZE
    enemy_robot.bottom = 8 * setup.SPRITE_SIZE
    room.noCol_list.append(enemy_robot)

    # Locked boxes, one for each letter in the keyword:
    for x in range(12 * setup.SPRITE_SIZE, 18 * setup.SPRITE_SIZE, setup.SPRITE_SIZE):
        lock = arcade.Sprite(":resources:images/tiles/lockYellow.png", setup.SPRITE_SCALING)
        lock.left = x
        lock.bottom = 6 * setup.SPRITE_SIZE
        room.wall_list.append(lock)

    # Dictionary with all the letters of the alphabet in Sprites, so the user can choose for the hangman:
    room.letters = dict()

    room.letters['a'] = arcade.Sprite("images/pixel-speech-bubble_A.png", setup.SPRITE_SCALING_TEXT2)
    room.letters['b'] = arcade.Sprite("images/pixel-speech-bubble_B.png", setup.SPRITE_SCALING_TEXT2)
    room.letters['c'] = arcade.Sprite("images/pixel-speech-bubble_C.png", setup.SPRITE_SCALING_TEXT2)
    room.letters['d'] = arcade.Sprite("images/pixel-speech-bubble_D.png", setup.SPRITE_SCALING_TEXT2)
    room.letters['e'] = arcade.Sprite("images/pixel-speech-bubble_E.png", setup.SPRITE_SCALING_TEXT2)
    room.letters['f'] = arcade.Sprite("images/pixel-speech-bubble_F.png", setup.SPRITE_SCALING_TEXT2)
    room.letters['g'] = arcade.Sprite("images/pixel-speech-bubble_G.png", setup.SPRITE_SCALING_TEXT2)
    room.letters['h'] = arcade.Sprite("images/pixel-speech-bubble_H.png", setup.SPRITE_SCALING_TEXT2)
    room.letters['i'] = arcade.Sprite("images/pixel-speech-bubble_I.png", setup.SPRITE_SCALING_TEXT2)
    room.letters['j'] = arcade.Sprite("images/pixel-speech-bubble_J.png", setup.SPRITE_SCALING_TEXT2)
    room.letters['k'] = arcade.Sprite("images/pixel-speech-bubble_K.png", setup.SPRITE_SCALING_TEXT2)
    room.letters['l'] = arcade.Sprite("images/pixel-speech-bubble_L.png", setup.SPRITE_SCALING_TEXT2)
    room.letters['m'] = arcade.Sprite("images/pixel-speech-bubble_M.png", setup.SPRITE_SCALING_TEXT2)
    room.letters['n'] = arcade.Sprite("images/pixel-speech-bubble_N.png", setup.SPRITE_SCALING_TEXT2)
    room.letters['o'] = arcade.Sprite("images/pixel-speech-bubble_O.png", setup.SPRITE_SCALING_TEXT2)
    room.letters['p'] = arcade.Sprite("images/pixel-speech-bubble_P.png", setup.SPRITE_SCALING_TEXT2)
    room.letters['q'] = arcade.Sprite("images/pixel-speech-bubble_Q.png", setup.SPRITE_SCALING_TEXT2)
    room.letters['r'] = arcade.Sprite("images/pixel-speech-bubble_R.png", setup.SPRITE_SCALING_TEXT2)
    room.letters['s'] = arcade.Sprite("images/pixel-speech-bubble_S.png", setup.SPRITE_SCALING_TEXT2)
    room.letters['t'] = arcade.Sprite("images/pixel-speech-bubble_T.png", setup.SPRITE_SCALING_TEXT2)
    room.letters['u'] = arcade.Sprite("images/pixel-speech-bubble_U.png", setup.SPRITE_SCALING_TEXT2)
    room.letters['v'] = arcade.Sprite("images/pixel-speech-bubble_V.png", setup.SPRITE_SCALING_TEXT2)
    room.letters['w'] = arcade.Sprite("images/pixel-speech-bubble_W.png", setup.SPRITE_SCALING_TEXT2)
    room.letters['x'] = arcade.Sprite("images/pixel-speech-bubble_X.png", setup.SPRITE_SCALING_TEXT2)
    room.letters['y'] = arcade.Sprite("images/pixel-speech-bubble_Y.png", setup.SPRITE_SCALING_TEXT2)
    room.letters['z'] = arcade.Sprite("images/pixel-speech-bubble_Z.png", setup.SPRITE_SCALING_TEXT2)
    return room
