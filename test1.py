"""
What happend in this commit?

SATURDAY:

I made the final boss room, still needs tweaking, kinda iffy, but working.
SANOJ will spawn after 15 seconds. If you hit the moving walls you respawn and will have to enter again.
Hit SANOJ after he spawned, to get teleported to room 1, with a new dialouge message and the trophy room opening up.
Still needs bug-fixing and transistion, when we implement hangman. Right now you can just walk through room 6.
I also added new background and "music" for the boss room. This NEEDS to be changed. It's scaring me shitless.
Also added epic music upon victory. This I like.
Now I sleep.

SUNDAY:

Edited boss room, still finicky, but better. Half of the blocks now remove upon death.
Added character animation. Played around with mubling sound upon dialouge, but wasn't really working.
Now I break.


Todo-list:
 - Shorten the on_update definition. I'm getting lost among all the elif statements. Anything we can do?
 - Make the hangman game.
 - Add more sound. Footsteps, mumbling for tutorial, etc.
 - Comments and tutorial .txt file

Done-list:
 - Add another .append list for non-collision objects and implement it.
 - We now have 3 sprite lists. Wall, noCol and coin.
 - add a global variable so no objects like coins will be in the walls
 - Add collision for coins, and make them disappear when touched.
 - Make a scoreboard.
 - Make coins reappear after fail
 - Transition to and from mini-games. Requires mini-game(s) to be completed.
 - Work out graphical elements in regards to textboxes from Jonas (tutorial)
 - Make a maze minigame
 - Experiment with sprites downloads and / or backgrounds.
 - Make the final boss room!!!
 - Added more sound.
 - Add animation to character. These sprites already exist. How?
"""

import arcade
import os
import random
import setup
import rooms

def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename)
    ]

