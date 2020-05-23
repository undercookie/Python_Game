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


Todo-list:
 - Shorten the on_update definition. I'm getting lost among all the elif statements. Anything we can do?
 - Make the hangman game.
 - Achievements. Sprites or background? Updates how?
 - Add animation to character. These sprites already exist. How?
 - Add more sound. Footsteps, mumbling for tutorial, etc.

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
"""

import arcade
import os
import random
import setup
import rooms


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
        self.rooms = None
        self.player_sprite = None
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

    def setup(self):
        """ Set up the game and initialize the variables. """
        # Set up the player
        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_adventurer/femaleAdventurer_walk0.png",
                                           setup.SPRITE_SCALING)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 100
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)
        self.score = 0
        self.total = 0
        self.total2 = 0
        self.status_var = 0
        self.music_list = ["sounds/music_background.mp3", "sounds/music_evil.mp3", "sounds/music_win.mp3"]
        self.current_song = 0
        self.play_song()
        self.second_updater = 0
        self.new_time_variable = 0

        # Our list of rooms
        self.rooms = []

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
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)



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
            self.player_sprite.change_y = setup.MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -setup.MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -setup.MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = setup.MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

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

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.physics_engine.update()

        # Do some logic here to figure out what room we are in, and if we need to go
        # to a different room.
        if self.player_sprite.center_x > setup.SCREEN_WIDTH and self.current_room == 0:
            self.current_room = 1
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = 0

        elif self.player_sprite.center_x > setup.SCREEN_WIDTH and self.current_room == 1:
            self.current_room = 2
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = 0

        elif self.player_sprite.center_x > setup.SCREEN_WIDTH and self.current_room == 2:
            self.current_room = 3
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = 0

        elif self.player_sprite.center_y > setup.SCREEN_HEIGHT and self.current_room == 2:
            self.current_room = 7
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_y = 0

        elif self.player_sprite.center_x > setup.SCREEN_WIDTH and self.current_room == 3:
            self.current_room = 4
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = 0

        elif self.player_sprite.center_y > setup.SCREEN_HEIGHT and self.current_room == 3:
            self.current_room = 8
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_y = 0

        elif self.player_sprite.center_x > setup.SCREEN_WIDTH and self.current_room == 4:
            self.current_room = 5
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = 0

        elif self.player_sprite.center_y > setup.SCREEN_HEIGHT and self.current_room == 4:
            self.current_room = 9
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_y = 0

        elif self.player_sprite.center_x > setup.SCREEN_WIDTH and self.current_room == 5:
            self.current_room = 6
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = 0

        elif self.player_sprite.center_y > setup.SCREEN_HEIGHT and self.current_room == 5:
            self.current_room = 10
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_y = 0

        elif self.player_sprite.center_x > setup.SCREEN_WIDTH and self.current_room == 6:
            self.current_room = 7
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = 0

        elif self.player_sprite.center_x < 0 and self.current_room == 1:
            self.current_room = 0
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = setup.SCREEN_WIDTH

        elif self.player_sprite.center_x < 0 and self.current_room == 2:
            self.current_room = 1
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = setup.SCREEN_WIDTH

        elif self.player_sprite.center_x < 0 and self.current_room == 3:
            self.current_room = 2
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = setup.SCREEN_WIDTH

        elif self.player_sprite.center_x < 0 and self.current_room == 4:
            self.current_room = 3
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = setup.SCREEN_WIDTH

        elif self.player_sprite.center_x < 0 and self.current_room == 5:
            self.current_room = 4
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = setup.SCREEN_WIDTH

        elif self.player_sprite.center_x < 0 and self.current_room == 6:
            self.current_room = 5
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = setup.SCREEN_WIDTH

        elif self.player_sprite.center_x < 0 and self.current_room == 7:
            self.current_room = 6
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = setup.SCREEN_WIDTH

        elif self.player_sprite.center_y < 0 and self.current_room == 7:
            self.current_room = 2
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_y = setup.SCREEN_HEIGHT

        elif self.player_sprite.center_y > setup.SCREEN_HEIGHT and self.current_room == 8:
            self.current_room = 3
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_y = setup.SCREEN_HEIGHT - 50
            self.player_sprite.center_x = setup.SCREEN_WIDTH // 2
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

        elif self.player_sprite.center_y < 0 and self.current_room == 9:
            for coin in self.rooms[self.current_room].coin_list:
                coin.remove_from_sprite_lists()
            self.score = 0
            self.current_room = 4
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_y = setup.SCREEN_HEIGHT

        elif self.player_sprite.center_y < 0 and self.current_room == 10:
            self.current_room = 5
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_y = setup.SCREEN_HEIGHT

        # This one is to throw out player and reset counters if they take more than 20 seconds.
        elif self.current_room == 8 and self.total_time >= 20:
            self.current_room = 3
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_y = setup.SCREEN_HEIGHT - 50
            self.player_sprite.center_x = setup.SCREEN_WIDTH // 2
            self.total_time = 0

        # This one is to throw out player and reset counters if they take more than 15 seconds.
        elif self.total2 >= 1 and self.total_time >= 15:
            self.current_room = 2
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_y = setup.SCREEN_HEIGHT - 50
            self.player_sprite.center_x = setup.SCREEN_WIDTH // 2
            self.total2 = 0
            self.total = 0
            self.total_time = 0
            self.score = 0

        elif self.current_room == 7 and self.score == 4:
            self.current_room = 2
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_y = setup.SCREEN_HEIGHT - 50
            self.player_sprite.center_x = setup.SCREEN_WIDTH // 2
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
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_y = setup.SCREEN_HEIGHT - 50
            self.player_sprite.center_x = setup.SCREEN_WIDTH // 2
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



        # Collision with coin - removing them and creating them again.
        if self.current_room == 7:

            coin_list = self.rooms[self.current_room].coin_list
            coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, coin_list)

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
            coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, coin_list)

            self.rooms[self.current_room].coin_list.update()
            for coin in coin_hit_list:
                coin.remove_from_sprite_lists()
                self.add_coin(delta_time)
                self.score += 1

        if self.current_room == 6:
            wall_row_list = self.rooms[self.current_room].coin_list
            wall_row_hit_list = arcade.check_for_collision_with_list(self.player_sprite, wall_row_list)
            self.rooms[self.current_room].coin_list.update()
            if self.second_updater != self.new_time_variable and self.second_updater % 3 == 0:
                self.add_wall_row(delta_time)
                self.new_time_variable = self.second_updater
            if self.second_updater != self.new_time_variable and self.second_updater % 3 != 0:
                self.new_time_variable = self.second_updater
            for wall_row in wall_row_hit_list:
                wall_row.remove_from_sprite_lists()
                self.current_room = 5
                self.player_sprite.center_y = setup.SCREEN_HEIGHT // 2 - 100
                self.player_sprite.center_x = setup.SCREEN_WIDTH - 150
        if self.current_room == 6 and self.new_time_variable == 15:
            wall = arcade.Sprite("images/jonas_character.PNG",
                                 setup.SPRITE_SCALING)
            wall.left = 18 * setup.SPRITE_SIZE
            wall.bottom = 2 * setup.SPRITE_SIZE
            self.rooms[self.current_room].noCol_list.append(wall)



        # Collision with player - displaying text.
        player_list = self.rooms[self.current_room].noCol_list
        player_hit_list = arcade.check_for_collision_with_list(self.player_sprite, player_list)

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


            # Set its position to a random height and off screen right
       #     dialogue_1.center_x = 650
       #     dialogue_1.center_y = 740
       #     dialogue_2.center_x = 650
       #     dialogue_2.center_y = 625

            # Add it to the enemies list
           # self.rooms[self.current_room].wall_list.append(dialogue_1)
           # self.rooms[self.current_room].wall_list.append(dialogue_2)

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
