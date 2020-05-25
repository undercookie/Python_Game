import arcade
import os
import random
import setup
import rooms


# Necesarry function for animation of player model.
def load_texture_pair(filename):
    return [
        arcade.load_texture(filename)
    ]


class PlayerCharacter(arcade.Sprite):
    def __init__(self):

        # Parent class setup
        super().__init__()

        # Player model and animation variables + collision self.points.
        self.character_face_direction = setup.RIGHT_FACING  # Player animation starts facing right.
        self.cur_texture = 0
        self.scale = setup.CHARACTER_SCALING  # Player character scale (size)
        self.points = [[-11, -32], [11, -32], [11, 14], [-11, 14]]  # Collision / hitbox of player.

        # Textures for animation and player model
        main_path = "images/female_person/femalePerson"  # Our Path to the player sprite.
        self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")
        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_walk{i}.png") # Loads all 8 sprites states for animation.
            self.walk_textures.append(texture)

    # This is used to make the player animated.
    def update_animation(self, delta_time: float = 1/60):

        # Redundant code, that is needed, as we move either left or right. Doesn't change anything.
        if self.change_x < 0 and self.character_face_direction == setup.RIGHT_FACING:
            self.character_face_direction = setup.LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == setup.LEFT_FACING:
            self.character_face_direction = setup.RIGHT_FACING
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 7 * setup.UPDATES_PER_FRAME:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture // setup.UPDATES_PER_FRAME][self.character_face_direction]