class PlayerCharacter(arcade.Sprite):
    def __init__(self):

        # Set up parent class
        super().__init__()

        # Default to face-right
        self.character_face_direction = setup.RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0

        # Track out state
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False
        self.scale = setup.CHARACTER_SCALING
        # Adjust the collision box. Default includes too much empty space
        # side-to-side. Box is centered at sprite center, (0, 0)
        self.points = [[-11, -32], [11, -32], [11, 14], [-11, 14]]

        # --- Load Textures ---

        # Images from Kenney.nl's Asset Pack 3
        main_path = "images/female_person/femalePerson"

        # Load textures for idle standing
        self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")

        # Load textures for walking
        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)


    def update_animation(self, delta_time: float = 1/60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == setup.RIGHT_FACING:
            self.character_face_direction = setup.LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == setup.LEFT_FACING:
            self.character_face_direction = setup.RIGHT_FACING

        # Idle animation
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 7 * setup.UPDATES_PER_FRAME:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture // setup.UPDATES_PER_FRAME][self.character_face_direction]

class FlyingSprite(arcade.Sprite):

    def update(self):

        super().update()

        if self.right < 0:
            self.remove_from_sprite_lists()


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        """
        Initializer
        """
        super().__init__(width, height, title)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)


        self.total_time = 0.0

        # Sprite lists
        self.current_room = 0

        # Set up the player
        self.character_face_direction = setup.LEFT_FACING
        self.rooms = None
        self.player = None
        self.player_list = None
        self.physics_engine = None
        self.score = 0
        self.total = 0
        self.total2 = 0
        self.status_var = 0
        self.enemies_list = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()
        self.music_list = []
        self.current_song = 0
        self.music = None
        self.collided = False
        self.second_updater = 0
        self.new_time_variable = 0

        main_path = ":resources:images/animated_characters/female_adventurer/femaleAdventurer"
        # main_path = ":resources:images/animated_characters/female_person/femalePerson"
        # main_path = ":resources:images/animated_characters/male_person/malePerson"
        # main_path = ":resources:images/animated_characters/male_adventurer/maleAdventurer"
        # main_path = ":resources:images/animated_characters/zombie/zombie"
        # main_path = ":resources:images/animated_characters/robot/robot"

        # Load textures for idle standing
        self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")

        # Load textures for walking
        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

    def setup(self):
        """ Set up the game and initialize the variables. """
        # Set up the player
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
        self.choice_hangman = None

        # Our list of rooms
        self.rooms = []

        self.player_list.append(self.player)

        # Create the rooms. Extend the pattern for each room.
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

        # Our starting room number
        self.current_room = 5

        self.total_time = 0.0

        # Create a physics engine for this room
        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.rooms[self.current_room].wall_list)


    def advance_song(self):
        self.current_song += 1
        if self.current_song >= len(self.music_list):
            self.current_song = 0

    def update_second(self):
        if self.current_room == 6:
            self.second_updater += 1

    def play_song(self):
        """ Play the song. """
        # Stop what is currently playing.
        if self.music:
            self.music.stop()

        # Play the next song
        self.music = arcade.Sound(self.music_list[self.current_song], streaming=True)
        self.music.play(setup.MUSIC_VOLUME)
        # This is a quick delay. If we don't do this, our elapsed time is 0.0
        # and on_update will think the music is over and advance us to the next
        # song before starting this one.

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            setup.SCREEN_WIDTH, setup.SCREEN_HEIGHT,
                                            self.rooms[self.current_room].background)

        # Draw all the walls in this room
        self.rooms[self.current_room].wall_list.draw()
        self.rooms[self.current_room].noCol_list.draw()
        self.rooms[self.current_room].coin_list.draw()

        # If you have coins or monsters, then copy and modify the line
        # above for each list.

        self.player_list.draw()

        self.all_sprites.draw()

        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

        minutes = int(self.total_time) // 60
        seconds = int(self.total_time) % 60
        output_time = f"Time: {minutes:02d}:{seconds:02d}"
        arcade.draw_text(output_time, 1150, 20, arcade.color.WHITE, 14)
        if self.new_time_variable == seconds:
            self.update_second()
            self.new_time_variable += 2

    def add_coin(self, delta_time: float):
        """Adds a new coin to the screen
        Arguments:
            delta_time {float} -- How much time has passed since the last call
        """

        # First, create the new coin sprite
        coin = FlyingSprite("images/python-icon-2.png", setup.SPRITE_SCALING_COIN)

        # Set its position to a random height and off screen right
        coin.center_x = random.randrange(setup.USABLE_ROOM, setup.SCREEN_WIDTH - setup.USABLE_ROOM)
        coin.center_y = setup.SCREEN_HEIGHT

        # Set its speed to a random speed heading left
        coin.change_y = random.randint(-5, -1)

        # Add it to the enemies list
        self.rooms[self.current_room].coin_list.append(coin)


    def add_wall_row(self, delta_time: float):
        """Adds a new enemy to the screen
        Arguments:
            delta_time {float} -- How much time has passed since the last call
        """


        local_random = random.randint(2, 14)

        for y in range(setup.SPRITE_SIZE, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE, setup.SPRITE_SIZE):
            # Skip making a block 5:
            if y != setup.SPRITE_SIZE * local_random:
                wall_row = arcade.Sprite(":resources:images/space_shooter/meteorGrey_big1.png", setup.SPRITE_SCALING)
                wall_row.left = setup.SCREEN_WIDTH - setup.SPRITE_SIZE
                wall_row.bottom = y
                wall_row.velocity = (-2, 0)
                self.rooms[self.current_room].coin_list.append(wall_row)


    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.player.change_y = setup.MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player.change_y = - setup.MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player.change_x = -setup.MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = setup.MOVEMENT_SPEED

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

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0

    def door_mechanism_close(self):
        for y in (0, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE):
            for x in range(0, setup.SCREEN_WIDTH, setup.SPRITE_SIZE):
                wall = arcade.Sprite(":resources:images/space_shooter/meteorGrey_big2.png", setup.SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                self.rooms[self.current_room].wall_list.append(wall)

    def door_mechanism_open(self):
        for wall in self.rooms[self.current_room].wall_list:
            wall.remove_from_sprite_lists()
        for y in (0, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE):
            # Loop for each box going across
            for x in range(0, setup.SCREEN_WIDTH, setup.SPRITE_SIZE):
                wall = arcade.Sprite(":resources:images/space_shooter/meteorGrey_big2.png", setup.SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                self.rooms[self.current_room].wall_list.append(wall)

        # Create left and right column of boxes
        for x in (0, setup.SCREEN_WIDTH - setup.SPRITE_SIZE):
            # Loop for each box going across
            for y in range(setup.SPRITE_SIZE, setup.SCREEN_HEIGHT - setup.SPRITE_SIZE, setup.SPRITE_SIZE):
                # Skip making a block 4 and 5 blocks up
                if y != setup.SPRITE_SIZE * 5:
                    wall = arcade.Sprite(":resources:images/space_shooter/meteorGrey_big1.png", setup.SPRITE_SCALING)
                    wall.left = x
                    wall.bottom = y
                    self.rooms[self.current_room].wall_list.append(wall)

    def on_update(self, delta_time):
        """ Movement and game logic """

        self.player_list.update()
        self.player_list.update_animation()

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.physics_engine.update()

        # Do some logic here to figure out what room we are in, and if we need to go
        # to a different room.
        if self.player.center_x > setup.SCREEN_WIDTH and self.current_room == 0:
            self.current_room = 1
            self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                             self.rooms[self.current_room].wall_list)
            self.player.center_x = 0

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
            MyGame.door_mechanism_close(self)
            MyGame.door_mechanism_open(self)
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
                coin.remove_from_sprite_lists()
            self.score = 0
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
            self.total_time = 0

        # This one is to throw out player and reset counters if they take more than 15 seconds.
        elif self.total2 >= 1 and self.total_time >= 15:
            self.current_room = 2
            self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                             self.rooms[self.current_room].wall_list)
            self.player.center_y = setup.SCREEN_HEIGHT - 50
            self.player.center_x = setup.SCREEN_WIDTH // 2
            self.total2 = 0
            self.total = 0
            self.total_time = 0
            self.score = 0

        elif self.current_room == 7 and self.score == 4:
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
            dialogue_1 = arcade.Sprite("images/room_3_dia_3.png", setup.SPRITE_SCALING_TEXT2)
            dialogue_2 = arcade.Sprite("images/room_3_dia_4.png", setup.SPRITE_SCALING_TEXT2)
            dialogue_1.center_x = 667
            dialogue_1.center_y = 740
            dialogue_2.center_x = 692
            dialogue_2.center_y = 625
            self.rooms[self.current_room].wall_list.append(dialogue_1)
            self.rooms[self.current_room].wall_list.append(dialogue_2)

        elif self.current_room == 9 and self.score == 2:
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
            dialogue_1 = arcade.Sprite("images/room_5_dia_3.png", setup.SPRITE_SCALING_TEXT2)
            dialogue_2 = arcade.Sprite("images/room_5_dia_4.png", setup.SPRITE_SCALING_TEXT2)
            dialogue_1.center_x = 660
            dialogue_1.center_y = 740
            dialogue_2.center_x = 692
            dialogue_2.center_y = 625
            self.status_var = 0

            # Add it to the enemies list
            self.rooms[self.current_room].wall_list.append(dialogue_1)
            self.rooms[self.current_room].wall_list.append(dialogue_2)

        if self.current_room == 10:
            word_hangman = "binary"
            if self.choice_hangman != None:
                if self.choice_hangman in self.rooms[self.current_room].letters.keys():
                    if self.choice_hangman in word_hangman:
                        #cover boxes with the right letter when guessed:
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

                                new_gallow =  self.rooms[self.current_room].gallows_list[self.tries]

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

            MyGame.door_mechanism_close(self)
            MyGame.door_mechanism_open(self)

        # Collision with coin - removing them and creating them again.
        if self.current_room == 7:

            coin_list = self.rooms[self.current_room].coin_list
            coin_hit_list = arcade.check_for_collision_with_list(self.player, coin_list)

            self.rooms[self.current_room].coin_list.update()
            for coin in coin_hit_list:
                coin.remove_from_sprite_lists()

                coin2 = arcade.Sprite("images/python-icon-2.png",
                                     setup.SPRITE_SCALING_COIN)

                # Set its position to a random height and off screen right
                coin2.center_x = random.randrange(setup.USABLE_ROOM, setup.SCREEN_WIDTH - setup.USABLE_ROOM)
                coin2.center_y = random.randrange(setup.USABLE_ROOM, setup.SCREEN_HEIGHT - setup.USABLE_ROOM)

                # Add it to the enemies list
                self.rooms[self.current_room].coin_list.append(coin2)

                self.total += 1
                if self.total == 1:
                    self.total2 += 1
                self.score += 1

        # Collision with flying coin - removing them and creating them again.
        if self.current_room == 9:
            if self.status_var < 5:
                self.add_coin(delta_time)
                self.status_var += 1
            coin_list = self.rooms[self.current_room].coin_list
            coin_hit_list = arcade.check_for_collision_with_list(self.player, coin_list)

            self.rooms[self.current_room].coin_list.update()
            for coin in coin_hit_list:
                coin.remove_from_sprite_lists()
                self.add_coin(delta_time)
                self.score += 1

        if self.current_room == 6:
            wall_row_list = self.rooms[self.current_room].coin_list
            wall_row_hit_list = arcade.check_for_collision_with_list(self.player, wall_row_list)
            self.rooms[self.current_room].coin_list.update()
            if self.second_updater != self.new_time_variable and self.second_updater % 3 == 0:
                self.add_wall_row(delta_time)
                self.new_time_variable = self.second_updater
            if self.second_updater != self.new_time_variable and self.second_updater % 3 != 0:
                self.new_time_variable = self.second_updater
            for wall_row in wall_row_hit_list:
                for wall_row in wall_row_list:
                    wall_row.remove_from_sprite_lists()
                self.current_room = 5
                self.new_time_variable = 0
                self.player.center_y = setup.SCREEN_HEIGHT // 2 - 100
                self.player.center_x = setup.SCREEN_WIDTH - 150
        if self.current_room == 6 and self.new_time_variable == 15:
            wall = arcade.Sprite("images/jonas_character.PNG",
                                 setup.SPRITE_SCALING)
            wall.left = 18 * setup.SPRITE_SIZE
            wall.bottom = 2 * setup.SPRITE_SIZE
            self.rooms[self.current_room].noCol_list.append(wall)



        # Collision with player - displaying text.
        player_list = self.rooms[self.current_room].noCol_list
        player_hit_list = arcade.check_for_collision_with_list(self.player, player_list)

        self.rooms[self.current_room].noCol_list.update()

        for player in player_hit_list:

            if self.current_room == 1 and self.total_time == 0:
                dialogue_1 = arcade.Sprite("images/room_2_dia_1.png", setup.SPRITE_SCALING_TEXT)
                dialogue_2 = arcade.Sprite("images/room_2_dia_2.png", setup.SPRITE_SCALING_TEXT)
                dialogue_1.center_x = 650
                dialogue_1.center_y = 740
                dialogue_2.center_x = 650
                dialogue_2.center_y = 625
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

        if self.current_room == 7 and self.total >= 1:
            self.total_time += delta_time

        if self.current_room == 8:
            self.total_time += delta_time

        if self.current_room == 6:
            if self.total_time == 0:
                self.current_song = 1
                self.play_song()
            self.total_time += delta_time

        if self.current_room == 4:
            self.status_var = 0

        position = self.music.get_stream_position()
        if position == 0.0:
            self.play_song()

def main():
    """ Main method """
    window = MyGame(setup.SCREEN_WIDTH, setup.SCREEN_HEIGHT, setup.SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
