"""
What happend in this commit?

After, and I'm not kidding, 2 whole hours of trying to figure out how to remove the god damn coins,
it finally happend. Legit euphoria.
The coins will now disappear when you move over them.
Furthermore I added a score counter in the bottom left, and a timer in the bottom right.
I don't know how to only show them when we are in the coin room, but they don't do anything before we enter and pick up,
our first coin.
If the player doesn't exit the room before the counter hits 15 (seconds), they get kicked out, and both are reset.
I still don't know how to make the coins that you picked up, reappear the next time you enter. Ideas?
I added the top entrance to room 4-5-6 as well and the rooms 9-10-11. I think the boss-fight should be in room 7,
without any need to enter one at the top.
The room numbers sound confusing? I made a room_overview.txt file. It should be in this folder.
Now I sleep.

Todo-list:
 - Shorten the on_update definition. I'm getting lost among all the elif statements. Anything we can do?
 - Make coins reappear after fail
 - Make scoreboard and timer only visible in room 8
 - Work out graphical elements in regards to textboxes from Jonas (tutorial)
 - Transition to and from mini-games. Requires mini-game(s) to be completed.
 - Achievements. Sprites or background? Updates how?
 - Experiment with sprites downloads and / or backgrounds.
 - Add animation to character. These sprites already exist.
 - Add sound. Ambiance, footsteps, mumbling for tutorial, etc.

Done-list:
 - Add another .append list for non-collision objects and implement it.
        - We now have 3 sprite lists. Wall, noCol and coin.
 - add a global variable so no objects like coins will be in the walls
 - Add collision for coins, and make them disappear when touched.
 - Make a scoreboard.
"""

import arcade
import os
import random
import setup
import rooms


rooms.setup_room_1()
rooms.setup_room_2()
rooms.setup_room_3()
rooms.setup_room_4()
rooms.setup_room_5()
rooms.setup_room_6()
rooms.setup_room_7()
rooms.setup_room_8()

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

    def setup(self):
        """ Set up the game and initialize the variables. """
        # Set up the player
        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png", setup.SPRITE_SCALING)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 100
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)
        self.score = 0
        self.total = 0
        self.total2 = 0

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
        self.current_room = 1

        self.total_time = 0.0


        # Create a physics engine for this room
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)


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

        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

        minutes = int(self.total_time) // 60
        seconds = int(self.total_time) % 60
        output_time = f"Time: {minutes:02d}:{seconds:02d}"
        arcade.draw_text(output_time, 1150, 20, arcade.color.WHITE, 14)


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

        elif self.player_sprite.center_y < 0 and self.current_room == 8:
            self.current_room = 3
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_y = setup.SCREEN_HEIGHT

        elif self.player_sprite.center_y < 0 and self.current_room == 9:
            self.current_room = 4
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_y = setup.SCREEN_HEIGHT

        elif self.player_sprite.center_y < 0 and self.current_room == 10:
            self.current_room = 5
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_y = setup.SCREEN_HEIGHT

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

        # Collision with coin - removing them.
        coin_list = self.rooms[self.current_room].coin_list
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, coin_list)

        self.rooms[self.current_room].coin_list.update()
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            self.total += 1
            if self.total == 1:
                self.total2 += 1
            self.score += 1

        if self.current_room == 7 and self.total >= 1:
            self.total_time += delta_time


def main():
    """ Main method """
    window = MyGame(setup.SCREEN_WIDTH, setup.SCREEN_HEIGHT, setup.SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()