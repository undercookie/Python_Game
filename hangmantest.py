"""

You can see the hangman logic at the def_hangman function at the bottom of the screen.
Feel free to try and make it work with the graphical elemets. I wasn't able to tonight.
I can't figure out how to update the white text on screen. Ideas?

Todo:
- Change on_release of PlayButton to work with Hangman function (line 97 to see my first draft)
- Incorporate random function. List or .txt file? How will a .txt work with final compile?
- Output decision. (See "def output". How does it get called?).  How to update it?
- Drawing of Hangman, right now in 10 steps. Or maybe no drawing?
- Implementation into main code. Import or C+V
"""

from arcade.gui import *
import os
import random


class PlayButton(TextButton):
    def __init__(self, game, x=0, y=0, width=100, height=40, text="Start", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)
        self.game = game

    def on_press(self):
        self.pressed = True

    def on_release(self):
        if self.pressed:
            output = hangman2()
            self.update()
            # Hangman here. Mix OOP & POP
            # Have the random part here, so it doesn't get randomized on every call to function.
            pass


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Hangman Test")
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        arcade.set_background_color(arcade.color.ARSENIC)
        self.text = ""
        self.text_x = 50
        self.text_y = 150
        self.text_font_size = 40
        self.theme = None

    def set_button_textures(self):
        normal = ":resources:gui_themes/Fantasy/Buttons/Normal.png"
        hover = ":resources:gui_themes/Fantasy/Buttons/Hover.png"
        clicked = ":resources:gui_themes/Fantasy/Buttons/Clicked.png"
        locked = ":resources:gui_themes/Fantasy/Buttons/Locked.png"
        self.theme.add_button_textures(normal, hover, clicked, locked)

    def setup_theme(self):
        self.theme = Theme()
        self.theme.set_font(24, arcade.color.ARSENIC)
        self.set_button_textures()

    def set_buttons(self):
        self.button_list.append(PlayButton(self, 60, 570, 110, 50, text="A", theme=self.theme))
        self.button_list.append(PlayButton(self, 60, 515, 110, 50, text="B", theme=self.theme))
        self.button_list.append(PlayButton(self, 60, 460, 110, 50, text="C", theme=self.theme))
        self.button_list.append(PlayButton(self, 60, 405, 110, 50, text="D", theme=self.theme))
        self.button_list.append(PlayButton(self, 60, 350, 110, 50, text="E", theme=self.theme))
        self.button_list.append(PlayButton(self, 60, 295, 110, 50, text="F", theme=self.theme))
        self.button_list.append(PlayButton(self, 180, 570, 110, 50, text="G", theme=self.theme))
        self.button_list.append(PlayButton(self, 180, 515, 110, 50, text="H", theme=self.theme))
        self.button_list.append(PlayButton(self, 180, 460, 110, 50, text="I", theme=self.theme))
        self.button_list.append(PlayButton(self, 180, 405, 110, 50, text="J", theme=self.theme))
        self.button_list.append(PlayButton(self, 180, 350, 110, 50, text="K", theme=self.theme))
        self.button_list.append(PlayButton(self, 180, 295, 110, 50, text="L", theme=self.theme))
        self.button_list.append(PlayButton(self, 300, 570, 110, 50, text="M", theme=self.theme))
        self.button_list.append(PlayButton(self, 300, 515, 110, 50, text="N", theme=self.theme))
        self.button_list.append(PlayButton(self, 300, 460, 110, 50, text="O", theme=self.theme))
        self.button_list.append(PlayButton(self, 300, 405, 110, 50, text="P", theme=self.theme))
        self.button_list.append(PlayButton(self, 300, 350, 110, 50, text="Q", theme=self.theme))
        self.button_list.append(PlayButton(self, 300, 295, 110, 50, text="R", theme=self.theme))
        self.button_list.append(PlayButton(self, 420, 570, 110, 50, text="S", theme=self.theme))
        self.button_list.append(PlayButton(self, 420, 515, 110, 50, text="T", theme=self.theme))
        self.button_list.append(PlayButton(self, 420, 460, 110, 50, text="U", theme=self.theme))
        self.button_list.append(PlayButton(self, 420, 405, 110, 50, text="V", theme=self.theme))
        self.button_list.append(PlayButton(self, 420, 350, 110, 50, text="W", theme=self.theme))
        self.button_list.append(PlayButton(self, 420, 295, 110, 50, text="X", theme=self.theme))
        self.button_list.append(PlayButton(self, 540, 570, 110, 50, text="Y", theme=self.theme))
        self.button_list.append(PlayButton(self, 540, 515, 110, 50, text="Z", theme=self.theme))

    def setup(self):
        self.setup_theme()
        self.set_buttons()

    def on_draw(self):
        arcade.start_render()
        super().on_draw()
        arcade.draw_text(self.text, self.text_x, self.text_y, arcade.color.ALICE_BLUE, self.text_font_size)

    def update(self, delta_time):
        self.text = "Test. How to update this?"



def hangman(current_guesses, turn):
    word = "test"
    guesses = current_guesses
    turns_remaining = turn
    output = ""

    failed = 0

    for char in word:
        if char in guesses:
            output += (char + " ")
        else:
            output += "_ "
            failed += 1
            turns_remaining -= 1

    # My idea here is, that we use an if-statement in the def update to look for WIN or LOSE,
    # and trigger based on that.
    if failed == 0:
        output = "WIN"

    if turns_remaining == 0:
        output = "LOSE"

    return output


def hangman2():
    ali = "TestOfFunctionality"
    return ali


def main():
    game = MyGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()