# This class is needed to make flying meteors in our boss room.
class FlyingSprite(arcade.Sprite):

    def update(self):

        super().update()

        if self.right < 0:
            self.remove_from_sprite_lists()  # Removes the sprite if it exits the screen.


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))  # File path for resources included in Arcade.
        os.chdir(file_path)

        # All of our variables. Some easy to read - others lean more on the "magic number turned magic variable"
        self.total_time = 0.0  # Timer in bottom right corner
        self.current_room = 0  # Which room are we in, and should be loaded
        self.character_face_direction = setup.LEFT_FACING  # Which direction is the player facing.
        self.rooms = None  # We'll append all of our rooms to this.
        self.player = None  # Our player variable, that we will create an instance of our PlayerCharacter class for.
        self.player_list = None  # Our player list. Only one player will be appended to this.
        self.physics_engine = None  # This will load our physics engine. It'll be a "basic" one implemented in Arcade.
        self.score = 0  # Variable for our score that is displayed in the bottom left corner.
        self.total = 0  # These next three custom variables are used for progress in mini games.
        self.total2 = 0
        self.status_var = 0
        self.music_list = []  # We'll append our background music to this variable.
        self.current_song = 0  # What is our current background song? This variable tells that.
        self.music = None  # Used to actually play the music.
        self.collided = False  # If true, we have collided with another sprite list.
        self.second_updater = 0  # Another time variable, used for creating wall_rows in the boss room.
        self.new_time_variable = 0  # WHAT?? ANOTHER TIME VARIABLE? Time is hard...

    def setup(self):
        """ Set up the game and initialize the variables. """
        # Setting up variables in our setup class function. You'll recognize a lot from our __init__.
        self.player = PlayerCharacter()
        self.player_list = arcade.SpriteList()
        self.player.center_x = setup.SCREEN_WIDTH // 2
        self.player.center_y = setup.SCREEN_HEIGHT // 2
        self.player.scale = 0.8
        self.score = 0
        self.total = 0
        self.total2 = 0
        self.status_var = 0
        self.music_list = ["sounds/music_background.mp3", "sounds/music_evil.mp3", "sounds/music_win.mp3"]
        self.current_song = 0
        self.play_song()
        self.second_updater = 0
        self.new_time_variable = 0
        self.choice_hangman = None  # Used for keystrokes in hangman room.
        self.rooms = []
        self.player_list.append(self.player)
        self.total_time = 0.0

        # Creating all of our rooms. Check rooms.py
        room = rooms.setup_room_1()
        self.rooms.append(room)
        room = rooms.setup_room_2()
        self.rooms.append(room)
        room = rooms.setup_room_3()
        self.rooms.append(room)
        room = rooms.setup_room_4()
        self.rooms.append(room)
        room = rooms.setup_room_5()
        self.rooms.append(room)
        room = rooms.setup_room_6()
        self.rooms.append(room)
        room = rooms.setup_room_7()
        self.rooms.append(room)
        room = rooms.setup_room_8()
        self.rooms.append(room)
        room = rooms.setup_room_9()
        self.rooms.append(room)
        room = rooms.setup_room_10()
        self.rooms.append(room)
        room = rooms.setup_room_11()
        self.rooms.append(room)

        # Our starting room number and enables physics engine
        self.current_room = 1
        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.rooms[self.current_room].wall_list)

    # We use this to change between background music
    def advance_song(self):
        self.current_song += 1
        if self.current_song >= len(self.music_list):  # If we have run out of music, it'll loop back to the start.
            self.current_song = 0

    # We use this to loop commands in our boss room
    def update_second(self):
        if self.current_room == 6:
            self.second_updater += 1

    # Another function needed to play our background music
    def play_song(self):
        if self.music:
            self.music.stop()
        self.music = arcade.Sound(self.music_list[self.current_song], streaming=True)  # Starts the music
        self.music.play(setup.MUSIC_VOLUME)  # Takes our variable for music volume. (RIP Headphone users)

    # on_draw is what draws all of our game.
    def on_draw(self):
        arcade.start_render()
        # Background for each room is being drawn.
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            setup.SCREEN_WIDTH, setup.SCREEN_HEIGHT,
                                            self.rooms[self.current_room].background)
        self.rooms[self.current_room].wall_list.draw()  # Draw all the walls in this room
        self.rooms[self.current_room].noCol_list.draw()  # Draws the interactable characters.
        self.rooms[self.current_room].coin_list.draw()  # Draws our coins. Used in minigame 1 and 3
        self.player_list.draw()  # Draws our player.

        # This is used to create a score counter (bottom left)
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 16)
        # And timer in the bottom right of the window
        minutes = int(self.total_time) // 60
        seconds = int(self.total_time) % 60
        output_time = f"Time: {minutes:02d}:{seconds:02d}"
        arcade.draw_text(output_time, 1150, 20, arcade.color.WHITE, 16)
        # Ayy, we found our time variables again. Why do we need this many? Don't ask what we can't explain.
        if self.new_time_variable == seconds:
            self.update_second()
            self.new_time_variable += 2

    # Adds a new coin to the screen
    def add_coin(self, delta_time: float):
        coin = FlyingSprite("images/python-icon-2.png", setup.SPRITE_SCALING_COIN)  # Calls FlyingSprite with sprite.
        coin.center_x = random.randrange(setup.USABLE_ROOM, setup.SCREEN_WIDTH - setup.USABLE_ROOM)  # Location of coin.
        coin.center_y = setup.SCREEN_HEIGHT
        coin.change_y = random.randint(-5, -1)  # Alters the y of the coin.
        self.rooms[self.current_room].coin_list.append(coin)  # Appends the coin to the coin_list and therefore appears.

    # Adds a new wall row to the screen
    def add_wall_row(self, delta_time: float):
        local_random = random.randint(2, 14)  # This local variable is used to make a hole in the wall_row.
        # This code is explained in rooms.py
        for y in range(setup.SPRITE_SIZE, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE, setup.SPRITE_SIZE):
            if y != setup.SPRITE_SIZE * local_random:
                wall_row = arcade.Sprite(":resources:images/space_shooter/meteorGrey_big1.png", setup.SPRITE_SCALING)
                wall_row.left = setup.SCREEN_WIDTH - setup.SPRITE_SIZE
                wall_row.bottom = y
                wall_row.velocity = (-2, 0)  # Speed at which the wall_row is moving, and the direction.
                self.rooms[self.current_room].coin_list.append(wall_row)  # Appends our wall_row and it appears.

    # This function is called upon a keypress
    def on_key_press(self, key, modifiers):
        # Arrow key updates - movement
        # Upon a key press, player moves in a direction with set movement speed (seen in setup.py).
        if key == arcade.key.UP:
            self.player.change_y = setup.MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player.change_y = - setup.MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player.change_x = -setup.MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = setup.MOVEMENT_SPEED

        # Hangman letter input
        if self.current_room == 10:
            self.choice_hangman = None
            try:
                choice_hangman = chr(key)
                self.choice_hangman = choice_hangman
                current_room = self.rooms[self.current_room]
                self.letter_sprite = current_room.letters[self.choice_hangman]
                self.letter_sprite.center_x = self.player.center_x + 30
                self.letter_sprite.center_y = self.player.center_y + 30
                self.rooms[self.current_room].wall_list.append(self.letter_sprite)
            except:
                pass

    # This function is called upon release of a keypress
    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:  # Stops the player vertical movement.
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:  # Stops the player horizontal movement.
            self.player.change_x = 0

    # This is used to close doors to mini games upon completion.
    def door_mechanism_close(self):
        # This code is covered in rooms.py. But it basically just redraws the wall without the holes in them.
        for y in (0, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE):
            for x in range(0, setup.SCREEN_WIDTH, setup.SPRITE_SIZE):
                wall = arcade.Sprite(":resources:images/space_shooter/meteorGrey_big2.png", setup.SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                self.rooms[self.current_room].wall_list.append(wall)

    # This is used to open doors to progress after completion of mini game.
    def door_mechanism_open(self):
        # Removes the walls.
        for wall in self.rooms[self.current_room].wall_list:
            wall.remove_from_sprite_lists()
        # This code is covered in rooms.py. But it basically just redraws the wall with the holes in them.
        for y in (0, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE):
            for x in range(0, setup.SCREEN_WIDTH, setup.SPRITE_SIZE):
                wall = arcade.Sprite(":resources:images/space_shooter/meteorGrey_big2.png", setup.SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                self.rooms[self.current_room].wall_list.append(wall)
        for x in (0, setup.SCREEN_WIDTH - setup.SPRITE_SIZE):
            for y in range(setup.SPRITE_SIZE, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE, setup.SPRITE_SIZE):
                if y != setup.SPRITE_SIZE * 5:
                    wall = arcade.Sprite(":resources:images/space_shooter/meteorGrey_big1.png", setup.SPRITE_SCALING)
                    wall.left = x
                    wall.bottom = y
                    self.rooms[self.current_room].wall_list.append(wall)

    # Our main update function. All game logic and progression is in here. We'll get more in depth throughout it.
    def on_update(self, delta_time):

        # Updates the player sprite
        self.player_list.update()
        self.player_list.update_animation()
        self.physics_engine.update()

        # Do some logic here to figure out what room we are in, and if we need to go to a different room.
        if self.player.center_x > setup.SCREEN_WIDTH and self.current_room == 0:  # If player leaves screen:
            self.current_room = 1  # Change room.
            # Loads physics engine for that room.
            self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                             self.rooms[self.current_room].wall_list)
            self.player.center_x = 0  # Sets player location.

        elif self.player.center_x > setup.SCREEN_WIDTH and self.current_room == 1:
            self.current_room = 2
            self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                             self.rooms[self.current_room].wall_list)
            self.player.center_x = 0

        elif self.player.center_x > setup.SCREEN_WIDTH and self.current_room == 2:
            self.current_room = 3
            self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                             self.rooms[self.current_room].wall_list)
            self.player.center_x = 0

        elif self.player.center_y > setup.SCREEN_HEIGHT and self.current_room == 2:
            self.current_room = 7
            self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                             self.rooms[self.current_room].wall_list)
            self.player.center_y = 0

        elif self.player.center_x > setup.SCREEN_WIDTH and self.current_room == 3:
            self.current_room = 4
            self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                             self.rooms[self.current_room].wall_list)
            self.player.center_x = 0

        elif self.player.center_y > setup.SCREEN_HEIGHT and self.current_room == 3:
            self.current_room = 8
            self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                             self.rooms[self.current_room].wall_list)
            self.player.center_y = 0

        elif self.player.center_x > setup.SCREEN_WIDTH and self.current_room == 4:
            self.current_room = 5
            self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                             self.rooms[self.current_room].wall_list)
            self.player.center_x = 0

        elif self.player.center_y > setup.SCREEN_HEIGHT and self.current_room == 4:
            self.current_room = 9
            self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                             self.rooms[self.current_room].wall_list)
            self.player.center_y = 0

        elif self.player.center_x > setup.SCREEN_WIDTH and self.current_room == 5:
            self.current_room = 6
            self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                             self.rooms[self.current_room].wall_list)
            self.player.center_x = 0

        elif self.player.center_y > setup.SCREEN_HEIGHT and self.current_room == 5:
            self.current_room = 10
            self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                             self.rooms[self.current_room].wall_list)
            self.player.center_y = 0
            self.tries = 0
            self.correct_letters = 0
            self.gallows_remove_list = []

        elif self.player.center_x > setup.SCREEN_WIDTH and self.current_room == 6:
            self.current_room = 7
            self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                             self.rooms[self.current_room].wall_list)
            self.player.center_x = 0

        elif self.player.center_x < 0 and self.current_room == 1:
            self.current_room = 0
            self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                             self.rooms[self.current_room].wall_list)
            self.player.center_x = setup.SCREEN_WIDTH

        elif self.player.center_x < 0 and self.current_room == 2:
            self.current_room = 1
            self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                             self.rooms[self.current_room].wall_list)
            self.player.center_x = setup.SCREEN_WIDTH

        elif self.player.center_x < 0 and self.current_room == 3:
            self.current_room = 2
            self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                             self.rooms[self.current_room].wall_list)
            self.player.center_x = setup.SCREEN_WIDTH

        elif self.player.center_x < 0 and self.current_room == 4:
            self.current_room = 3
            self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                             self.rooms[self.current_room].wall_list)
            self.player.center_x = setup.SCREEN_WIDTH

        elif self.player.center_x < 0 and self.current_room == 5:
            self.current_room = 4
            self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                             self.rooms[self.current_room].wall_list)
            self.player.center_x = setup.SCREEN_WIDTH

        elif self.player.center_x < 0 and self.current_room == 6:
            self.current_room = 5
            self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                             self.rooms[self.current_room].wall_list)
            self.player.center_x = setup.SCREEN_WIDTH

        elif self.player.center_x < 0 and self.current_room == 7:
            self.current_room = 6
            self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                             self.rooms[self.current_room].wall_list)
            self.player.center_x = setup.SCREEN_WIDTH

        elif self.player.center_y < 0 and self.current_room == 7:
            self.current_room = 2
            self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                             self.rooms[self.current_room].wall_list)
            self.player.center_y = setup.SCREEN_HEIGHT

        elif self.player.center_y > setup.SCREEN_HEIGHT and self.current_room == 8:
            self.current_room = 3
            self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                             self.rooms[self.current_room].wall_list)
            self.player.center_y = setup.SCREEN_HEIGHT - 50
            self.player.center_x = setup.SCREEN_WIDTH // 2
            MyGame.door_mechanism_close(self)  # Calls the close and open door functions, covered earlier.
            MyGame.door_mechanism_open(self)
            # Dialogue, will be commented on later in the code.
            dialogue_1 = arcade.Sprite("images/room_4_dia_3.png", setup.SPRITE_SCALING_TEXT2)
            dialogue_2 = arcade.Sprite("images/room_4_dia_4.png", setup.SPRITE_SCALING_TEXT2)
            dialogue_1.center_x = 669
            dialogue_1.center_y = 738
            dialogue_2.center_x = 692
            dialogue_2.center_y = 625
            self.rooms[self.current_room].wall_list.append(dialogue_1)
            self.rooms[self.current_room].wall_list.append(dialogue_2)

        elif self.player.center_y < 0 and self.current_room == 9:
            for coin in self.rooms[self.current_room].coin_list:
                coin.remove_from_sprite_lists()  # Removes the coins from the sprite list.
            self.score = 0  # Sets our score to 0. Used if score is not reset earlier.
            self.current_room = 4
            self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                             self.rooms[self.current_room].wall_list)
            self.player.center_y = setup.SCREEN_HEIGHT

        elif self.player.center_y < 0 and self.current_room == 10:
            self.current_room = 5
            self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                             self.rooms[self.current_room].wall_list)
            self.player.center_y = setup.SCREEN_HEIGHT

        # This one is to throw out player and reset counters if they take more than 20 seconds.
        elif self.current_room == 8 and self.total_time >= 20:
            self.current_room = 3
            self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                             self.rooms[self.current_room].wall_list)
            self.player.center_y = setup.SCREEN_HEIGHT - 50
            self.player.center_x = setup.SCREEN_WIDTH // 2
            self.total_time = 0  # Resets time counter.

        # This one is to throw out player and reset counters if they take more than 15 seconds.
        elif self.total2 >= 1 and self.total_time >= 15:
            self.current_room = 2
            self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                             self.rooms[self.current_room].wall_list)
            self.player.center_y = setup.SCREEN_HEIGHT - 50
            self.player.center_x = setup.SCREEN_WIDTH // 2
            self.total2 = 0  # Resets all our variables needed for progress.
            self.total = 0
            self.total_time = 0
            self.score = 0

        elif self.current_room == 7 and self.score == 40:
            self.current_room = 2
            self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                             self.rooms[self.current_room].wall_list)
            self.player.center_y = setup.SCREEN_HEIGHT - 50
            self.player.center_x = setup.SCREEN_WIDTH // 2
            self.total2 = 0
            self.total = 0
            self.score = 0
            self.total_time = 0
            MyGame.door_mechanism_close(self)
            MyGame.door_mechanism_open(self)
            # Dialogue, will be commented on later in the code.
            dialogue_1 = arcade.Sprite("images/room_3_dia_3.png", setup.SPRITE_SCALING_TEXT2)
            dialogue_2 = arcade.Sprite("images/room_3_dia_4.png", setup.SPRITE_SCALING_TEXT2)
            dialogue_1.center_x = 667
            dialogue_1.center_y = 740
            dialogue_2.center_x = 692
            dialogue_2.center_y = 625
            self.rooms[self.current_room].wall_list.append(dialogue_1)
            self.rooms[self.current_room].wall_list.append(dialogue_2)

        elif self.current_room == 9 and self.score == 20:
            self.current_room = 4
            self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                             self.rooms[self.current_room].wall_list)
            self.player.center_y = setup.SCREEN_HEIGHT - 50
            self.player.center_x = setup.SCREEN_WIDTH // 2
            self.total2 = 0
            self.total = 0
            self.score = 0
            self.total_time = 0
            MyGame.door_mechanism_close(self)
            MyGame.door_mechanism_open(self)
            # Dialogue, will be commented on later in the code.
            dialogue_1 = arcade.Sprite("images/room_5_dia_3.png", setup.SPRITE_SCALING_TEXT2)
            dialogue_2 = arcade.Sprite("images/room_5_dia_4.png", setup.SPRITE_SCALING_TEXT2)
            dialogue_1.center_x = 660
            dialogue_1.center_y = 740
            dialogue_2.center_x = 692
            dialogue_2.center_y = 625
            self.status_var = 0
            self.rooms[self.current_room].wall_list.append(dialogue_1)
            self.rooms[self.current_room].wall_list.append(dialogue_2)

        # Hangman room logic.
        if self.current_room == 10:
            # This is our secret word
            word_hangman = "binary"
            if self.choice_hangman != None:
                if self.choice_hangman in self.rooms[self.current_room].letters.keys():
                    if self.choice_hangman in word_hangman:
                        # Cover boxes with the right letter when guessed:
                        if self.choice_hangman == "b":
                            letter_B = arcade.Sprite("images/lock_B.png", setup.SPRITE_SCALING)
                            letter_B.left = 12 * setup.SPRITE_SIZE
                            letter_B.bottom = 6 * setup.SPRITE_SIZE
                            self.rooms[self.current_room].wall_list.append(letter_B)
                            self.correct_letters += 1
                            self.choice_hangman = None
                        if self.choice_hangman == "i":
                            letter_I = arcade.Sprite("images/lock_I.png", setup.SPRITE_SCALING)
                            letter_I.left = 13 * setup.SPRITE_SIZE
                            letter_I.bottom = 6 * setup.SPRITE_SIZE
                            self.rooms[self.current_room].wall_list.append(letter_I)
                            self.correct_letters += 1
                            self.choice_hangman = None
                        if self.choice_hangman == "n":
                            letter_N = arcade.Sprite("images/lock_N.png", setup.SPRITE_SCALING)
                            letter_N.left = 14 * setup.SPRITE_SIZE
                            letter_N.bottom = 6 * setup.SPRITE_SIZE
                            self.rooms[self.current_room].wall_list.append(letter_N)
                            self.correct_letters += 1
                            self.choice_hangman = None
                        if self.choice_hangman == "a":
                            letter_A = arcade.Sprite("images/lock_A.png", setup.SPRITE_SCALING)
                            letter_A.left = 15 * setup.SPRITE_SIZE
                            letter_A.bottom = 6 * setup.SPRITE_SIZE
                            self.rooms[self.current_room].wall_list.append(letter_A)
                            self.correct_letters += 1
                            self.choice_hangman = None
                        if self.choice_hangman == "r":
                            letter_R = arcade.Sprite("images/lock_R.png", setup.SPRITE_SCALING)
                            letter_R.left = 16 * setup.SPRITE_SIZE
                            letter_R.bottom = 6 * setup.SPRITE_SIZE
                            self.rooms[self.current_room].wall_list.append(letter_R)
                            self.correct_letters += 1
                            self.choice_hangman = None
                        if self.choice_hangman == "y":
                            letter_Y = arcade.Sprite("images/lock_Y.png", setup.SPRITE_SCALING)
                            letter_Y.left = 17 * setup.SPRITE_SIZE
                            letter_Y.bottom = 6 * setup.SPRITE_SIZE
                            self.rooms[self.current_room].wall_list.append(letter_Y)
                            self.correct_letters += 1
                            self.choice_hangman = None
                    # Else adds an error and draws another part of the gallow
                    else:
                        self.tries += 1
                        self.rooms[self.current_room].gallows_list[self.tries].left = 13 * setup.SPRITE_SIZE
                        self.rooms[self.current_room].gallows_list[self.tries].bottom = 2 * setup.SPRITE_SIZE
                        self.rooms[self.current_room].wall_list.append(self.rooms[self.current_room].gallows_list[self.tries])
                        self.choice_hangman = None
                        if self.tries != 0:
                            self.gallows_remove_list.append(self.rooms[self.current_room].gallows_list[self.tries -1])
                            for gallow in self.gallows_remove_list:
                                gallow.remove_from_sprite_lists()

                                new_gallow = self.rooms[self.current_room].gallows_list[self.tries]

                                self.rooms[self.current_room].gallows_list[self.tries].left = 13 * setup.SPRITE_SIZE
                                self.rooms[self.current_room].gallows_list[self.tries].bottom = 2 * setup.SPRITE_SIZE
                                self.rooms[self.current_room].wall_list.append(new_gallow)

        if self.current_room == 10 and self.tries == 5:
            self.current_room = 5
            self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                             self.rooms[self.current_room].wall_list)
            self.player.center_y = setup.SCREEN_HEIGHT - 50
            self.player.center_x = setup.SCREEN_WIDTH // 2
            self.tries == 0
            self.correct_letters = 0
            self.rooms[10] = rooms.setup_room_11()

        if self.current_room == 10 and self.correct_letters == 6:
            self.current_room = 5
            self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                             self.rooms[self.current_room].wall_list)
            self.player.center_y = setup.SCREEN_HEIGHT - 50
            self.player.center_x = setup.SCREEN_WIDTH // 2
            # Dialogue, will be commented on later in the code.
            dialogue_1 = arcade.Sprite("images/room_6_dia_3.png", setup.SPRITE_SCALING_TEXT2)
            dialogue_2 = arcade.Sprite("images/room_6_dia_4.png", setup.SPRITE_SCALING_TEXT2)
            dialogue_1.center_x = 669
            dialogue_1.center_y = 738
            dialogue_2.center_x = 692
            dialogue_2.center_y = 625
            self.rooms[self.current_room].wall_list.append(dialogue_1)
            self.rooms[self.current_room].wall_list.append(dialogue_2)

            MyGame.door_mechanism_close(self)
            MyGame.door_mechanism_open(self)

        # Collision with coin - removing them and creating them again.
        if self.current_room == 7:

            coin_list = self.rooms[self.current_room].coin_list  # Loads all of our coins into a list.
            coin_hit_list = arcade.check_for_collision_with_list(self.player, coin_list)  # Collision-check. New list.
            self.rooms[self.current_room].coin_list.update()
            for coin in coin_hit_list:
                coin.remove_from_sprite_lists()  # Removes the coins we've hit
                # And draws a new one.
                coin2 = arcade.Sprite("images/python-icon-2.png",
                                     setup.SPRITE_SCALING_COIN)
                coin2.center_x = random.randrange(setup.USABLE_ROOM, setup.SCREEN_WIDTH - setup.USABLE_ROOM)
                coin2.center_y = random.randrange(setup.USABLE_ROOM, setup.SCREEN_HEIGHT - setup.USABLE_ROOM)
                self.rooms[self.current_room].coin_list.append(coin2)
                self.total += 1  # Adds one to our "in code only" timer counter.
                if self.total == 1:
                    self.total2 += 1  # So many "magic variables". This one is used to start the timer.
                self.score += 1  # Adds one to our score counter

        # Collision with flying coin - removing them and creating them again.
        if self.current_room == 9:
            # Creates 5 coins at the start.
            if self.status_var < 5:
                self.add_coin(delta_time)
                self.status_var += 1
            # This is code from last part. Checks for collision and removes.
            coin_list = self.rooms[self.current_room].coin_list
            coin_hit_list = arcade.check_for_collision_with_list(self.player, coin_list)
            self.rooms[self.current_room].coin_list.update()
            for coin in coin_hit_list:
                coin.remove_from_sprite_lists()
                # If you catch a coin - a new one spawns.
                self.add_coin(delta_time)
                self.score += 1 # Score is updated.

        # Boss room wall row creation and collision detection.
        if self.current_room == 6:
            # Same code again. This time the "coin" is a row of walls.
            wall_row_list = self.rooms[self.current_room].coin_list
            wall_row_hit_list = arcade.check_for_collision_with_list(self.player, wall_row_list)
            self.rooms[self.current_room].coin_list.update()
            # We add a new wall every three seconds.
            if self.second_updater != self.new_time_variable and self.second_updater % 3 == 0:
                self.add_wall_row(delta_time)
                self.new_time_variable = self.second_updater
            # Still update one of our many time variables, every second.
            if self.second_updater != self.new_time_variable and self.second_updater % 3 != 0:
                self.new_time_variable = self.second_updater
            for wall_row in wall_row_hit_list:
                for wall_row in wall_row_list:
                    wall_row.remove_from_sprite_lists()
                self.current_room = 5  # Kicks us out, if hit.
                self.new_time_variable = 0  # Reset one of our time variables.
                self.player.center_y = setup.SCREEN_HEIGHT // 2 - 100
                self.player.center_x = setup.SCREEN_WIDTH - 150
        # Spawns "SANOJ" after 15 seconds. Code is more in depth in rooms.py
        if self.current_room == 6 and self.new_time_variable == 15:
            wall = arcade.Sprite("images/jonas_character.PNG",
                                 setup.SPRITE_SCALING)
            wall.left = 18 * setup.SPRITE_SIZE
            wall.bottom = 2 * setup.SPRITE_SIZE
            self.rooms[self.current_room].noCol_list.append(wall)

        # Dialogue logic. New list of objects, noCol. When player model hits, dialogue appears - depending on room.
        player_list = self.rooms[self.current_room].noCol_list
        player_hit_list = arcade.check_for_collision_with_list(self.player, player_list)

        self.rooms[self.current_room].noCol_list.update()

        for player in player_hit_list:

            if self.current_room == 1 and self.total_time == 0:
                # Dialogue location and scaling.
                dialogue_1 = arcade.Sprite("images/room_2_dia_1.png", setup.SPRITE_SCALING_TEXT)
                dialogue_2 = arcade.Sprite("images/room_2_dia_2.png", setup.SPRITE_SCALING_TEXT)
                dialogue_1.center_x = 650
                dialogue_1.center_y = 740
                dialogue_2.center_x = 650
                dialogue_2.center_y = 625
                # Appending the dialogue and therefore making it appear on screen.
                self.rooms[self.current_room].wall_list.append(dialogue_1)
                self.rooms[self.current_room].wall_list.append(dialogue_2)
            if self.current_room == 2 and self.score != 40:
                dialogue_1 = arcade.Sprite("images/room_3_dia_1.png", setup.SPRITE_SCALING_TEXT)
                dialogue_2 = arcade.Sprite("images/room_3_dia_2.png", setup.SPRITE_SCALING_TEXT)
                dialogue_1.center_x = 650
                dialogue_1.center_y = 740
                dialogue_2.center_x = 650
                dialogue_2.center_y = 625
                self.rooms[self.current_room].wall_list.append(dialogue_1)
                self.rooms[self.current_room].wall_list.append(dialogue_2)
            if self.current_room == 3:
                dialogue_1 = arcade.Sprite("images/room_4_dia_1.png", setup.SPRITE_SCALING_TEXT)
                dialogue_2 = arcade.Sprite("images/room_4_dia_2.png", setup.SPRITE_SCALING_TEXT)
                dialogue_1.center_x = 650
                dialogue_1.center_y = 740
                dialogue_2.center_x = 650
                dialogue_2.center_y = 625
                self.rooms[self.current_room].wall_list.append(dialogue_1)
                self.rooms[self.current_room].wall_list.append(dialogue_2)
            if self.current_room == 4 and self.score != 20:
                dialogue_1 = arcade.Sprite("images/room_5_dia_1.png", setup.SPRITE_SCALING_TEXT)
                dialogue_2 = arcade.Sprite("images/room_5_dia_2.png", setup.SPRITE_SCALING_TEXT)
                dialogue_1.center_x = 650
                dialogue_1.center_y = 740
                dialogue_2.center_x = 650
                dialogue_2.center_y = 625
                self.rooms[self.current_room].wall_list.append(dialogue_1)
                self.rooms[self.current_room].wall_list.append(dialogue_2)
            if self.current_room == 5:
                dialogue_1 = arcade.Sprite("images/room_6_dia_1.png", setup.SPRITE_SCALING_TEXT)
                dialogue_2 = arcade.Sprite("images/room_6_dia_2.png", setup.SPRITE_SCALING_TEXT)
                dialogue_1.center_x = 650
                dialogue_1.center_y = 700
                dialogue_2.center_x = 650
                dialogue_2.center_y = 625
                self.rooms[self.current_room].wall_list.append(dialogue_1)
                self.rooms[self.current_room].wall_list.append(dialogue_2)
            if self.current_room == 6:
                self.current_room = 1
                self.door_mechanism_open()
                dialogue_1 = arcade.Sprite("images/room_2_dia_3.png", setup.SPRITE_SCALING_TEXT)
                dialogue_2 = arcade.Sprite("images/room_2_dia_4.png", setup.SPRITE_SCALING_TEXT)
                dialogue_1.center_x = 670
                dialogue_1.center_y = 740
                dialogue_2.center_x = 670
                dialogue_2.center_y = 625
                self.rooms[self.current_room].wall_list.append(dialogue_1)
                self.rooms[self.current_room].wall_list.append(dialogue_2)
                self.current_song = 2
                self.play_song()
            if self.current_room == 10:
                dialogue_1 = arcade.Sprite("images/room_10_dia_1.png", setup.SPRITE_SCALING_TEXT)
                dialogue_2 = arcade.Sprite("images/room_10_dia_2.png", setup.SPRITE_SCALING_TEXT)
                dialogue_1.center_x = 650
                dialogue_1.center_y = 740
                dialogue_2.center_x = 650
                dialogue_2.center_y = 650
                self.rooms[self.current_room].wall_list.append(dialogue_1)
                self.rooms[self.current_room].wall_list.append(dialogue_2)

        # Some rooms trigger the timer seen in the bottom right. This is logic for that. Also another background song.
        if self.current_room == 7 and self.total >= 1:
            self.total_time += delta_time
        if self.current_room == 8:
            self.total_time += delta_time
        # Updates our background music for the boss fight.
        if self.current_room == 6:
            if self.total_time == 0:
                self.current_song = 1
                self.play_song()
            self.total_time += delta_time
        # Needed variable reset.
        if self.current_room == 4:
            self.status_var = 0

        # Background music update.
        position = self.music.get_stream_position()
        if position == 0.0:
            self.play_song()


# Main function running the game.
def main():
    window = MyGame(setup.SCREEN_WIDTH, setup.SCREEN_HEIGHT, setup.SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
